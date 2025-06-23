# NarratAIve - Your AI-Powered Data Whisperer

### TL;DR
Upload your dataset. Get a smart summary. Get instant insights.  
No more "what am I even looking at?" moments.

---

## What It Does

- Upload any CSV dataset
- AI generates a natural-language report:
  - Data types, missing values
  - Suggestions for cleaning and visualizing
  - Potential trends and insights
- All summaries are stored in MongoDB
- Use **natural language search** (vector search!) to retrieve previous reports

---

## How It Works

-  **Gemini Pro** handles the AI analysis
-  **SentenceTransformers** encodes the narratives
-  **MongoDB Atlas** stores everything (with vector search)
-  **FastAPI** backend
-  **React + Vite** frontend
-  **Vector search** for querying insights

---

## Use Case

Perfect for:
- Data analysts doing EDA
- Hackathoners prototyping fast
- Anyone scared of raw CSVs

---


## Tech Stack

| Layer         | Tech                          |
|---------------|-------------------------------|
| Frontend      | React (Vite)                  |
| Backend       | FastAPI (Python)              |
| - AI Model    | Gemini API + MiniLM Embedding |
| - Vector DB   | MongoDB Atlas                 |

---

##  Example Usage

**Upload**: `diabetes.csv`  
**AI says**: "Looks like glucose level strongly correlates with diabetes outcome. Try a scatterplot of Glucose vs Outcome."

**Search**: "Titanic survival rate"  
**Results**: Auto-suggested insights from `titanic.csv`, including survival by gender, age, and class.

---

## Setup (Local)

```bash
git clone https://github.com/GnautSpace/NarratAIve
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
---
```bash
cd frontend
npm install
npm run dev
```

Live Demo
[NarratAIve](https://narrataive.vercel.app) – Hosted on Vercel + Railway

## Acknowledgements
Thanks to:
- Gemini for not hallucinating (too much)
- MongoDB Atlas for free vector search
- Hackathon deadlines for adrenaline

### AI in Action Google Cloud Hackathon project 
