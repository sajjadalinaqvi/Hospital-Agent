# medical_knowledge.py
import uuid
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone and embedding model
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))
model = SentenceTransformer("all-MiniLM-L6-v2")

# Medical knowledge base for Clifton Hospital
MEDICAL_KNOWLEDGE = [
    # Hospital Information
    {
        "text": "Clifton Hospital is located at Street 8, Shah Allah Ditta, Islamabad. We provide comprehensive healthcare services including emergency care, general medicine, surgery, pediatrics, gynecology, and specialized treatments.",
        "category": "hospital_info"
    },
    {
        "text": "Clifton Hospital emergency services are available 24/7. For emergencies, call 911 or visit our emergency department immediately. Our emergency team is equipped to handle all types of medical emergencies.",
        "category": "emergency"
    },
    {
        "text": "To book an appointment at Clifton Hospital, you can call our reception or use our online booking system. We have specialists available for cardiology, neurology, orthopedics, dermatology, and internal medicine.",
        "category": "appointments"
    },
    
    # Common Health Issues - Guidance
    {
        "text": "For common cold symptoms like runny nose, sneezing, and mild cough: Rest, drink plenty of fluids, use saline nasal drops, and take over-the-counter pain relievers if needed. If symptoms persist for more than 7 days or worsen, consult a doctor.",
        "category": "common_cold"
    },
    {
        "text": "For mild headaches: Try rest in a quiet, dark room, apply cold or warm compress, stay hydrated, and take over-the-counter pain relievers like acetaminophen or ibuprofen. If headaches are severe, frequent, or accompanied by other symptoms, see a doctor.",
        "category": "headache"
    },
    {
        "text": "For minor cuts and scrapes: Clean the wound with water, apply antibiotic ointment, cover with a bandage, and keep it clean and dry. Change the bandage daily. Seek medical attention if signs of infection appear.",
        "category": "minor_wounds"
    },
    {
        "text": "For mild stomach upset or indigestion: Eat bland foods like rice, bananas, toast. Avoid spicy, fatty, or acidic foods. Stay hydrated with clear fluids. If symptoms persist for more than 24 hours or include severe pain, see a doctor.",
        "category": "stomach_upset"
    },
    {
        "text": "For mild fever (under 101°F): Rest, drink plenty of fluids, take acetaminophen or ibuprofen as directed. Monitor temperature regularly. If fever exceeds 103°F, persists for more than 3 days, or is accompanied by severe symptoms, seek medical attention.",
        "category": "mild_fever"
    },
    {
        "text": "For minor allergic reactions (mild rash, itching): Avoid the allergen, apply cool compresses, use antihistamines like Benadryl. If symptoms worsen or include difficulty breathing, seek immediate medical attention.",
        "category": "mild_allergies"
    },
    
    # Serious Conditions - Refer to Doctor
    {
        "text": "SERIOUS: Chest pain, especially if accompanied by shortness of breath, nausea, or pain radiating to arm or jaw, requires immediate medical attention. This could indicate a heart attack. Call emergency services immediately.",
        "category": "serious_chest_pain"
    },
    {
        "text": "SERIOUS: Severe abdominal pain, especially if sudden onset, accompanied by vomiting, fever, or inability to pass gas, requires immediate medical evaluation. This could indicate appendicitis or other serious conditions.",
        "category": "serious_abdominal_pain"
    },
    {
        "text": "SERIOUS: Difficulty breathing, wheezing, or shortness of breath requires immediate medical attention. This could indicate asthma, pneumonia, or other respiratory emergencies.",
        "category": "breathing_difficulty"
    },
    {
        "text": "SERIOUS: High fever (over 103°F), especially with stiff neck, severe headache, rash, or confusion, requires immediate medical attention. This could indicate meningitis or other serious infections.",
        "category": "high_fever"
    },
    {
        "text": "SERIOUS: Severe allergic reactions (anaphylaxis) with difficulty breathing, swelling of face/throat, rapid pulse, or dizziness require immediate emergency treatment. Use EpiPen if available and call 911.",
        "category": "severe_allergic_reaction"
    },
    {
        "text": "SERIOUS: Any head injury with loss of consciousness, confusion, persistent vomiting, or severe headache requires immediate medical evaluation. Do not ignore head injuries.",
        "category": "head_injury"
    },
    {
        "text": "SERIOUS: Severe burns, deep cuts requiring stitches, or any injury with heavy bleeding requires immediate medical attention. Apply pressure to bleeding wounds and seek emergency care.",
        "category": "serious_injuries"
    },
    {
        "text": "SERIOUS: Signs of stroke including sudden weakness, numbness, confusion, trouble speaking, or severe headache require immediate emergency treatment. Time is critical - call 911 immediately.",
        "category": "stroke_symptoms"
    },
    
    # Preventive Care
    {
        "text": "Regular health checkups at Clifton Hospital include blood pressure monitoring, cholesterol screening, diabetes screening, and cancer screenings. We recommend annual checkups for adults and more frequent visits for those with chronic conditions.",
        "category": "preventive_care"
    },
    {
        "text": "Vaccination services at Clifton Hospital include routine immunizations for children and adults, flu shots, COVID-19 vaccines, and travel vaccines. Keep your vaccination records up to date.",
        "category": "vaccinations"
    },
    
    # Specialist Referrals
    {
        "text": "Our cardiology department at Clifton Hospital specializes in heart conditions, high blood pressure, chest pain evaluation, and cardiac procedures. Dr. Ahmed Khan is our lead cardiologist.",
        "category": "cardiology"
    },
    {
        "text": "Our orthopedic department handles bone fractures, joint problems, sports injuries, and arthritis. Dr. Sarah Malik specializes in orthopedic surgery and joint replacement.",
        "category": "orthopedics"
    },
    {
        "text": "Our pediatrics department provides comprehensive care for children from birth to 18 years. Dr. Fatima Ali specializes in child health, growth monitoring, and pediatric emergencies.",
        "category": "pediatrics"
    },
    {
        "text": "Our gynecology department offers women's health services including pregnancy care, reproductive health, and gynecological procedures. Dr. Ayesha Khan is our senior gynecologist.",
        "category": "gynecology"
    }
]

def load_medical_knowledge():
    """Load medical knowledge into Pinecone vector database"""
    print("Loading medical knowledge into Pinecone...")
    
    for knowledge in MEDICAL_KNOWLEDGE:
        # Generate embedding
        embedding = model.encode(knowledge["text"]).tolist()
        
        # Create unique ID
        knowledge_id = str(uuid.uuid4())
        
        # Upsert to Pinecone
        index.upsert([
            (knowledge_id, embedding, {
                "text": knowledge["text"],
                "category": knowledge["category"],
                "source": "clifton_hospital_knowledge"
            })
        ])
    
    print(f"✅ Successfully loaded {len(MEDICAL_KNOWLEDGE)} medical knowledge entries into Pinecone")

def search_medical_knowledge(query, top_k=3):
    """Search medical knowledge base for relevant information"""
    try:
        # Generate query embedding
        query_embedding = model.encode(query).tolist()
        
        # Search in Pinecone
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter={"source": "clifton_hospital_knowledge"}
        )
        
        # Extract relevant information
        relevant_info = []
        for match in results["matches"]:
            if match["score"] > 0.7:  # Only include high-confidence matches
                relevant_info.append({
                    "text": match["metadata"]["text"],
                    "category": match["metadata"]["category"],
                    "confidence": match["score"]
                })
        
        return relevant_info
    
    except Exception as e:
        print(f"Error searching medical knowledge: {e}")
        return []

if __name__ == "__main__":
    load_medical_knowledge()

