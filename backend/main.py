# main.py
import time
import struct
import threading
import random
import os
import pvporcupine
import sounddevice as sd

from jarvis.backend.voice import speak_async, stop_speaking, is_speaking, listen_until_silence_safe
from jarvis.backend.brain import process_command_async

def get_random_acknowledgement() -> str:
    phrases = [
        "Yes?",
        "I'm listening.",
        "At your service.",
        "Go ahead.",
        "What can I do for you?",
    ]
    return random.choice(phrases)

class WakeWordDetector:
    def __init__(self, keyword="jarvis"):
        access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        if not access_key:
            raise ValueError("PORCUPINE_ACCESS_KEY not found in environment variables")

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

def wait_until_done_speaking():
    while is_speaking():
        time.sleep(0.1)

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
            stop_speaking()  # Just in case something is being spoken
            time.sleep(1.0)  # Brief pause after wake word to avoid echo

            ack = get_random_acknowledgement()
            speak_async(ack)
            wait_until_done_speaking()

            time.sleep(1.0)  # Delay after speaking to prevent hearing itself

            command = listen_until_silence_safe()
            if command:
                print(f"Command received: {command}")
                process_command_async(command)
            else:
                speak_async("Sorry, I didn't catch that.")
                wait_until_done_speaking()

if __name__ == "__main__":
    main()
