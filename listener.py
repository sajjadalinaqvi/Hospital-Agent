import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
import queue
import time

# Audio recording settings
SAMPLE_RATE = 16000  # 16kHz for better compatibility with Whisper
CHANNELS = 1
BLOCK_SIZE = 1024

# Voice Activity Detection settings
VAD_THRESHOLD = 0.01  # Volume threshold for detecting speech
SILENCE_DURATION = 1.5  # Seconds of silence before stopping recording
MIN_SPEECH_DURATION = 0.5  # Minimum speech duration to consider valid

# Queues for audio data and VAD events
audio_queue = queue.Queue()
vad_event = threading.Event()
stop_listening_event = threading.Event()

def audio_callback(indata, frames, time_info, status):
    """Callback function for audio input stream"""
    if status:
        print(f"Recording status: {status}")
    audio_queue.put(indata.copy())

def listen_continuously():
    """Continuously listen for audio input"""
    print("👂 Agent is continuously listening...")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=audio_callback, blocksize=BLOCK_SIZE):
        while not stop_listening_event.is_set():
            sd.sleep(100)  # Small sleep to prevent busy-waiting

def start_listening():
    """Start continuous listening in a separate thread"""
    stop_listening_event.clear()
    threading.Thread(target=listen_continuously, daemon=True).start()

def stop_listening():
    """Stop continuous listening"""
    stop_listening_event.set()

def detect_voice_activity():
    """Detect when user starts and stops speaking"""
    frames = []
    speaking = False
    silence_start_time = None
    speech_start_time = None

    print("🎤 Waiting for speech...")

    while True:
        if not audio_queue.empty():
            data = audio_queue.get()
            volume_norm = np.linalg.norm(data) * 10

            # Check if speech is detected
            if volume_norm > VAD_THRESHOLD:
                frames.append(data)

                if not speaking:
                    # Speech started
                    speaking = True
                    speech_start_time = time.time()
                    silence_start_time = None
                    print("🗣️ Speech detected, recording...")

            elif speaking:
                # User was speaking but now there's silence
                frames.append(data)  # Keep recording for a bit after speech ends

                if silence_start_time is None:
                    silence_start_time = time.time()
                elif (time.time() - silence_start_time) > SILENCE_DURATION:
                    # Enough silence detected, check if we have valid speech
                    speech_duration = time.time() - speech_start_time if speech_start_time else 0

                    if speech_duration >= MIN_SPEECH_DURATION:
                        print("✅ Speech ended, processing...")
                        break
                    else:
                        # Speech was too short, reset and continue listening
                        print("⚠️ Speech too short, continuing to listen...")
                        frames = []
                        speaking = False
                        silence_start_time = None
                        speech_start_time = None

            # Check for interruption from TTS
            if vad_event.is_set():
                vad_event.clear()
                print("🔄 VAD interrupted.")
                return None

        time.sleep(0.01)  # Prevent busy-waiting

    # Process recorded audio
    if frames:
        audio_np = np.concatenate(frames, axis=0)
        filename = "recorded_speech.wav"
        sf.write(filename, audio_np, SAMPLE_RATE)
        print("✅ Speech recorded and saved.")
        return filename

    return None

def record_and_detect_speech():
    """Main function to record speech with voice activity detection"""
    return detect_voice_activity()

# For barge-in, we need to stop TTS playback immediately
import pygame

def interrupt_tts():
    """Interrupt TTS playback immediately"""
    if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
        print("⏹️ Interrupting TTS...")
        pygame.mixer.music.stop()

