from fastapi import FastAPI, HTTPException, Request, Header
from pydantic import BaseModel
from pipeline import analyze_legal_text
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

#  Read API Keys from .env
API_KEYS = os.getenv("API_KEYS", "").split(",")

app = FastAPI(title="Legal Document Analyzer API")



# Request Body
class LegalTextRequest(BaseModel):
    legal_text: str

# API Route with API Key check
@app.post("/analyze")
async def analyze(
    request: LegalTextRequest, 
    api_key: str = Header(None)  # Read from Header 'api-key'
):
    # Check API Key
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key.")
    
    if not request.legal_text.strip():
        raise HTTPException(status_code=400, detail="Empty legal text provided.")
    
    result = analyze_legal_text(request.legal_text)
    return result