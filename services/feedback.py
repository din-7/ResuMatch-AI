import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

MODEL_ID = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"


def generate_feedback(resume_text: str, job_description: str, score: float) -> str:
    """Use Claude via Bedrock to explain the similarity score and suggest improvements."""

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

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }),
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]
