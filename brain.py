import os
import requests
import threading
from playsound import playsound
import uuid
import hashlib
import openai
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API setup
OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

client = openai.OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ElevenLabs TTS setup
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
if not ELEVENLABS_API_KEY or not VOICE_ID:
    raise ValueError("ElevenLabs API key or Voice ID not found in .env")

CACHE_FOLDER = "tts_cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

def speak(text):
    if not text or not isinstance(text, str) or text.strip() == "":
        print("Empty or invalid text, skipping TTS request.")
        return

    text = text.strip()
    print(f"JARVIS: {text}")

    hash_name = hashlib.md5(text.encode()).hexdigest()
    filename = os.path.join(CACHE_FOLDER, f"{hash_name}.mp3")

    if os.path.exists(filename):
        playsound(filename)
        return

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
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
            print("ElevenLabs TTS Error:", response.status_code)
            print("Response:", response.text)
    except Exception as e:
        print("Error during TTS request or playback:", e)

def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,), daemon=True)
    thread.start()

def think(prompt: str) -> str:
    system_prompt = (
        "You are J.A.R.V.I.S., Tony Stark’s AI assistant, intelligent, calm, and articulate. "
        "You speak with a formal British tone, but can be witty and subtly sarcastic. "
        "Analyze problems quickly and provide insightful suggestions. "
        "Stay in character. Call the user 'Sir'. Avoid unnecessary apologies, be confident and precise."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=messages
        )
        answer = response.choices[0].message.content.strip()
        return answer

    except Exception as e:
        print(f"[OpenRouter Error]: {e}")
        return "Sorry, I'm having trouble thinking right now."

def think_and_speak(prompt):
    answer = think(prompt)
    speak(answer)

def ask_jarvis_async(prompt):
    # Speak "Thinking..." immediately
    speak_async("Thinking...")
    # Then start background thread to think + speak actual answer
    thread = threading.Thread(target=think_and_speak, args=(prompt,), daemon=True)
    thread.start()
