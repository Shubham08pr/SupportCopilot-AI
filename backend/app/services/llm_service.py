from openai import OpenAI
from backend.app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(query: str, context: str):
    prompt = f"""
You are a helpful customer support assistant.

Answer ONLY using the context below.
If answer is not found, say "I don't know".

Context:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

def evaluate_response(query: str, answer: str, context: str):
    prompt = f"""
You are evaluating an AI customer support response.

Question:
{query}

Context:
{context}

Answer:
{answer}

Rate the answer confidence from 0 to 1.

Rules:
- 1.0 = completely correct and grounded
- 0.7 = mostly correct
- 0.5 = partially correct
- 0.2 = weak/confused
- 0.0 = incorrect or hallucinated

Return ONLY the number.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    score_text = response.choices[0].message.content.strip()

    try:
        return float(score_text)
    except:
        return 0.5