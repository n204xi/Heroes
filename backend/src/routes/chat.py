# Google Docs API support removed. To analyze a Google Doc, please download it as a PDF or text file and upload it here.
from fastapi import APIRouter, Form, UploadFile, File, HTTPException
from src.services.elevenlabs_service import ElevenLabsService
from src.services.openai_service import get_ai_response
from src.services.file_analysis import perform_analysis
from src.services.db import db
import shutil
import os
import re
import requests
import openai
import logging

router = APIRouter()

VOICE_IDS = {
    "Sora": "fAt309m8BNzwjpxxBgs3",
    "Connor": "wCy1ydaMFBmZZwQiOeNS",
    "Baymax": "Zhqb1TETGbCYZOutkCrI",
    "Vanitas": "6hBhtPwuEgGi7izpHewi",
    "Moritz": "QRhAvK854mQXaP6NgwVQ",
    "Ventus": "eYHLb8tAFD1PNP8VSQKT",
    "Tadashi": "GHJhJZTqmC3Odw0RyDeu"
}

elevenlabs = ElevenLabsService(api_key=None)  # Uses .env key

# Allowed file types and max size (5MB)
ALLOWED_FILE_TYPES = {"image/png", "image/jpeg", "application/pdf", "text/plain"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# TODO: Implement authentication for all endpoints

def validate_file(file: UploadFile):
    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail=f"File type {file.content_type} not allowed.")
    file.file.seek(0, os.SEEK_END)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB).")

@router.post("/message")
async def chat_message(
    message: str = Form(...),
    character: str = Form("Sora")
):
    try:
        user_message = {"text": message, "from": "user", "character": character}
        await db.messages.insert_one(user_message)

        # Google Docs API support removed. To analyze a document, please upload it as a PDF or text file.
        ai_reply = get_ai_response(message, character)
        ai_message = {"text": ai_reply, "from": "ai", "character": character}
        await db.messages.insert_one(ai_message)

        voice_id = VOICE_IDS.get(character, VOICE_IDS["Sora"])
        audio_url = elevenlabs.text_to_speech(ai_reply, voice_id)
        return {"reply": ai_reply, "audio_url": audio_url, "character": character}
    except Exception as e:
        logging.exception("Error in /message endpoint")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    character: str = Form("Sora")
):
    try:
        validate_file(file)
        upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"/uploads/{file.filename}"
        file_type = file.content_type

        user_message = {
            "text": f"[File uploaded: {file.filename}]",
            "from": "user",
            "fileUrl": file_url,
            "fileType": file_type,
            "fileName": file.filename
        }
        await db.messages.insert_one(user_message)

        ai_message = {
            "text": "File uploaded and analyzed.",
            "from": "ai",
            "character": character
        }
        await db.messages.insert_one(ai_message)

        # Analyze file
        if file.content_type.startswith("image/"):
            with open(file_path, "rb") as img_file:
                import base64
                img_b64 = base64.b64encode(img_file.read()).decode("utf-8")
            prompt = "Describe the contents of this image and provide any insights or context you can."
            response = get_ai_response(
                {"image": img_b64, "prompt": prompt},
                character=character,
                vision=True
            )
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as doc_file:
                content = doc_file.read()
            prompt = f"Analyze the following document and summarize its contents:\n\n{content}"
            response = get_ai_response(prompt, character=character)

        voice_id = VOICE_IDS.get(character, VOICE_IDS["Sora"])
        audio_url = elevenlabs.text_to_speech(response, voice_id)
        # TODO: Implement periodic cleanup of old files in uploads/
        return {"reply": response, "audio_url": audio_url, "character": character}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error in /upload endpoint")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/proactive")
async def proactive_message(
    text: str = Form(...),
    character: str = Form("Sora")
):
    try:
        doc = await db.away_status.find_one({"character": character})
        if not doc or not doc.get("enabled", False):
            return {"status": "not_sent", "reason": "Away messages are disabled for this character."}
        ai_message = {
            "text": text,
            "from": "ai",
            "character": character,
            "notification": True
        }
        await db.messages.insert_one(ai_message)
        return {"status": "sent", "message": ai_message}
    except Exception as e:
        logging.exception("Error in /proactive endpoint")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/away_status")
async def update_away_status(character: str = Form(...), enabled: bool = Form(...)):
    try:
        await db.away_status.update_one(
            {"character": character},
            {"$set": {"enabled": enabled}},
            upsert=True
        )
        return {"character": character, "away_enabled": enabled}
    except Exception as e:
        logging.exception("Error in /away_status POST endpoint")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.get("/away_status")
async def get_status(character: str):
    try:
        doc = await db.away_status.find_one({"character": character})
        enabled = doc["enabled"] if doc else False
        return {"character": character, "away_enabled": enabled}
    except Exception as e:
        logging.exception("Error in /away_status GET endpoint")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/voice_message")
async def voice_message(
    file: UploadFile = File(...),
    character: str = Form("Sora")
):
    try:
        if file.content_type not in {"audio/wav", "audio/mpeg", "audio/mp3", "audio/x-wav"}:
            raise HTTPException(status_code=400, detail="Unsupported audio file type.")
        upload_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../voice_uploads'))
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                "whisper-1",
                audio_file,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        user_text = transcript["text"]

        user_message = {
            "text": user_text,
            "from": "user",
            "character": character,
            "audioUrl": f"/voice_uploads/{file.filename}"
        }
        await db.messages.insert_one(user_message)

        ai_reply = get_ai_response(user_text, character)
        ai_message = {"text": ai_reply, "from": "ai", "character": character}
        await db.messages.insert_one(ai_message)

        voice_id = VOICE_IDS.get(character, VOICE_IDS["Sora"])
        audio_url = elevenlabs.text_to_speech(ai_reply, voice_id)
        # TODO: Implement periodic cleanup of old files in voice_uploads/
        return {
            "reply": ai_reply,
            "audio_url": audio_url,
            "character": character
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error in /voice_message endpoint")
        raise HTTPException(status_code=500, detail="Internal server error.")