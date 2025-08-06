# Hospital Voice Assistant

A modern, AI-powered voice assistant for Clifton Hospital that provides medical guidance, appointment booking, and emergency referrals. Built with real-time voice processing, barge-in interruption, and a beautiful modern UI.

## 🏥 Features

### Core Functionality
- **Always Listening**: Continuous voice recognition without hold-to-speak button
- **Barge-in Interruption**: Users can interrupt the agent while it's speaking
- **Real-time Processing**: Fast response times with optimized TTS
- **Medical Context**: Specialized knowledge base for healthcare guidance
- **Appointment Booking**: Help patients schedule appointments with doctors
- **Emergency Detection**: Automatic detection and referral for serious conditions

### Modern UI
- **Chat Interface**: Modern chat-like interface similar to ChatGPT
- **Sidebar Navigation**: Chat history and conversation management
- **Light/Dark Themes**: Toggle between light and dark modes
- **Responsive Design**: Works on desktop and mobile devices
- **Voice Indicators**: Visual feedback for listening and speaking states

### Medical Capabilities
- **Common Health Issues**: Guidance for cold, fever, headaches, minor injuries
- **Emergency Referral**: Immediate referral for serious conditions
- **Specialist Booking**: Appointments with cardiology, orthopedics, pediatrics, gynecology
- **Hospital Information**: Location, services, and contact information

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js (for any additional frontend tools)
- Pinecone account and API key
- Groq API key for LLM
- Microphone access in browser

### Installation

1. **Clone and Setup**
   ```bash
   cd Clinic-agent
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys:
   # - PINECONE_API_KEY
   # - GROQ_API_KEY
   # - Other Pinecone settings
   ```

3. **Initialize Medical Knowledge**
   ```bash
   python medical_knowledge.py
   ```

4. **Start the Server**
   ```bash
   python run_server.py
   ```

5. **Access the Application**
   Open http://localhost:5000 in your browser

## 🔧 Configuration

### Environment Variables
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_INDEX`: Pinecone index name (default: clinic-embeddings)
- `PINECONE_HOST`: Pinecone host URL
- `PINECONE_REGION`: Pinecone region
- `API_URL`: Groq API endpoint for LLM
- `GROQ_API_KEY`: Your Groq API key

### Medical Knowledge
The system includes a comprehensive medical knowledge base covering:
- Hospital information and services
- Common health issues and guidance
- Emergency conditions and referrals
- Specialist information and booking

## 🏗️ Architecture

### Backend Components
- **Flask Server** (`run_server.py`): Web server and API endpoints
- **Voice Processing** (`stt.py`, `listener.py`): Speech-to-text and continuous listening
- **TTS Engine** (`tts.py`): Text-to-speech with Coqui TTS
- **AI Agent** (`agent.py`): Medical AI with context awareness
- **Knowledge Base** (`medical_knowledge.py`): Medical information and embeddings
- **Memory System** (`memory.py`): Conversation history management

### Frontend Components
- **Modern UI** (`templates/index.html`): Chat interface with sidebar
- **Responsive CSS** (`static/style.css`): Light/dark themes and animations
- **Interactive JS** (`static/script.js`): Voice controls and real-time updates

### Key Technologies
- **Speech Recognition**: OpenAI Whisper
- **Text-to-Speech**: Coqui TTS (human-like voices)
- **Embeddings**: Sentence Transformers + Pinecone
- **LLM**: Groq API for fast inference
- **Frontend**: Modern HTML5/CSS3/JavaScript

## 🎯 Usage

### Voice Interaction
1. **Start Conversation**: The agent is always listening
2. **Speak Naturally**: Just talk - no button pressing needed
3. **Interrupt Anytime**: Speak while the agent is talking to interrupt
4. **Get Responses**: Immediate audio and text responses

### Chat Management
- **New Chat**: Click "New Conversation" to start fresh
- **Chat History**: View previous conversations in sidebar
- **Theme Toggle**: Switch between light and dark modes
- **Settings**: Adjust voice sensitivity and response speed

### Medical Assistance
- **Common Issues**: Get guidance for cold, fever, headaches
- **Appointments**: Book with specialists (cardiology, orthopedics, etc.)
- **Emergencies**: Automatic detection and immediate referral
- **Hospital Info**: Location, services, and contact details

## 🏥 Hospital Information

**Clifton Hospital**
- **Address**: Street 8, Shah Allah Ditta, Islamabad
- **Emergency**: 911
- **Services**: Emergency care, general medicine, surgery, pediatrics, gynecology
- **Specialists Available**:
  - Dr. Ahmed Khan (Cardiology)
  - Dr. Sarah Malik (Orthopedics)
  - Dr. Fatima Ali (Pediatrics)
  - Dr. Ayesha Khan (Gynecology)

## 🔒 Safety Features

### Emergency Detection
The system automatically detects emergency keywords and prioritizes immediate medical attention:
- Chest pain, difficulty breathing
- Severe injuries, heavy bleeding
- Stroke symptoms, loss of consciousness
- Severe allergic reactions
- High fever with concerning symptoms

### Medical Disclaimers
- AI assistant is not a replacement for professional medical care
- Always consult healthcare providers for serious conditions
- Emergency situations require immediate medical attention
- System provides guidance, not medical diagnoses

## 🛠️ Development

### Project Structure
```
Clinic-agent/
├── agent.py              # AI agent with medical context
├── stt.py                # Speech-to-text processing
├── tts.py                # Text-to-speech generation
├── listener.py           # Continuous listening
├── interrupt.py          # Barge-in interruption
├── memory.py             # Conversation memory
├── medical_knowledge.py  # Medical knowledge base
├── run_server.py         # Flask web server
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── style.css         # Modern UI styles
    └── script.js         # Interactive functionality
```

### Key Improvements Made
1. **Removed Hold-to-Speak**: Now always listening
2. **Added Barge-in**: Interrupt capability during TTS
3. **Faster TTS**: Optimized with Coqui TTS
4. **Modern UI**: ChatGPT-like interface with themes
5. **Medical Context**: Specialized healthcare knowledge
6. **Real-time Processing**: Immediate response system

### API Endpoints
- `GET /`: Main chat interface
- `POST /process_voice`: Process voice input
- `GET /audio/<filename>`: Serve TTS audio files
- `GET /chat_history`: Get conversation history
- `POST /clear_history`: Clear chat history
- `GET /health`: Health check endpoint

## 📱 Browser Support
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers with microphone support

## 🔧 Troubleshooting

### Common Issues
1. **Microphone Access**: Ensure browser has microphone permissions
2. **API Keys**: Verify Pinecone and Groq API keys are correct
3. **Dependencies**: Install all requirements with `pip install -r requirements.txt`
4. **Port Conflicts**: Change port in `run_server.py` if 5000 is occupied

### Performance Tips
- Use Chrome for best WebRTC support
- Ensure stable internet connection for API calls
- Close other audio applications to avoid conflicts
- Use headphones to prevent audio feedback


## 🤝 Support
For technical support or medical emergencies:
- **Emergency**: 911
- **Hospital**: Clifton Hospital, Street 8, Islamabad
- **Technical Issues**: Contact development team

---

**⚠️ Important**: This AI assistant is for guidance only and not a replacement for professional medical care. Always consult healthcare providers for serious medical conditions.

