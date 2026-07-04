"""
Step 1: Standalone script to test the core idea.
No FastAPI, no React yet — just prove the AI call works correctly.
Run this first. Once it works, we wrap it in a web API (Step 2).
"""

import json
import os
from groq import Groq

API_KEY = os.environ.get("GROQ_API_KEY", "groq_api_key") 

if API_KEY == "groq_api_key":
    raise ValueError("Open this file and replace API_KEY with your actual Groq key on line 8.")

client = Groq(api_key=API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"


def generate_questions(content: str, difficulty: str, num_questions: int) -> list:
    """
    Takes study content + user preferences, returns a list of question dicts.
    This function is the entire 'brain' of your app.
    """
    prompt = f"""You are a question bank generator for a student studying a learning unit.

Based on the content below, generate exactly {num_questions} questions at {difficulty} difficulty level.

Content:
\"\"\"
{content}
\"\"\"

Return ONLY a valid JSON array, no markdown formatting, no extra text. Each item must have this exact structure:
{{"question": "...", "difficulty": "{difficulty}", "answer": "..."}}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    raw_text = response.choices[0].message.content.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        questions = json.loads(raw_text)
        return questions
    except json.JSONDecodeError:
        print("Could not parse JSON. Raw response was:")
        print(raw_text)
        return []


if __name__ == "__main__":

    sample_content = """
    Photosynthesis is the process by which green plants, algae, and some bacteria
    convert light energy into chemical energy. It occurs mainly in the chloroplasts
    of plant cells, using chlorophyll to absorb sunlight. The overall reaction
    converts carbon dioxide and water into glucose and oxygen. Photosynthesis has
    two main stages: the light-dependent reactions, which occur in the thylakoid
    membrane, and the light-independent reactions (Calvin cycle), which occur in
    the stroma.
    """

    results = generate_questions(
        content=sample_content,
        difficulty="medium",
        num_questions=3
    )

    print(f"\nGenerated {len(results)} questions:\n")
    for i, q in enumerate(results, 1):
        print(f"{i}. {q.get('question')}")
        print(f"   Answer: {q.get('answer')}\n")
