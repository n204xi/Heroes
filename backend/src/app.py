from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes.chat import router as chat_router
from src.routes.history import router as history_router
from src.routes.profile import router as profile_router
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.middleware.cors import CORSMiddleware
import os
from src.services.db import db

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

app.include_router(chat_router, prefix="/chat")
app.include_router(history_router, prefix="/history")
app.include_router(profile_router, prefix="/profile")

AUDIO_DIR = os.path.join('/app', 'audio')
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")
app.mount("/uploads", StaticFiles(directory=os.path.join('/app', 'uploads')), name="uploads")
app.mount("/voice_uploads", StaticFiles(directory=os.path.join('/app', 'voice_uploads')), name="voice_uploads")
app.mount("/profile_pics", StaticFiles(directory=os.path.join('/app', 'profile_pics')), name="profile_pics")

def send_proactive_message():
    ai_message = {
        "text": "This is your scheduled reminder from Heroes!",
        "from": "ai",
        "character": "Sora",
        "notification": True
    }
    db.messages.insert_one(ai_message)

scheduler.add_job(send_proactive_message, "interval", hours=1)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Friend Chatbot API!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://heroes.vercel.app"],  # <-- Updated to your actual Vercel frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

