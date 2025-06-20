import os
import threading
import hashlib
import requests
import speech_recognition as sr
from playsound import playsound
from dotenv import load_dotenv
import uuid

load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

CACHE_FOLDER = "tts_cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

def speak(text):
    if not text or not isinstance(text, str) or text.strip() == "":
        print("Empty or invalid text, skipping TTS request.")
        return

    if not API_KEY or not VOICE_ID:
        print("Missing ElevenLabs API key or Voice ID in environment variables.")
        return

    text = text.strip()
    print(f"JARVIS: {text}")

    # Create filename based on hash of the text
    hash_name = hashlib.md5(text.encode()).hexdigest()
    filename = os.path.join(CACHE_FOLDER, f"{hash_name}.mp3")

    # Play from cache if available
    if os.path.exists(filename):
        playsound(filename)
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            playsound(filename)
        else:
            print(f"ElevenLabs TTS Error: {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print("Error during TTS request or playback:", e)

def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,), daemon=True)
    thread.start()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak_async("Sorry, my speech service is down.")
            return ""
