
import io
from fastapi import FastAPI, File, UploadFile, Query, Body, Depends
from pymongo import MongoClient
from datetime import datetime,timezone
from bson.json_util import dumps
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
import sys

import requests
import pandas as pd
import numpy as np

app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://narrataive.vercel.app","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#model = SentenceTransformer("all-MiniLM-L6-v2")

_sentence_transformer_model_instance = None

def get_sentence_transformer_model():
    global _sentence_transformer_model_instance
    if _sentence_transformer_model_instance is None:
        print("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
        _sentence_transformer_model_instance = SentenceTransformer("all-MiniLM-L6-v2")
    return _sentence_transformer_model_instance



MONGODB_URI = os.getenv("MONGODB_URI")


client = MongoClient(MONGODB_URI)
db = client["narrative_db"] 
collection = db["reports"]


@app.get("/")
async def read_root():
    return {"Hello" : "World"}


@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...),st_model: SentenceTransformer = Depends(get_sentence_transformer_model) ):
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")

    try:
        df = pd.read_csv(io.StringIO(text),on_bad_lines='skip')
    except Exception as e:
        return {"error": f"Failed to parse CSV: {e}"}


    narrative = generate_narrative_gemini(df)
    embedding = st_model.encode(narrative).tolist()

    metadata = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "column_names": list(df.columns),
        "has_nulls": bool(df.isnull().values.any())
    }

    doc = {
        "filename": file.filename,
        "created_at": datetime.now(timezone.utc),
        "metadata": metadata,
        "narrative": narrative,
        "embedding": embedding
    }

    collection.insert_one(doc)

    return {"filename": file.filename, "narrative": narrative, "metadata": metadata}


@app.get("/reports/{report_id}")
async def get_report(report_id: str):
    from bson import ObjectId
    try:
        report=collection.find_one({"_id": ObjectId(report_id)})
        if not report:
            return {"error": "Report not found"}
        return json.loads(dumps(report))
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/search")
async def search_reports(filename: str=Query(None),from_date: str=Query(None),to_date: str=Query(None)):
    query={}

    if filename:
        query["filename"]={"$regex": filename,"$options": "i"}

    if from_date:
        query["created_at"]=query.get("created_at", {})
        query["created_at"]["$gte"]=datetime.fromisoformat(from_date)


    if to_date:
        query["created_at"]=query.get("created_at", {})
        query["created_at"]["$lte"]=datetime.fromisoformat(to_date)

    results=collection.find(query).sort("created_at",-1)
    return json.loads(dumps(results))


@app.get("/upload_history")
async def upload_history():
    reports=collection.find().sort("created_at",-1)
    return json.loads(dumps(reports))

class QueryRequest(BaseModel):
    query: str

@app.post("/vector_search")
async def vector_search(req: QueryRequest,st_model: SentenceTransformer = Depends(get_sentence_transformer_model)):
    q=req.query
    qy_embedding = st_model.encode(q).tolist()
    pipeline=[
        {
            "$search": {
                 "index": "default",
                 "knnBeta": {
                    "vector": qy_embedding,
                    "path": "embedding",
                    "k": 5
                }
            }
        },
        {"$project": {"filename": 1, "narrative": 1, "_id": 0}},
        {"$limit": 5}
    ]
    results=list(collection.aggregate(pipeline))
    return results



def generate_narrative_gemini(df: pd.DataFrame) -> str:
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
    You're a data analyst AI. Analyze the dataset below and provide a detailed, human-readable summary.

    Columns: {', '.join(df.columns)}
    Shape: {df.shape}
    Missing values present: {df.isnull().values.any()}
    Data types: {df.dtypes.to_dict()}
    First 5 rows:
    {df.head(5).to_string(index=False)}

    Include:
    - Type of data
    - Data quality (nulls, types)
    - Suggestions for visualization
    - Insights (trends, outliers, correlations)
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[ERROR] Gemini response: {e}"
