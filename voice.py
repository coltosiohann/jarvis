# voice.py
import time
import threading
import hashlib
import os
import requests
import pygame
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

if not API_KEY or not VOICE_ID:
    raise ValueError("Missing ElevenLabs API key or voice ID in .env")

# Initialize pygame mixer for audio playback
pygame.mixer.init()
CACHE_FOLDER = "tts_cache"
os.makedirs(CACHE_FOLDER, exist_ok=True)

current_sound_channel = None
play_lock = threading.Lock()
_speaking_flag = False

def stop_speaking():
    global current_sound_channel, _speaking_flag
    with play_lock:
        if current_sound_channel:
            current_sound_channel.stop()
            current_sound_channel = None
        pygame.mixer.stop()
        _speaking_flag = False

def is_speaking():
    global _speaking_flag
    return _speaking_flag

def speak(text):
    global current_sound_channel, _speaking_flag

    if not text or not isinstance(text, str) or text.strip() == "":
        print("Empty or invalid text, skipping TTS request.")
        return

    text = text.strip()
    print(f"JARVIS: {text}")

    hash_name = hashlib.md5(text.encode()).hexdigest()
    filename = os.path.join(CACHE_FOLDER, f"{hash_name}.mp3")

    if not os.path.exists(filename):
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
            else:
                print("ElevenLabs TTS Error:", response.status_code)
                print("Response:", response.text)
                return
        except Exception as e:
            print("Error during TTS request:", e)
            return

    try:
        with play_lock:
            sound = pygame.mixer.Sound(filename)
            _speaking_flag = True
            current_sound_channel = sound.play()

        # Wait while speaking
        while pygame.mixer.get_busy():
            time.sleep(0.1)
    except Exception as e:
        print("Error during audio playback:", e)
    finally:
        with play_lock:
            _speaking_flag = False
            current_sound_channel = None

def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,), daemon=True)
    thread.start()

# Speech recognition helper
recognizer = sr.Recognizer()

def listen_until_silence(timeout=10, phrase_time_limit=5):
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Please speak.")

        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Got audio, recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    return ""

def listen_until_silence_safe():
    # Wait until speaking is finished before listening
    while is_speaking():
        time.sleep(0.1)
    return listen_until_silence()
