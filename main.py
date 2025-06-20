import os
import time
import random
import struct
import threading

import pvporcupine
import sounddevice as sd

from voice import (
    listen_until_silence,
    speak_async,
    stop_speaking,
    process_command_async,
    is_speaking,
)
from commands import handle_command  # your command handler
from dotenv import load_dotenv

load_dotenv()

# Wake word detector using Porcupine
class WakeWordDetector:
    def __init__(self, keyword="jarvis"):
        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        if not access_key:
            raise ValueError("PICOVOICE_ACCESS_KEY not found in environment variables")

        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[keyword]
        )
        self.detected = False

    def audio_callback(self, indata, frames, time_info, status):
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, indata)
        result = self.porcupine.process(pcm)
        if result >= 0:
            self.detected = True

    def detect(self):
        self.detected = False
        try:
            with sd.InputStream(
                samplerate=self.porcupine.sample_rate,
                blocksize=self.porcupine.frame_length,
                channels=1,
                dtype="int16",
                callback=self.audio_callback,
            ):
                print("Listening for wake word...")
                while not self.detected:
                    time.sleep(0.1)
            return True
        finally:
            self.porcupine.delete()


def detect_wake_word():
    detector = WakeWordDetector()
    return detector.detect()


def is_special_command(command: str) -> bool:
    keywords = [
        "object detection",
        "shutdown",
        "youtube",
        "exit",
        "goodbye",
        "stop",
        "quit",
        "time",
    ]
    return any(k in command for k in keywords)


def get_random_acknowledgement() -> str:
    phrases = [
        "Yes?",
        "I'm listening.",
        "At your service.",
        "Go ahead.",
        "What can I do for you?",
    ]
    return random.choice(phrases)


def wait_until_done_speaking():
    while is_speaking():
        time.sleep(0.1)


def safe_listen() -> str:
    # Wait until JARVIS stops speaking before listening
    while is_speaking():
        time.sleep(0.1)
    return listen_until_silence()


def dialogue_session(timeout=20):
    print("Entering dialogue mode, waiting for follow-up commands...")

    last_interaction = time.time()

    while True:
        if time.time() - last_interaction > timeout:
            print("Dialogue session timed out due to inactivity.")
            break

        command = safe_listen()
        if not command:
            continue

        print(f"Dialogue command received: {command}")

        if any(
            phrase in command
            for phrase in ["no", "thank you", "stop", "goodbye", "exit", "quit"]
        ):
            speak_async("Understood, Sir. Standing by.")
            wait_until_done_speaking()
            break

        if is_special_command(command):
            handle_command(command)
        else:
            process_command_async(command)

        last_interaction = time.time()


def main():
    speak_async(
        "JARVIS is online. Hello Sir! Your system is fully operational! I am ready to assist you today! What can I do for you?"
    )
    wait_until_done_speaking()

    while True:
        print("Waiting for wake word...")
        detected = detect_wake_word()

        if detected:
            print("Wake word detected.")
            stop_speaking()  # stop any ongoing speech (stop TTS)

            time.sleep(1)  # delay to avoid residual audio detection

            ack = get_random_acknowledgement()
            speak_async(ack)
            wait_until_done_speaking()

            command = safe_listen()
            if command:
                print(f"Command received: {command}")

                if is_special_command(command):
                    handle_command(command)
                else:
                    process_command_async(command)

                dialogue_session(timeout=20)
            else:
                speak_async("Sorry, I didn't catch that.")
                wait_until_done_speaking()


if __name__ == "__main__":
    main()
