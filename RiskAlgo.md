
# 📄 Risk Scoring Algorithm Documentation (`RiskAlgo.md`)

## ✅ Overview
This document explains how the **legal document risk scoring** works in the current pipeline.

The purpose of this algorithm is to:
- Analyze legal text using AI classification and summarization.
- Identify key legal categories and their associated risks.
- Compute a **risk score** (higher score = safer document).

---

## 🎯 Key Legal Categories Detected
The model classifies each paragraph into one of the following **categories**:
1. **Payment Terms**
2. **Liability & Indemnification**
3. **Termination**
4. **Confidentiality**
5. **Dispute Resolution**

---

## 🪄 How Risk Scoring Works

### 1. **Paragraph Processing**
- The text is split into paragraphs.
- Short lines or headings are skipped (less than 4 words or numbered headings).

### 2. **Classification & Summarization**
For each valid paragraph:
- The model classifies it into one of the categories.
- A summary is generated using a summarization model.

---

### 3. **Assigning Base Risk Points per Clause**
Each category has a **base risk score**:

| Category                     | Risk Level  | Base Risk Points |
|------------------------------|-------------|------------------|
| Termination                  | High Risk   | **30**           |
| Liability & Indemnification  | Medium Risk | **15**           |
| Confidentiality              | Medium Risk | **15**           |
| Dispute Resolution           | Medium Risk | **15**           |
| Payment Terms                | Low Risk    | **5**            |

---

### 4. **Keyword-Based Adjustments (Fine-Tuning)**
The algorithm then adjusts the base risk points based on **specific keywords** in the paragraph:

#### For **Termination** clauses:
- Mentions of `"with notice"` or `"prior notice"` → **–10** points (safer termination)
- Mentions of `"immediate termination"` → **+10** points (riskier termination)

#### For **Payment Terms**:
- Mentions of `"penalty"` or `"late fee"` → **+5** points (riskier payment terms)
- Mentions of `"due upon receipt"` → **+3** points (mild risk)

#### For **Confidentiality**:
- Mentions of `"no obligation"` or `"not liable"` → **–5** points (less restrictive confidentiality)

---

### 5. **Risk Score Calculation (Final Score)**
After assigning base points and adjustments:
- Total risk points for the document are summed.
- The **risk score** is computed:

```
Risk Score (%) = 100 - (Total Risk Points / (Number of Clauses × 30)) × 100
```

This formula normalizes the score:
- Higher score → safer document.
- Maximum possible per clause: **30** points.
- Minimum score capped at **0**, maximum at **100**.

---

### ✅ Example:
If a document has 5 clauses and 45 total risk points:
```
Risk Score = 100 - (45 / (5 × 30)) × 100
            = 100 - (45 / 150) × 100
            = 70/100 (safer)
```

---

## 📝 Notes:
- Risk scoring is **relative**, not legal advice.
- Higher scores suggest less risky contracts based on general terms.
- The scoring system is **tunable** for stricter or looser evaluations by changing:
  - Base risk points per category.
  - Keyword adjustments.
  - Max risk per clause.

---

## 🚀 Future Improvements Ideas:
- More nuanced keyword detection.
- Risk score caps for safer clauses.
- Legal expert review for fine-tuning risk logic.
