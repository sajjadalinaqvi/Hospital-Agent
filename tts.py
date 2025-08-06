from TTS.api import TTS
import pygame
import os
import time

# Initialize TTS model (download if not exists)
# This model is good for human-like speech and relatively fast

os.environ["USE_CPU"] = "True"
tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def speak(text):
    filename = "temp_coqui.wav"
    tts_model.tts_to_file(text=text, file_path=filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.quit()

    try:
        os.remove(filename)
    except Exception as e:
        print(f"⚠️ Could not delete {filename}: {e}")


