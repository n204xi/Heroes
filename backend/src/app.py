from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.routes.chat import router as chat_router
from src.routes.history import router as history_router
from src.routes.profile import router as profile_router
from apscheduler.schedulers.background import BackgroundScheduler
from src.db import db
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
scheduler = BackgroundScheduler()
scheduler.start()

app.include_router(chat_router, prefix="/chat")
app.include_router(history_router, prefix="/history")
app.include_router(profile_router, prefix="/profile")

AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../audio'))
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
VOICE_UPLOADS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../voice_uploads'))
app.mount("/voice_uploads", StaticFiles(directory=VOICE_UPLOADS_DIR), name="voice_uploads")
PROFILE_PICS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../profile_pics'))
app.mount("/profile_pics", StaticFiles(directory=PROFILE_PICS_DIR), name="profile_pics")

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
    allow_origins=["https://your-frontend.onrender.com"],  # <-- Replace with your actual frontend Render URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

