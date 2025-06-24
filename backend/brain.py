import threading
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

from backend.voice import speak_async, stop_speaking
from backend.memory_manager import log_memory

def think(prompt: str, model: str = "gpt-3.5-turbo") -> str:
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
            model=model,
            messages=messages
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        print(f"[OpenAI Error]: {e}")
        return "Sorry Sir, I am having trouble thinking right now."

def process_command_async(prompt, model: str = "gpt-3.5-turbo"):
    stop_speaking()
    speak_async("Thinking...")

    def think_and_speak():
        try:
            response = think(prompt, model=model)
            # Automatically log conversation to memory
            log_memory(f"User: {prompt}\nJARVIS: {response}")
        except Exception as e:
            print("Error during think():", e)
            response = "Sorry Sir, I encountered an error."
        speak_async(response)

    thread = threading.Thread(target=think_and_speak, daemon=True)
    thread.start()