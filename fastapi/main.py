from typing import Union

from fastapi import FastAPI

import random

import os
import openai

client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model='Meta-Llama-3.1-8B-Instruct',
    messages=[{"role":"system","content":"You are a helpful assistant"},{"role":"user","content":"Hello"}],
    temperature =  0.1,
    top_p = 0.1
)

print(response.choices[0].message.content)

app = FastAPI()

class Message:
    text: str
    user: str
    
    def __init__(self, text: str, user: str):
        self.text = text
        self.user = user

class Transcript:
    id: int
    messages: list
    
    def __init__(self):
        self.id = None
        self.messages = []
        
    def reset(self):
        self.id = random.randint(1000, 9999)
        self.messages = []
    
    def add_message(self, message: Message):
        self.messages.append(message)
        
    def get_transcript(self):
        return self.messages

transcript = Transcript()

@app.post("/start_transcript")
def start_transcript():
    # random id
    transcript.reset()
    return {"status": "started"}

@app.post("/transcript")
def add_transcript(transcript: str, user: str):
    transcript.add_message(
        Message(text=transcript, user=user)
    )
    return {"transcript": transcript}