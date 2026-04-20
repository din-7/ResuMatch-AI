# ResuMatch AI

A full-stack app that scores how well your resume matches a job description using NLP embeddings, then provides AI-powered feedback via Llama 3.3 on Groq.

## Live Demo

- **App:** https://resu-match-ai-five.vercel.app
- **API:** https://resumatch-ai-fd5l.onrender.com

## Tech Stack

- **Frontend:** React, Vite, CSS — hosted on Vercel
- **Backend:** Python, FastAPI, Uvicorn — hosted on Render
- **ML/NLP:** sentence-transformers (all-MiniLM-L6-v2), PyTorch (CPU), NumPy
- **AI Feedback:** Groq API, Llama 3.3 70B
- **Libraries:** pdfplumber, httpx, scikit-learn, SciPy

## How It Works

1. Upload a resume PDF and paste a job description
2. The backend extracts text from the PDF using pdfplumber and cleans it
3. Both texts are converted into 384-dimensional vectors using sentence-transformers
4. Cosine similarity (dot product of normalized embeddings) produces a match score
5. Llama 3.3 on Groq analyzes both texts and generates actionable feedback

## Score Tiers

| Score | Label | Color |
|-------|-------|-------|
| 80%+ | Strong Match | Green |
| 65-80% | Good Match | Blue |
| 50-65% | Moderate Match | Yellow |
| Below 50% | Weak Match | Red |

Note: Scores above 90% are rare. A resume and job description are fundamentally different document types — cosine similarity compares semantic meaning, not keyword overlap. A 65%+ is a strong match.

## Project Structure

```
├── main.py                  # FastAPI app (API routes, CORS, file size limit)
├── services/
│   ├── embeddings.py        # Model loading and similarity scoring
│   ├── extractor.py         # PDF text extraction
│   ├── preprocess.py        # Text cleaning and normalization
│   └── feedback.py          # Groq API integration for AI feedback
├── requirements.txt         # Python dependencies
├── render.yaml              # Render deployment config
└── frontend/
    ├── src/
    │   ├── App.jsx          # React UI
    │   ├── App.css          # Styling (dark theme)
    │   └── main.jsx         # Entry point
    ├── .env.example         # Environment variable template
    ├── index.html           # HTML shell
    ├── vite.config.js       # Vite build config
    └── package.json         # JS dependencies
```

## Running Locally

### Backend

```bash
python -m venv venv
source venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
export GROQ_API_KEY=your_groq_key_here
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # edit VITE_API_URL if needed
npm run dev
```

Open `http://localhost:5173` in your browser.

## Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `VITE_API_URL` | Vercel / `frontend/.env` | Backend API URL for the frontend |
| `GROQ_API_KEY` | Render / server env | Groq API key for AI feedback |

## API Endpoints

- `GET /health` — Health check
- `POST /analyze` — Upload resume PDF + job description, returns similarity score and AI feedback
- `GET /docs` — Auto-generated API documentation
