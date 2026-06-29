from pydantic import BaseModel

class SearchRequest(BaseModel):
    query: str


class CandidateResponse(BaseModel):
    candidate_id: str
    match_score: float
    behavior_score: float
    reasoning: str