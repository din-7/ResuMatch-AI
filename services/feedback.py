import os
import httpx
import json

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_feedback(resume_text: str, job_description: str, score: float) -> str:
    """Use Groq (Llama 3.3 70B) to explain the similarity score and suggest improvements."""

    if not GROQ_API_KEY:
        return None

    prompt = f"""You are a career coach. A candidate's resume was compared against a job description
using NLP embeddings and received a similarity score of {score:.0%}.

Resume text:
{resume_text[:3000]}

Job description:
{job_description[:2000]}

Provide a brief, actionable analysis:
1. Why the score is what it is (2-3 sentences)
2. Top 3 specific suggestions to improve the resume for this role
3. Key skills or keywords from the job description that are missing from the resume

Keep it concise and practical. No fluff."""

    response = httpx.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024,
        },
        timeout=30,
    )

    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
