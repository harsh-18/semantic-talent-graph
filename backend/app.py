from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Semantic Talent Graph API",
    version="1.0"
)


# --------------------------
# Request Model
# --------------------------

class SearchRequest(BaseModel):
    query: str


# --------------------------
# Root Endpoint
# --------------------------

@app.get("/")
def home():
    return {
        "message": "Semantic Talent Graph Backend Running!"
    }


# --------------------------
# Search Endpoint
# --------------------------

@app.post("/search")
def search_candidates(request: SearchRequest):

    dummy_response = {
        "status": "success",
        "query": request.query,
        "total_matches_found": 3,
        "top_candidates": [
            {
                "candidate_id": "CAND_000001",
                "name": "Dummy Candidate",
                "match_score": 92.5,
                "behavior_score": 88.1,
                "honeypot": False,
                "core_skills": [
                    "Python",
                    "FastAPI",
                    "SQL"
                ],
                "reasoning": "Strong backend experience with Python and FastAPI."
            }
        ]
    }

    return dummy_response