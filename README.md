# 📄 Legal Document Analyzer API

A sophisticated AI-powered API for analyzing legal documents and contracts. This application uses advanced machine learning models to classify legal clauses, assess risk levels, generate summaries, and provide legal insights.

## 🚀 Features

### Core Capabilities
- **Legal Text Classification**: Automatically categorizes legal clauses into 5 key categories
- **Risk Assessment**: Calculates comprehensive risk scores for legal documents
- **Smart Summarization**: Generates concise summaries of complex legal text
- **Key Findings Detection**: Identifies critical legal issues and potential risks
- **Legal Questions Generation**: Suggests important questions for legal review
- **API Key Authentication**: Secure access control for production use

### Legal Categories Analyzed
1. **Payment Terms** - Payment schedules, fees, and financial obligations
2. **Liability & Indemnification** - Responsibility and damage limitations
3. **Termination** - Contract termination conditions and procedures
4. **Confidentiality** - Information protection and non-disclosure terms
5. **Dispute Resolution** - Conflict resolution mechanisms and procedures

## 🏗️ Architecture

### Technology Stack
- **Backend Framework**: FastAPI (Python)
- **AI Models**: 
  - Hugging Face Transformers (BART models for classification and summarization)
  - Google Gemini 2.0 Flash (for legal question generation)
- **Authentication**: API Key-based security
- **Deployment**: Heroku-ready with Procfile

### Key Components
- `app.py` - FastAPI application with REST endpoints
- `pipeline.py` - Core AI analysis pipeline and risk scoring algorithm
- `requirements.txt` - Python dependencies
- `Procfile` - Heroku deployment configuration

## 📋 Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for optimal performance)
- Google Gemini API key
- Environment variables setup

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd pythonAi
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# API Keys for authentication (comma-separated)
API_KEYS=key1,key2,key3
```

### 4. Run the Application
```bash
# Development
uvicorn app:app --reload

# Production
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 🔌 API Usage

### Authentication
All API requests require an API key in the header:
```
api-key: your_api_key_here
```

### Endpoint: `/analyze`

**Method**: `POST`

**Request Body**:
```json
{
  "legal_text": "Your legal document text here..."
}
```

**Response**:
```json
{
  "full_summary": "Comprehensive summary of the legal document...",
  "risk_score": "85/100 (Higher scores indicate lower risk)",
  "categories": {
    "Payment Terms": {
      "risk_level": "Low Risk",
      "points": ["Clear payment schedule defined..."]
    },
    "Termination": {
      "risk_level": "High Risk", 
      "points": ["Broad termination rights..."]
    }
  },
  "key_findings": [
    {
      "title": "Broad Termination Clause",
      "description": "Agreement allows broad termination clauses...",
      "risk_level": "High",
      "icon": "🔴",
      "section": "Section 8.2"
    }
  ],
  "legal_questions": [
    "What notice period is required for termination?",
    "Are there any penalties for early termination?",
    "How are disputes resolved under this agreement?",
    "What happens to intellectual property after termination?"
  ]
}
```

## 🧠 Risk Scoring Algorithm

The application uses a sophisticated risk scoring system that:

### Base Risk Points by Category
| Category | Risk Level | Base Points |
|----------|------------|-------------|
| Termination | High Risk | 30 |
| Liability & Indemnification | Medium Risk | 15 |
| Confidentiality | Medium Risk | 15 |
| Dispute Resolution | Medium Risk | 15 |
| Payment Terms | Low Risk | 5 |

### Risk Adjustments
The algorithm applies keyword-based adjustments:
- **Termination**: "with notice" (-10), "immediate termination" (+10)
- **Payment Terms**: "penalty" (+5), "due upon receipt" (+3)
- **Confidentiality**: "no obligation" (-5)

### Final Score Calculation
```
Risk Score (%) = 100 - (Total Risk Points / (Number of Clauses × 30)) × 100
```

**Higher scores indicate safer documents.**

## 🚀 Deployment

### Heroku Deployment
1. Ensure `Procfile` is present (already included)
2. Set environment variables in Heroku dashboard
3. Deploy using Heroku CLI or GitHub integration

### Environment Variables for Production
```env
GEMINI_API_KEY=your_production_gemini_key
API_KEYS=production_key1,production_key2
PORT=8000
```

## 📊 Performance Considerations

### Model Loading
- Models are loaded once at startup for optimal performance
- GPU acceleration is utilized when available
- Text chunking prevents memory overflow for large documents

### Response Time
- Typical analysis: 5-15 seconds for standard legal documents
- Large documents (>10,000 words) may take longer
- Summarization is optimized for speed vs. quality balance

## 🔒 Security Features

- **API Key Authentication**: Required for all endpoints
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Graceful error responses without exposing internals
- **Rate Limiting**: Can be implemented at the deployment level

## 🧪 Testing

### Example Request
```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -H "api-key: your_api_key" \
  -d '{
    "legal_text": "This agreement is entered into between Party A and Party B. Payment terms are net 30 days. Either party may terminate this agreement with 30 days written notice."
  }'
```

## 📈 Monitoring & Logging

The application includes:
- Error logging for failed API calls
- Performance monitoring for model inference
- Input validation logging

## 🔮 Future Enhancements

### Planned Features
- **Multi-language Support**: Analysis in multiple languages
- **Document Comparison**: Compare multiple legal documents
- **Custom Risk Rules**: User-defined risk assessment criteria
- **Legal Precedent Integration**: Reference similar cases
- **Export Functionality**: PDF/Word document generation

### Technical Improvements
- **Caching**: Redis integration for repeated analyses
- **Async Processing**: Background job processing for large documents
- **Model Fine-tuning**: Custom models for specific legal domains
- **API Versioning**: Versioned endpoints for backward compatibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application provides AI-powered analysis for educational and informational purposes only. It is not a substitute for professional legal advice. Always consult with qualified legal professionals for actual legal matters.

## 📞 Support

For questions, issues, or contributions:
- Create an issue in the repository
- Contact the development team
- Review the documentation in `RiskAlgo.md` for technical details

---

**Built with ❤️ using FastAPI, Transformers, and Google Gemini** 