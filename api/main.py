from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional
import base64
import os
import json
from utils.helpers import cosine_similarity
from utils.helpers import chunk_text
from utils.embedder import get_embedding

# Load precomputed embeddings
with open("data/combined_embeddings.json", "r") as f:
    combined_data = json.load(f)

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str
    image: Optional[str] = None

class Link(BaseModel):
    url: str
    text: str

class AnswerResponse(BaseModel):
    answer: str
    links: List[Link]

@app.post("/", response_model=AnswerResponse)
async def answer_question(request: QuestionRequest):
    query_embedding = get_embedding(request.question)

    similarities = []
    for item in combined_data:
        similarity = cosine_similarity(query_embedding, item["embedding"])
        similarities.append((similarity, item))

    # Sort and get top 2 most relevant chunks
    top_chunks = sorted(similarities, reverse=True)[:2]

    top_links = []
    answer_parts = []

    for sim, item in top_chunks:
        link = {
            "url": item["url"],
            "text": item["text"][:150] + "..." if len(item["text"]) > 150 else item["text"]
        }
        top_links.append(link)
        answer_parts.append(item["text"])

    # Construct final answer
    full_answer = "\n\n".join(answer_parts)

    return {
        "answer": full_answer,
        "links": top_links
    }
