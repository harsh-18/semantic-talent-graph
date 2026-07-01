from fastapi import FastAPI
from models import SearchRequest

from preprocess import (
    load_candidates,
    preprocess_candidates
)

from honeypot import remove_honeypots
from ranking import rank_candidates


app = FastAPI(
    title="Semantic Talent Graph API",
    version="1.0"
)

# ===================================================
# Load everything once when server starts
# ===================================================

print("\nLoading candidate dataset...")

DATA_PATH = "data/candidates.jsonl.gz"

raw_candidates = load_candidates(DATA_PATH)

processed_candidates = preprocess_candidates(raw_candidates)

clean_candidates = remove_honeypots(processed_candidates)

print(f"Backend Ready!")
print(f"Candidates Loaded : {len(raw_candidates)}")
print(f"Candidates After Cleaning : {len(clean_candidates)}")

# Warm up the TF-IDF vectorizer at startup so the first request is instant!
print("Warming up TF-IDF vectorizer...")
_ = rank_candidates(clean_candidates, "warmup")
print("Warmup complete!")


# ===================================================
# Home Route
# ===================================================

@app.get("/")
def home():

    return {
        "status": "running",
        "message": "Semantic Talent Graph Backend Running"
    }


# ===================================================
# Search Endpoint
# ===================================================

@app.post("/search")
def search(request: SearchRequest):

    # Rank candidates using TF-IDF ranking pipeline
    ranked_candidates = rank_candidates(
        clean_candidates,
        request.query
    )

    results = []

    for rank, candidate in enumerate(ranked_candidates[:100], start=1):

        profile = candidate["raw_candidate"].get("profile", {})

        results.append({

            "candidate_id": candidate["candidate_id"],

            "name": profile.get(
                "anonymized_name",
                "Unknown"
            ),

            "current_role": profile.get(
                "current_title",
                "N/A"
            ),

            "rank": rank,

            "score": candidate.get("match_score", candidate["behavior_score"]),

            "behavior_score": candidate["behavior_score"],

            "active": candidate["active"],

            "honeypot": candidate["is_honeypot"],

            "reasoning": candidate.get("reasoning", "TF-IDF matching candidate profile.")

        })

    return {

        "query": request.query,

        "total_candidates": len(clean_candidates),

        "results": results

    }