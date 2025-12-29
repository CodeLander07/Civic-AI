from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    language: str = "en"

@app.post("/api/query")
def ask_ai(data: QueryRequest):
    return {
        "answer": f"Your question was: {data.question}",
        "language": data.language
    }
