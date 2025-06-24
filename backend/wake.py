import os
import pvporcupine
import pyaudio
import struct
from dotenv import load_dotenv

from backend.voice import listen_until_silence
from backend.brain import process_command_async

load_dotenv()  # Load environment variables from .env

def detect_wake_word(keyword="jarvis"):
    access_key = os.getenv("PORCUPINE_ACCESS_KEY")
    if not access_key:
        raise ValueError("Porcupine access key not found. Please set PORCUPINE_ACCESS_KEY in .env")

    porcupine = pvporcupine.create(
        access_key=access_key,
        keywords=[keyword]
    )
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for wake word...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm_unpacked)
            if result >= 0:
                print("Wake word detected!")
                # Listen for command after wake word
                print("Listening for your command...")
                command = listen_until_silence()
                print(f"Recognized command: {command}")
                if command:
                    process_command_async(command)
                print("Listening for wake word...")
    except KeyboardInterrupt:
        print("Wake word listener stopped by user.")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        pa.terminate()
        porcupine.delete()