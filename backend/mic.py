import sounddevice as sd
import numpy as np

duration = 5  # seconds
fs = 16000

print("Recording...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()
print("Recording finished.")

rms = np.sqrt(np.mean(np.square(audio)))
print(f"RMS audio level: {rms}")
