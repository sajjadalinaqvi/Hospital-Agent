import sounddevice as sd
import numpy as np
import threading
import time
from listener import vad_event, interrupt_tts

# Interrupt detection settings
INTERRUPT_THRESHOLD = 0.01  # Volume threshold for detecting speech
INTERRUPT_DURATION = 0.3    # How long speech must be detected to trigger interrupt

interrupt_event = threading.Event()
interrupt_thread = None

def detect_interrupt():
    """Continuously monitor for speech to interrupt TTS"""
    print("🔊 Interrupt detection started...")
    
    def audio_callback(indata, frames, time_info, status):
        volume_norm = np.linalg.norm(indata) * 10
        
        if volume_norm > INTERRUPT_THRESHOLD:
            # Speech detected, set interrupt event
            interrupt_event.set()
            vad_event.set()  # Signal to listener that interruption occurred
            interrupt_tts()  # Stop TTS immediately
    
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=16000, blocksize=512):
        while True:
            if interrupt_event.is_set():
                time.sleep(0.1)  # Brief pause after interrupt
                interrupt_event.clear()
            time.sleep(0.01)

def start_interrupt_listener():
    """Start the interrupt detection in a separate thread"""
    global interrupt_thread
    if interrupt_thread is None or not interrupt_thread.is_alive():
        interrupt_thread = threading.Thread(target=detect_interrupt, daemon=True)
        interrupt_thread.start()

def stop_interrupt_listener():
    """Stop the interrupt detection"""
    global interrupt_thread
    if interrupt_thread and interrupt_thread.is_alive():
        interrupt_event.set()
        interrupt_thread = None

