import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form
from src.services.db import db

router = APIRouter()

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    character: str = Form("Sora")
):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
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

    return {
        "reply": ai_message["text"],
        "audio_url": None,
        "character": character,
        "fileUrl": file_url,
        "fileType": file_type,
        "fileName": file.filename
    }

@router.post("/message")
async def chat_message(
    message: str = Form(...),
    character: str = Form("Sora")
):
    user_message = {"text": message, "from": "user", "character": character}
    await db.messages.insert_one(user_message)

    # ...generate AI reply as before...
    ai_message = {"text": ai_reply, "from": "ai", "character": character}
    await db.messages.insert_one(ai_message)

    # ...return response as before...