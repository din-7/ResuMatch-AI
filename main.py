from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.embeddings import score_resume
from services.extractor import extract_text_from_pdf
from services.preprocess import clean_resume_text
from services.feedback import generate_feedback
import io
import os

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

   
        pdf_file.seek(0)
        resume_text = extract_text_from_pdf(pdf_file)
        cleaned_resume = clean_resume_text(resume_text)
        cleaned_jd = clean_resume_text(job_description)

        try:
            feedback = generate_feedback(cleaned_resume, cleaned_jd, score)
        except Exception as fb_err:
            print(f"Bedrock feedback error: {fb_err}")
            feedback = None

        return {"similarity_score": score, "feedback": feedback}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# Serve React frontend 
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        return FileResponse(os.path.join(static_dir, "index.html"))
