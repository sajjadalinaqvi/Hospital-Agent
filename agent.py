# agent.py
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from medical_knowledge import search_medical_knowledge
from groq import Groq

from memory import load_history

# Load environment variables
load_dotenv()

# === Environment Variables ===
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_index_name = os.getenv("PINECONE_INDEX")
pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Pinecone connection
try:
    pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)
    index = pc.Index(pinecone_index_name)
    print("✅ Pinecone initialized.")
except Exception as e:
    print(f"[❌ Pinecone Initialization Error] {e}")
    index = None  # Set index to None if initialization fails

# === Initialize Groq ===
try:
    groq_client = Groq(api_key=groq_api_key)
    print("✅ Groq client initialized.")
except Exception as e:
    print(f"[❌ Groq Initialization Error] {e}")
    groq_client = None

# Load SentenceTransformer model (384-dimensional output)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Clifton Hospital system prompt
SYSTEM_PROMPT = """You are Dr. Assistant, a medical AI assistant for Clifton Hospital located at Street 8, Shah Allah Ditta, Islamabad. Your primary responsibilities are:

1. **Appointment Booking**: Help patients book appointments with our specialists including:
   - Dr. Ahmed Khan (Cardiology)
   - Dr. Sarah Malik (Orthopedics) 
   - Dr. Fatima Ali (Pediatrics)
   - Dr. Ayesha Khan (Gynecology)
   - General Medicine doctors

2. **Medical Guidance**: Provide guidance for common health issues like:
   - Common cold, mild fever, headaches
   - Minor cuts, stomach upset, mild allergies
   - General wellness and preventive care advice

3. **Emergency Referral**: For serious conditions, IMMEDIATELY refer to emergency services or doctors:
   - Chest pain, difficulty breathing, severe abdominal pain
   - High fever with concerning symptoms, severe allergic reactions
   - Head injuries, stroke symptoms, severe bleeding
   - Any life-threatening emergency

4. **Hospital Information**: Provide information about our services, location, and emergency contact (911).

IMPORTANT GUIDELINES:
- Always be empathetic and professional
- For serious symptoms, prioritize patient safety and recommend immediate medical attention
- For appointment booking, collect: patient name, preferred doctor, preferred date/time, contact information
- Never provide specific medical diagnoses - only general guidance
- Always mention that you're an AI assistant and not a replacement for professional medical care
- Be concise but thorough in your responses

Remember: Patient safety is the top priority. When in doubt, refer to a doctor or emergency services."""

# === Context Search ===
def search_context(query, top_k=3):
    if index is None:
        print("[⚠️ Pinecone not initialized. Skipping context search.]")
        return ""

    try:
        # Get query embedding
        embedding = model.encode(query).tolist()

        # Query Pinecone
        results = index.query(vector=embedding, top_k=top_k, include_metadata=True)
        general_context = "\n".join([match["metadata"]["text"] for match in results.get("matches", [])])

        # Medical knowledge context
        medical_context = search_medical_knowledge(query, top_k=2)
        medical_text = "\n".join([item["text"] for item in medical_context])

        # Combine context
        context_parts = []
        if medical_text:
            context_parts.append(f"Medical Knowledge:\n{medical_text}")
        if general_context:
            context_parts.append(f"Additional Context:\n{general_context}")

        return "\n\n".join(context_parts).strip()

    except Exception as e:
        print(f"[❌ Context Search Error] {e}")
        return ""


def determine_urgency(query):
    """Determine if the query indicates a medical emergency"""
    emergency_keywords = [
        "chest pain", "can't breathe", "difficulty breathing", "severe pain",
        "bleeding heavily", "unconscious", "stroke", "heart attack",
        "severe allergic reaction", "anaphylaxis", "head injury",
        "high fever", "severe headache", "can't move", "emergency"
    ]

    query_lower = query.lower()
    for keyword in emergency_keywords:
        if keyword in query_lower:
            return True
    return False


def get_response(history):
    if groq_client is None:
        print("[⚠️ Groq client not initialized. Cannot get response.]")
        return "I'm sorry, I'm currently unable to connect to my knowledge base. Please try again later or call 911 for emergencies."

    try:
        # Get the latest user message
        user_message = next((msg["content"] for msg in reversed(history) if msg["role"] == "user"), "")

        # Check for emergency situations
        is_urgent = determine_urgency(user_message)

        # Search for relevant context
        context = search_context(user_message)

        # Prepare messages for Groq API
        messages = load_history()
        messages.append({"role": "system", "content": SYSTEM_PROMPT})

        if context:
            messages.append({"role": "system", "content": f"Relevant Information:\n{context}"})

        if is_urgent:
            messages.append({"role": "system",
                             "content": "⚠️ URGENT: This appears to be a medical emergency. Prioritize immediate medical attention in your response."})

            # Add conversation history
        messages.extend(history)

        # Send to Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",  # You can choose a different model if needed
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )

        assistant_response = chat_completion.choices[0].message.content
        return assistant_response

    except Exception as e:
        print(f"[❌ Groq API Error] {e}")
        return "I'm experiencing technical difficulties. For urgent medical matters, please call 911 or visit Clifton Hospital emergency department immediately."


def format_appointment_request(patient_info):
    """Format appointment booking request"""
    return f"""
    📋 APPOINTMENT REQUEST SUMMARY:

    Patient Name: {patient_info.get("name", "Not provided")}
    Preferred Doctor: {patient_info.get("doctor", "Not specified")}
    Preferred Date: {patient_info.get("date", "Not specified")}
    Preferred Time: {patient_info.get("time", "Not specified")}
    Contact: {patient_info.get("contact", "Not provided")}
    Reason: {patient_info.get("reason", "Not specified")}

    I'll help you book this appointment. Our reception team will contact you within 24 hours to confirm the details.

    For urgent matters, please call our emergency line at 911 or visit Clifton Hospital directly at Street 8, Shah Allah Ditta, Islamabad.
    """