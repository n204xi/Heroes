from fastapi import APIRouter, Request
from src.db import db

router = APIRouter()

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