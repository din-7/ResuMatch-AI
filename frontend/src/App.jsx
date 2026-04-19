import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [score, setScore] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setScore(null);
    setFeedback("");

    if (!resume) {
      setError("Please upload a resume PDF.");
      return;
    }
    if (!jobDescription.trim()) {
      setError("Please enter a job description.");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("resume", resume);
      formData.append("job_description", jobDescription);

      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Analysis failed.");
      }

      const data = await res.json();
      setScore(data.similarity_score);
      if (data.feedback) setFeedback(data.feedback);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (s) => {
    if (s >= 0.8) return "#22c55e";
    if (s >= 0.65) return "#3b82f6";
    if (s >= 0.5) return "#eab308";
    return "#ef4444";
  };

  const getScoreLabel = (s) => {
    if (s >= 0.8) return "Strong Match";
    if (s >= 0.65) return "Good Match";
    if (s >= 0.5) return "Moderate Match";
    return "Weak Match";
  };

  return (
    <div className="container">
      <h1>Resume Analyzer</h1>
      <p className="subtitle">
        Compare your resume against a job description using AI-powered
        similarity analysis.
      </p>

      <form onSubmit={handleSubmit} className="form">
        <div className="field">
          <label htmlFor="resume">Upload Resume (PDF)</label>
          <input
            id="resume"
            type="file"
            accept=".pdf"
            onChange={(e) => setResume(e.target.files[0])}
          />
          {resume && <span className="file-name">{resume.name}</span>}
        </div>

        <div className="field">
          <label htmlFor="job-description">Job Description</label>
          <textarea
            id="job-description"
            rows={8}
            placeholder="Paste the job description here..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {score !== null && (
        <div className="result">
          <div
            className="score"
            style={{ color: getScoreColor(score) }}
          >
            {(score * 100).toFixed(1)}%
          </div>
          <div
            className="label"
            style={{ color: getScoreColor(score) }}
          >
            {getScoreLabel(score)}
          </div>
        </div>
      )}

      {feedback && (
        <div className="feedback">
          <h2>AI Feedback</h2>
          <pre>{feedback}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
