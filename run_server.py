# run_server.py
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import json
from datetime import datetime

# Import our modules
from stt import transcribe
from tts import speak
from agent import get_response
from memory import update_history, load_history
from medical_knowledge import load_medical_knowledge

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Global variables
is_processing = False


@app.route("/")
def index():
    """Serve the main chat interface"""
    return render_template("index.html")


@app.route("/process_voice", methods=["POST"])
def process_voice():
    """Process voice input from the web interface"""
    global is_processing

    if is_processing:
        return jsonify({"error": "Already processing audio"}), 429

    try:
        is_processing = True

        # Get audio file from request
        if "audio" not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files["audio"]
        if audio_file.filename == "":
            return jsonify({"error": "No audio file selected"}), 400

        # Save audio file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            audio_file.save(tmp_file.name)
            temp_audio_path = tmp_file.name

        # Transcribe audio
        user_input = transcribe(temp_audio_path)

        # Clean up temp file
        os.unlink(temp_audio_path)

        if not user_input or not user_input.strip():
            return jsonify({"error": "No speech detected"}), 400

        # Update conversation history
        update_history("user", user_input)
        history = load_history()

        # Get AI response
        assistant_response = get_response(history)
        update_history("assistant", assistant_response)

        # Generate TTS audio
        tts_filename = f'response_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        tts_path = os.path.join(tempfile.gettempdir(), tts_filename)

        # Create TTS audio file
        try:
            speak_to_file(assistant_response, tts_path)
            audio_url = f"/audio/{tts_filename}"
        except Exception as e:
            print(f"TTS Error: {e}")
            audio_url = None

        return jsonify({
            "user_input": user_input,
            "assistant_response": assistant_response,
            "audio_url": audio_url,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        print(f"Error processing voice: {e}")
        return jsonify({"error": "Failed to process voice input"}), 500

    finally:
        is_processing = False


@app.route("/audio/<filename>")
def serve_audio(filename):
    """Serve generated TTS audio files"""
    try:
        audio_path = os.path.join(tempfile.gettempdir(), secure_filename(filename))
        if os.path.exists(audio_path):
            return send_file(audio_path, mimetype="audio/wav")
        else:
            return jsonify({"error": "Audio file not found"}), 404
    except Exception as e:
        print(f"Error serving audio: {e}")
        return jsonify({"error": "Failed to serve audio"}), 500


@app.route("/chat_history")
def get_chat_history():
    """Get conversation history"""
    try:
        history = load_history()
        return jsonify({"history": history})
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return jsonify({"error": "Failed to get chat history"}), 500


@app.route("/clear_history", methods=["POST"])
def clear_chat_history():
    """Clear conversation history"""
    try:
        # Clear the conversation log
        with open("aaconversation_log.json", "w") as f:
            json.dump([], f)
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error clearing history: {e}")
        return jsonify({"error": "Failed to clear history"}), 500


@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Clifton Hospital Voice Assistant",
        "timestamp": datetime.now().isoformat()
    })


def speak_to_file(text, filepath):
    """Generate TTS audio and save to file"""
    try:
        from TTS.api import TTS

        # Initialize TTS model if not already done
        if not hasattr(speak_to_file, "tts_model"):
            speak_to_file.tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False,
                                          gpu=False)

        # Generate TTS audio
        speak_to_file.tts_model.tts_to_file(text=text, file_path=filepath)

    except Exception as e:
        print(f"TTS Error: {e}")
        # Fallback to basic TTS if Coqui fails (though it should be installed)
        # This fallback might not be ideal for speed, but prevents total failure
        speak(text)  # This will use the existing TTS function from tts.py


def initialize_app():
    """Initialize the application"""
    print("🏥 Initializing Clifton Hospital Voice Assistant...")

    # Load medical knowledge into Pinecone
    try:
        load_medical_knowledge()
        print("✅ Medical knowledge loaded successfully")
    except Exception as e:
        print(f"⚠️ Warning: Could not load medical knowledge: {e}")

    print("🚀 Clifton Hospital Voice Assistant is ready!")
    print("📍 Hospital Location: Street 8, Shah Allah Ditta, Islamabad")
    print("🆘 Emergency: 911")

if __name__ == '__main__':
    initialize_app()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        ssl_context=('certs/cert.pem', 'certs/key.pem'),
        threaded=True
    )
