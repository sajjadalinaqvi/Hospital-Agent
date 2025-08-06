# stt.py

import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os

# Load model once
model = whisper.load_model("medium.en")

def transcribe(path=None, duration=10):
    """
    Transcribe either a WAV file or live mic input.
    :param path: Path to WAV file. If None, records live audio.
    :param duration: Recording duration in seconds for live mode.
    :return: Transcribed text string.
    """
    if path:
        print(f"📂 Transcribing from file: {path}")
        result = model.transcribe(path, language="en")
        return result["text"].strip()
    
    print("🎤 Listening (live mic)...")
    fs = 16000
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav.write(tmp.name, fs, audio)
        result = model.transcribe(tmp.name)
        os.remove(tmp.name)

    return result["text"].strip()
