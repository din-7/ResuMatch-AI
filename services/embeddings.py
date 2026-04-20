from sentence_transformers import SentenceTransformer
import numpy as np
from services.extractor import extract_text_from_pdf
from services.preprocess import clean_resume_text

model = SentenceTransformer("all-MiniLM-L6-v2")


def score_resume(resume_file, job_description: str) -> float:
    if not job_description or not job_description.strip():
        raise ValueError("Job description is empty.")

    try:
        raw_resume = extract_text_from_pdf(resume_file)
    except Exception as e:
        raise ValueError(f"Resume extraction failed: {str(e)}")

    cleaned_resume = clean_resume_text(raw_resume)
    cleaned_job = clean_resume_text(job_description)

    if not cleaned_resume:
        raise ValueError("Resume text is empty after cleaning.")

    embeddings = model.encode(
        [cleaned_resume, cleaned_job],
        normalize_embeddings=True
    )

    resume_emb, jd_emb = embeddings


    score = float(np.dot(resume_emb, jd_emb))

    return round(score, 4)