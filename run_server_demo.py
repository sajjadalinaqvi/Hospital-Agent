# run_server_demo.py - Demo version without Pinecone dependency
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import json
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Mock medical knowledge for demo
DEMO_MEDICAL_RESPONSES = {
    "appointment": "I'd be happy to help you book an appointment at Clifton Hospital. Could you please provide your name, preferred doctor, and preferred date/time? Our specialists include Dr. Ahmed Khan (Cardiology), Dr. Sarah Malik (Orthopedics), Dr. Fatima Ali (Pediatrics), and Dr. Ayesha Khan (Gynecology).",
    "headache": "For mild headaches, try resting in a quiet, dark room, apply a cold or warm compress, stay hydrated, and consider over-the-counter pain relievers like acetaminophen. If headaches are severe, frequent, or accompanied by other symptoms, please see a doctor.",
    "emergency": "⚠️ This sounds like it could be a medical emergency. Please call 911 immediately or visit our emergency department at Clifton Hospital, Street 8, Shah Allah Ditta, Islamabad. Our emergency services are available 24/7.",
    "default": "I'm Dr. Assistant from Clifton Hospital. I can help you book appointments, provide guidance for common health issues, or direct you to emergency care if needed. How can I assist you today?"
}

def get_demo_response(user_input):
    """Generate demo response based on keywords"""
    user_lower = user_input.lower()
    
    # Check for emergency keywords
    emergency_keywords = ["chest pain", "can't breathe", "emergency", "severe pain", "bleeding"]
    if any(keyword in user_lower for keyword in emergency_keywords):
        return DEMO_MEDICAL_RESPONSES["emergency"]
    
    # Check for appointment keywords
    if any(word in user_lower for word in ["appointment", "book", "schedule", "doctor"]):
        return DEMO_MEDICAL_RESPONSES["appointment"]
    
    # Check for headache keywords
    if any(word in user_lower for word in ["headache", "head hurt", "migraine"]):
        return DEMO_MEDICAL_RESPONSES["headache"]
    
    # Default response
    return DEMO_MEDICAL_RESPONSES["default"]

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    """Process voice input from the web interface - Demo version"""
    try:
        # Get audio file from request
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({"error": "No audio file selected"}), 400
        
        # For demo purposes, simulate transcription
        user_input = "Hello, I would like to book an appointment with a doctor."
        
        # Get demo response
        assistant_response = get_demo_response(user_input)
        
        return jsonify({
            "user_input": user_input,
            "assistant_response": assistant_response,
            "audio_url": None,  # No TTS in demo
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        print(f"Error processing voice: {e}")
        return jsonify({"error": "Failed to process voice input"}), 500

@app.route('/chat_history')
def get_chat_history():
    """Get conversation history - Demo version"""
    return jsonify({"history": []})

@app.route('/clear_history', methods=['POST'])
def clear_chat_history():
    """Clear conversation history - Demo version"""
    return jsonify({"success": True})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Clifton Hospital Voice Assistant (Demo Mode)",
        "timestamp": datetime.now().isoformat(),
        "note": "Demo version - limited functionality"
    })

if __name__ == '__main__':
    print("🏥 Starting Clifton Hospital Voice Assistant (Demo Mode)...")
    print("📍 Hospital Location: Street 8, Shah Allah Ditta, Islamabad")
    print("🆘 Emergency: 911")
    print("🚀 Demo server ready at http://localhost:5000")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )

