import re
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_matched_skills(query: str, candidate_skills: List[Dict[str, Any]]) -> List[str]:
    """
    Find which candidate skills are mentioned or match the search query.
    """
    if not query:
        return []
    
    query_words = set(re.findall(r"\b\w+\b", query.lower()))
    matched = []
    
    for skill in candidate_skills:
        name = skill.get("name", "")
        name_lower = name.lower()
        if name_lower in query.lower() or any(part in query_words for part in name_lower.split()):
            matched.append(name)
            
    return matched

def generate_reasoning(
    similarity_score: float, 
    behavior_score: float, 
    is_honeypot_flag: bool,
    honeypot_score: int,
    candidate: Dict[str, Any], 
    matched_skills: List[str]
) -> str:
    """
    Generate detailed semantic alignment analysis reasoning.
    """
    reasons = []
    profile = candidate.get("profile", {})
    title = profile.get("current_title", "Professional")
    exp = profile.get("years_of_experience", 0)
    
    if is_honeypot_flag:
        reasons.append(f"⚠️ Flagged as potential Honeypot (Score: {honeypot_score}/100). Profile details contain consistency or stuffing anomalies.")
        return " ".join(reasons)
        
    if similarity_score > 70:
        reasons.append(f"Excellent semantic fit as a {title}.")
    elif similarity_score > 40:
        reasons.append(f"Moderate semantic match with requested role foundations.")
    else:
        reasons.append(f"Low semantic matching; profile text overlaps minimally with query.")

    if matched_skills:
        reasons.append(f"Matches key query requirements: {', '.join(matched_skills)}.")
    else:
        reasons.append("No direct skill matches found in the search query.")
        
    reasons.append(f"Brings {exp:.1f} years of experience in {profile.get('current_industry', 'industry')}.")
    
    signals = candidate.get("redrob_signals", {})
    if behavior_score > 70:
        reasons.append(f"Highly engaged candidate with {signals.get('profile_completeness_score', 0)}% profile completeness and {signals.get('connection_count', 0)}+ connections.")
    elif behavior_score > 40:
        reasons.append("Steady platform engagement signals.")
    else:
        reasons.append("Low platform activity signals.")
        
    if signals.get("open_to_work_flag", False):
        reasons.append("Actively open to new opportunities.")
        
    return " ".join(reasons)

def rank_candidates(candidates, query):
    """
    Ranks candidates using TF-IDF + Cosine Similarity based on query.
    Aligned with the frontend's local ranking engine.
    """
    if not candidates:
        return []
        
    cleaned_query = query.strip()
    similarity_scores = [0.0] * len(candidates)
    
    if cleaned_query:
        corpus = [c.get("combined_text", "") for c in candidates]
        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            query_vector = vectorizer.transform([cleaned_query])
            cos_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            similarity_scores = [float(score) * 100.0 for score in cos_similarities]
        except Exception:
            similarity_scores = [0.0] * len(candidates)
            
    ranked_list = []
    for i, c in enumerate(candidates):
        sim_score = similarity_scores[i]
        beh_score = c.get("behavior_score", 0.0)
        
        # Aligned composite score calculation
        match_score = sim_score * 0.7 + beh_score * 0.3
        match_score_scaled = match_score / 100.0
        
        raw = c.get("raw_candidate", c)
        matched_skills = extract_matched_skills(query, raw.get("skills", []))
        reasoning_text = generate_reasoning(
            sim_score, 
            beh_score, 
            c.get("is_honeypot", False),
            c.get("honeypot_score", 0),
            raw, 
            matched_skills
        )
        
        ranked_c = dict(c)
        ranked_c["match_score"] = round(match_score_scaled, 4)
        ranked_c["similarity_score"] = round(sim_score, 1)
        ranked_c["behavior_score"] = round(beh_score, 1)
        ranked_c["reasoning"] = reasoning_text
        
        ranked_list.append(ranked_c)
        
    # Enforce candidate_id ascending tie-break rule during sorting
    ranked_list.sort(key=lambda x: (-x["match_score"], x.get("candidate_id", "")))
    
    return ranked_list
