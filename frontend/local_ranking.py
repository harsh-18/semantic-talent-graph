import re
import json
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def local_load_candidates(file_path: str) -> List[Dict[str, Any]]:
    """
    Load candidates from JSON, JSONL, or JSONL.GZ file.
    Returns a list of candidate dictionaries. Highly memory-efficient.
    """
    import os
    import gzip
    import json

    # If looking for candidates.jsonl but candidates.jsonl.gz exists, use it
    if not os.path.exists(file_path):
        if file_path.endswith("candidates.jsonl") and os.path.exists(file_path + ".gz"):
            file_path = file_path + ".gz"
        elif file_path.endswith("candidates.jsonl") and os.path.exists(file_path.replace("candidates.jsonl", "candidates.jsonl.gz")):
            file_path = file_path.replace("candidates.jsonl", "candidates.jsonl.gz")

    is_gzip = file_path.endswith(".gz")

    def open_file(path):
        if is_gzip:
            return gzip.open(path, "rt", encoding="utf-8")
        return open(path, "r", encoding="utf-8")

    # 1. Peek at the first character to determine format
    try:
        with open_file(file_path) as file:
            first_char = file.read(1).strip()
    except Exception:
        first_char = ""
            
    # 2. If it's a JSON array, load the entire file
    if first_char == "[":
        with open_file(file_path) as file:
            try:
                return json.load(file)
            except Exception:
                pass
                
    # 3. Otherwise, parse as JSONL line-by-line to avoid loading full file content into memory
    candidates = []
    try:
        with open_file(file_path) as file:
            for line in file:
                line = line.strip()
                if line:
                    try:
                        candidates.append(json.loads(line))
                    except Exception:
                        pass
    except Exception:
        pass
    return candidates

def extract_matched_skills(query: str, candidate_skills: List[Dict[str, Any]]) -> List[str]:
    """
    Find which candidate skills are mentioned or match the search query.
    """
    if not query:
        return []
    
    # Tokenize and clean query
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
    Generate detailed semantic alignment analysis reasoning for UI display.
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

def local_rank_candidates(
    query: str,
    processed_candidates: List[Dict[str, Any]],
    similarity_weight: float = 0.7,
    behavior_weight: float = 0.3,
    hide_honeypots: bool = False,
    min_experience: float = 0.0,
    min_behavior_score: float = 0.0,
    target_education_tiers: List[str] = None
) -> List[Dict[str, Any]]:
    """
    Rank processed candidates based on TF-IDF similarity with query and behavioral scores.
    Applies custom filters. Runs locally in the frontend workspace.
    """
    filtered_candidates = []
    
    for pc in processed_candidates:
        raw = pc["raw_candidate"]
        profile = raw.get("profile", {})
        
        # Filter 1: Honeypots
        if hide_honeypots and pc["is_honeypot"]:
            continue
            
        # Filter 2: Years of Experience
        exp = profile.get("years_of_experience", 0)
        if exp < min_experience:
            continue
            
        # Filter 3: Minimum Behavior Score
        if pc["behavior_score"] < min_behavior_score:
            continue
            
        # Filter 4: Education Tier
        if target_education_tiers:
            edu_list = raw.get("education", [])
            has_matching_tier = False
            for edu in edu_list:
                tier = edu.get("tier", "unknown")
                if tier in target_education_tiers:
                    has_matching_tier = True
                    break
            if not has_matching_tier:
                continue
                
        filtered_candidates.append(pc)
        
    if not filtered_candidates:
        return []
        
    cleaned_query = query.strip()
    similarity_scores = [0.0] * len(filtered_candidates)
    
    if cleaned_query:
        corpus = [pc["combined_text"] for pc in filtered_candidates]
        vectorizer = TfidfVectorizer(stop_words="english")
        try:
            tfidf_matrix = vectorizer.fit_transform(corpus)
            query_vector = vectorizer.transform([cleaned_query])
            cos_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            similarity_scores = [float(score) * 100.0 for score in cos_similarities]
        except Exception:
            similarity_scores = [0.0] * len(filtered_candidates)
            
    ranked_list = []
    for i, pc in enumerate(filtered_candidates):
        sim_score = similarity_scores[i]
        beh_score = pc["behavior_score"]
        
        total_weight = similarity_weight + behavior_weight
        if total_weight > 0:
            match_score = (sim_score * similarity_weight + beh_score * behavior_weight) / total_weight
        else:
            match_score = 0.0
            
        # Scale composite match score to [0.0, 1.0] for challenge/submission compliance
        match_score_scaled = match_score / 100.0
            
        raw = pc["raw_candidate"]
        matched_skills = extract_matched_skills(query, raw.get("skills", []))
        reasoning_text = generate_reasoning(
            sim_score, 
            beh_score, 
            pc["is_honeypot"],
            pc["honeypot_score"],
            raw, 
            matched_skills
        )
        
        ranked_list.append({
            "candidate_id": pc["candidate_id"],
            "match_score": round(match_score_scaled, 4),
            "similarity_score": round(sim_score, 1),
            "behavior_score": round(beh_score, 1),
            "honeypot_score": pc["honeypot_score"],
            "is_honeypot": pc["is_honeypot"],
            "active": pc["active"],
            "matched_skills": matched_skills,
            "reasoning": reasoning_text,
            "raw_candidate": raw
        })
        
    ranked_list.sort(key=lambda x: (-x["match_score"], x["candidate_id"]))
    for rank_idx, item in enumerate(ranked_list):
        item["rank"] = rank_idx + 1
        
    return ranked_list
