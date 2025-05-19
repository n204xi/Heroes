import requests
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

AUDIO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../audio'))
os.makedirs(AUDIO_DIR, exist_ok=True)

class ElevenLabsService:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = "https://api.elevenlabs.io/v1/text-to-speech"

    def text_to_speech(self, text, voice_id):
        url = f"{self.base_url}/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_path = os.path.join(AUDIO_DIR, audio_filename)
            with open(audio_path, "wb") as f:
                f.write(response.content)
            return f"/audio/{audio_filename}"
        else:
            return None