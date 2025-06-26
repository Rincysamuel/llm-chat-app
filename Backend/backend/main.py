from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_API = "http://localhost:11434/api/chat"

class Message(BaseModel):
    model: str
    messages: list

@app.post("/chat")
async def chat_with_model(data: Message):
    try:
        response = requests.post(OLLAMA_API, json={
            "model": data.model,
            "messages": data.messages,
            "stream": False
        })
        return response.json()
    except Exception as e:
        return {"error": str(e)}
