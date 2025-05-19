from fastapi import APIRouter, UploadFile, File, Form, Request
import os
import shutil
from src.db import db  # Make sure this import works

router = APIRouter()

UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.get("/history")
async def get_history():
    messages = await db.messages.find().sort("_id", 1).to_list(length=1000)
    for msg in messages:
        msg["_id"] = str(msg["_id"])
    return messages

@router.post("/history")
async def save_message(request: Request):
    message = await request.json()
    await db.messages.insert_one(message)
    return {"status": "ok"}

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