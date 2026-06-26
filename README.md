# Redrob Semantic Talent Graph UI

A highly polished Streamlit dashboard frontend for the **Semantic Talent Graph** hackathon project. This UI consumes a strict, pre-defined JSON API contract to retrieve, rank, and visually map engineering candidate profiles based on semantic search queries.

---

## 📂 Project Structure

The frontend workspace is organized as follows:

```
semantic-talent-graph-ui/
├── .gitignore            # Python version control exclusions
├── README.md             # Setup and running instructions
├── requirements.txt      # Project dependencies (Streamlit, Pandas, Requests)
├── mock_data.json        # Pre-defined API contract / mock dataset
└── frontend/
    ├── app.py            # Streamlit dashboard entry point
    └── components.py     # Custom UI rendering functions (candidate cards, metrics)
```

---

## 📄 The API Contract (`mock_data.json`)

The dashboard is decoupled from the backend ML matching engine. During local development, the UI loads `mock_data.json` to simulate the backend response structure.

```json
{
  "status": "success",
  "query": "Looking for an AI Engineer with backend integration skills",
  "processing_time_ms": 78,
  "total_candidates": 5000,
  "total_matches_found": 100,
  "top_candidates": [
    {
      "candidate_id": "CAND-8932",
      "rank": 1,
      "name": "Arjun Sharma",
      "match_score": 94.5,
      "experience_years": 2,
      "core_skills": ["Python", "FastAPI", "scikit-learn", "TensorFlow", "SQL"],
      "matched_skills": ["Python", "FastAPI", "SQL"],
      "reasoning": "Strong semantic match with the job description. Backend API development experience along with ML stack aligns well with the required profile."
    }
  ]
}
```

---

## ⚡ Setup & Local Execution

Follow these steps to run the Streamlit dashboard locally:

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
Install the required packages using pip:
```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit App
Run the Streamlit application from the root directory:
```bash
streamlit run frontend/app.py
```

The application will launch automatically in your default browser at:
**[http://localhost:8501](http://localhost:8501)**
