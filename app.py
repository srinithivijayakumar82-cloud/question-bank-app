from test_question_gen import generate_questions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class question(BaseModel):
    content: str
    difficulty: str
    num_questions: int

@app.post("/generate_questions_endpoint")
def generate_questions_endpoint(request: question):
    return generate_questions(content=request.content, difficulty=request.difficulty, num_questions=request.num_questions)