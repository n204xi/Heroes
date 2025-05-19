import os
import json
from fastapi import APIRouter, UploadFile, File, Form
from src.db import db

router = APIRouter()
PROFILE_PICS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../profile_pics'))
os.makedirs(PROFILE_PICS_DIR, exist_ok=True)
PROFILE_PICS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../profile_pics.json'))

@router.post("/upload_profile_pic")
async def upload_profile_pic(
    character: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = os.path.join(PROFILE_PICS_DIR, f"{character}_{file.filename}")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    await db.profile_pics.update_one(
        {"character": character},
        {"$set": {"profile_pic_url": f"/profile_pics/{character}_{file.filename}"}},
        upsert=True
    )
    return {"character": character, "profile_pic_url": f"/profile_pics/{character}_{file.filename}"}

@router.get("/profile_pic")
async def get_profile_pic(character: str):
    doc = await db.profile_pics.find_one({"character": character})
    return {"profile_pic_url": doc["profile_pic_url"] if doc else None}