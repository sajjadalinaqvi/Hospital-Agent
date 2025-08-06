# main.py

from stt import transcribe
from tts import speak
from agent import get_response
from memory import update_history, load_history,get_messages
from interrupt import start_interrupt_listener, interrupt_event
from listener import start_listening, record_and_detect_speech
import time
import threading


def run_agent():
    print("🏥 Clifton Hospital Voice Agent is starting...")

    # Start continuous listening and interrupt detection
    start_listening()
    start_interrupt_listener()

    history = load_history()

    print("👂 Agent is ready and listening continuously...")
    print("💬 Speak to start a conversation...")

    while True:
        try:
            # Wait for speech detection
            audio_file = record_and_detect_speech()

            if audio_file:
                # Transcribe the recorded speech
                user_input = transcribe(audio_file)

                if user_input and user_input.strip():
                    print(f"🗣️ You: {user_input}")

                    # Update conversation history
                    update_history("user", user_input)
                    history = load_history()

                    # Get response from agent
                    response = get_response(history)
                    update_history("assistant", response)

                    print(f"🤖 Dr. Assistant: {response}")

                    # Speak response (can be interrupted)
                    speak_with_interrupt_handling(response)
                else:
                    print("🔇 No speech detected or transcription failed.")

            # Small delay to prevent excessive CPU usage
            time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n👋 Shutting down agent...")
            break
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            time.sleep(1)  # Brief pause before retrying


def speak_with_interrupt_handling(text):
    """Speak text while monitoring for interruptions"""

    def speak_thread():
        speak(text)

    # Start speaking in a separate thread
    speech_thread = threading.Thread(target=speak_thread, daemon=True)
    speech_thread.start()

    # Monitor for interruptions while speaking
    while speech_thread.is_alive():
        if interrupt_event.is_set():
            print("⚠️ Speech interrupted by user")
            interrupt_event.clear()
            break
        time.sleep(0.1)


if __name__ == "__main__":
    run_agent()
