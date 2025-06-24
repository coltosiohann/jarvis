import time
import speech_recognition as sr
import threading

from voice import speak, speak_async, stop_speaking, is_speaking

recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_until_silence(timeout=10, phrase_time_limit=5):
    with mic as source:
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

def process_command_async(prompt):
    stop_speaking()
    speak_async("Thinking...")

    # import here to avoid circular import
    from brain import think

    def think_and_speak():
        try:
            response = think(prompt)
        except Exception as e:
            print("Error during think():", e)
            response = "Sorry Sir, I encountered an error."
        speak(response)

    thread = threading.Thread(target=think_and_speak, daemon=True)
    thread.start()
