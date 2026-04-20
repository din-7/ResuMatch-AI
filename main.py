from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services.embeddings import score_resume
from services.extractor import extract_text_from_pdf
from services.preprocess import clean_resume_text
from services.feedback import generate_feedback
import io

app = FastAPI(
    title="Resume Similarity Analyzer",
    description="Compares a resume PDF against a job description using sentence embeddings.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    resume: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., description="Job description text"),
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    try:
        contents = await resume.read()
        pdf_file = io.BytesIO(contents)
        score = score_resume(pdf_file, job_description)

        # Generate AI feedback using Groq
        pdf_file.seek(0)
        resume_text = extract_text_from_pdf(pdf_file)
        cleaned_resume = clean_resume_text(resume_text)
        cleaned_jd = clean_resume_text(job_description)

        try:
            feedback = generate_feedback(cleaned_resume, cleaned_jd, score)
        except Exception as fb_err:
            print(f"Feedback error: {fb_err}")
            feedback = None

        return {"similarity_score": score, "feedback": feedback}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
