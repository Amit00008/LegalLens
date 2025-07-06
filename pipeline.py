from dotenv import load_dotenv
import os
from transformers import pipeline
import json
import re
import google.generativeai as genai

# Load Environment Variables
load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API (Your API key here - keep it secret!)
genai.configure(api_key=gemini_key)

# Load Gemini Model (Keep this global if calling multiple times)
gemini_model = genai.GenerativeModel('gemini-2.0-flash')

# Load Models (only once at app startup!)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0)
generator = pipeline("text-generation", model="gpt2", device=0)

categories = ["Payment Terms", "Liability & Indemnification", "Termination", "Confidentiality", "Dispute Resolution"]

KEY_FINDINGS_RULES = [
    {
        "label": "Broad Termination Clause",
        "keywords": ["terminate", "termination", "notice"],
        "risk_level": "High",
        "icon": "🔴",
        "section_hint": "Section 8.2",
        "custom_description": "Agreement allows broad termination clauses which may result in early contract cancellation."
    },
    {
        "label": "Limited Liability Cap",
        "keywords": ["liability", "limited liability", "liability cap"],
        "risk_level": "Medium",
        "icon": "🟡",
        "section_hint": "Section 12.1",
        "custom_description": "Liability limits are present, potentially capping damages recoverable under this agreement."
    },
    {
        "label": "Clear Payment Terms",
        "keywords": ["payment", "fee", "invoice"],
        "risk_level": "Low",
        "icon": "🟢",
        "section_hint": "Section 4",
        "custom_description": "Clear payment terms are defined, reducing payment-related ambiguities."
    },
    {
        "label": "IP Ownership Ambiguity",
        "keywords": ["intellectual property", "IP", "ownership"],
        "risk_level": "Medium",
        "icon": "🟡",
        "section_hint": "Section 9.3",
        "custom_description": "Intellectual Property (IP) ownership clauses may lack clarity, review is recommended."
    }
]

def extract_key_findings(paragraphs):
    key_findings = []
    for rule in KEY_FINDINGS_RULES:
        for para in paragraphs:
            if any(keyword in para.lower() for keyword in rule["keywords"]):
                key_findings.append({
                    "title": rule["label"],
                    "description": rule["custom_description"],
                    "risk_level": rule["risk_level"],
                    "icon": rule["icon"],
                    "section": rule["section_hint"]
                })
                break
    return key_findings


import re
import google.generativeai as genai  # assuming you use this lib for Gemini

def generate_legal_questions(legal_text):
    prompt = (
        "You are a legal expert. Read the following legal agreement carefully:\n\n"
        f"{legal_text}\n\n"
        "Suggest exactly 4 specific, practical questions that a lawyer should ask to improve this agreement.\n"
        "Only provide the questions as a numbered list. Do not include any answers, explanations, or extra text.\n\n"
        "Questions:"
    )

    try:
        # Gemini API Call
        response = gemini_model.generate_content(prompt)
        if not hasattr(response, "text") or not response.text.strip():
            raise ValueError("Empty or invalid response from Gemini API.")
        
        # Extract Questions and Clean
        questions_text = response.text.strip()
        questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
        questions = [re.sub(r'^[\s\-\d\.\)\:\/]+', '', q).replace('/', '').strip() for q in questions]
        
        return questions[:4]  # Limit to exactly 4 questions
    
    except Exception as e:
        print(f"[ERROR] Failed to generate legal questions: {e}")
        return ["Error generating legal questions. Please try again later."]


def analyze_legal_text(legal_text: str) -> dict:
    def chunk_text(text, max_chunk_words=150):
        words = text.split()
        return [" ".join(words[i:i+max_chunk_words]) for i in range(0, len(words), max_chunk_words)]

    legal_text_cleaned = re.sub(r'\n(\d+\.)', r' \1', legal_text)
    paragraphs = [p.strip() for p in legal_text_cleaned.split('\n') if p.strip()]

    results = []
    total_risk_points = 0
    clause_count = 0

    for paragraph in paragraphs:
        if len(paragraph.split()) < 4 or re.match(r'^\d+\. ', paragraph):
            continue

        classification = classifier(paragraph, categories)
        best_category = classification["labels"][0]
        score = classification["scores"][0]

        # ✅ Summarize only if long (Fast)
        if len(paragraph.split()) > 40:
            max_len = min(60, len(paragraph.split()) + 20)
            summary = summarizer(paragraph, max_length=max_len, min_length=10, do_sample=False)
            summary_text = summary[0]["summary_text"]
        else:
            summary_text = paragraph.strip()

        risk_level = "Unknown"
        base_risk_points = 0
        if best_category == "Termination":
            risk_level = "High Risk"
            base_risk_points = 30
        elif best_category == "Payment Terms":
            risk_level = "Low Risk"
            base_risk_points = 5
        elif best_category in ["Liability & Indemnification", "Confidentiality", "Dispute Resolution"]:
            risk_level = "Medium Risk"
            base_risk_points = 15

        paragraph_lower = paragraph.lower()
        adjust = 0

        if best_category == "Termination":
            if "with notice" in paragraph_lower or "prior notice" in paragraph_lower:
                adjust -= 10
            if "immediate termination" in paragraph_lower:
                adjust += 10

        if best_category == "Payment Terms":
            if "penalty" in paragraph_lower or "late fee" in paragraph_lower:
                adjust += 5
            if "due upon receipt" in paragraph_lower:
                adjust += 3

        if best_category == "Confidentiality":
            if "no obligation" in paragraph_lower or "not liable" in paragraph_lower:
                adjust -= 5

        risk_points = max(0, base_risk_points + adjust)
        total_risk_points += risk_points
        clause_count += 1

        results.append({
            "category": best_category,
            "risk_level": risk_level,
            "bullet_point": summary_text,
            "score": round(score, 2)
        })

    final_data = {}
    for result in results:
        cat = result["category"]
        if cat not in final_data:
            final_data[cat] = {"risk_level": result["risk_level"], "points": []}
        final_data[cat]["points"].append(result["bullet_point"])

    document_chunks = chunk_text(legal_text, max_chunk_words=200)
    full_summary = ""
    for chunk in document_chunks:
        summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
        full_summary += summary[0]["summary_text"] + " "

    lower_text = legal_text.lower()
    if "non-binding" in lower_text or "memorandum of understanding" in lower_text:
        total_risk_points *= 0.9

    if clause_count > 0:
        score_percent = round(100 - (total_risk_points / (clause_count * 30)) * 100)
    else:
        score_percent = 100

    risk_score = f"{score_percent}/100 (Higher scores indicate lower risk)"

    key_findings = extract_key_findings(paragraphs)
    legal_questions = generate_legal_questions(legal_text)

    return {
        "full_summary": full_summary.strip().replace("\n", " "),
        "risk_score": risk_score,
        "categories": final_data,
        "key_findings": key_findings,
        "legal_questions": legal_questions
    }
