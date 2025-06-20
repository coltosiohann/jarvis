import os
import datetime
import webbrowser
from voice import speak

def handle_command(command):
    command = command.lower()
    
    if "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}.")
    
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")
    
    elif "shutdown" in command:
        speak("Shutting down the system.")
        os.system("shutdown now")
    
    elif "exit" in command or "goodbye" in command:
        speak("Goodbye!")
        exit(0)
    
    else:
        speak("Sorry, I don't know how to do that yet.")
