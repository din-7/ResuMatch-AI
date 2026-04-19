# Resume-Description Similarity Analyzer

A full-stack app that scores how well your resume matches a job description using NLP embeddings, then provides AI-powered feedback via Claude on Amazon Bedrock.

## Tech Stack

- **Frontend:** React, Vite
- **Backend:** Python, FastAPI, Uvicorn
- **ML/NLP:** sentence-transformers (all-mpnet-base-v2), PyTorch, NumPy
- **AI:** Amazon Bedrock, Claude Sonnet 4.5
- **Cloud:** AWS EC2, EBS, Security Groups, systemd
- **Libraries:** pdfplumber, boto3, scikit-learn, SciPy

## How It Works

1. Upload a resume PDF and paste a job description
2. The backend extracts text from the PDF and cleans it
3. Both texts are converted into 768-dimensional vectors using sentence-transformers
4. Cosine similarity (dot product of normalized embeddings) produces a match score
5. Claude on Bedrock analyzes both texts and generates actionable feedback

## Score Tiers

| Score | Label | Color |
|-------|-------|-------|
| 80%+  | Strong Match | Green |
| 65-80% | Good Match | Blue |
| 50-65% | Moderate Match | Yellow |
| Below 50% | Weak Match | Red |

## Project Structure

```
├── main.py                  # FastAPI app (API routes, CORS, static serving)
├── services/
│   ├── embeddings.py        # Model loading and similarity scoring
│   ├── extractor.py         # PDF text extraction
│   ├── preprocess.py        # Text cleaning and normalization
│   └── feedback.py          # Claude via Bedrock integration
├── resume_api.service       # systemd service for EC2 deployment
├── requirements.txt         # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx          # React UI
    │   ├── App.css          # Styling
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

## Deploying to EC2

1. Launch a `t3.medium` Ubuntu 22.04 instance with 20 GB disk
2. Open ports 22 (SSH) and 8000 (API) in the security group
3. Upload code via `scp` and install dependencies (use CPU-only PyTorch)
4. Create `/home/ubuntu/.env` with AWS credentials for Bedrock access
5. Copy `resume_api.service` to `/etc/systemd/system/` and enable it

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now resume_api
```

## Environment Variables

| Variable | Where | Purpose |
|----------|-------|---------|
| `VITE_API_URL` | `frontend/.env` | Backend API URL for the frontend |
| `AWS_ACCESS_KEY_ID` | Server `.env` | AWS credentials for Bedrock |
| `AWS_SECRET_ACCESS_KEY` | Server `.env` | AWS credentials for Bedrock |
| `AWS_SESSION_TOKEN` | Server `.env` | AWS session token (if using temporary creds) |
| `AWS_DEFAULT_REGION` | Server `.env` | AWS region (us-west-2) |

## API Endpoints

- `GET /health` — Health check
- `POST /analyze` — Upload resume PDF + job description, returns similarity score and AI feedback
- `GET /docs` — Auto-generated API documentation
