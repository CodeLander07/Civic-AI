from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # 🔥 MUST be called before using env vars

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}

class QueryRequest(BaseModel):
    question: str
    language: str = "en"

@app.post("/api/query")
def ask_ai(data: QueryRequest):
    return {
        "answer": f"Your question was: {data.question}",
        "language": data.language
    }
