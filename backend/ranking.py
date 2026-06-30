import os
import json
from datetime import datetime, date
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from docx import Document

# AI skills list
AI_SKILLS = {"machine learning", "deep learning", "nlp", "python", "tensorflow", 
             "pytorch", "llm", "transformers", "bert", "gpt", "scikit-learn",
             "mlops", "langchain", "embeddings", "fine-tuning llms", "computer vision",
             "recommendation systems", "feature engineering", "data science"}

def count_ai_skills(candidate):
    skills = [s['name'].lower() for s in candidate.get('skills', [])]
    return sum(1 for s in skills if s in AI_SKILLS)

def final_score(candidate, tfidf_score):
    # Inactive penalty
    last_active = candidate['redrob_signals']['last_active_date']
    last_date = datetime.strptime(last_active, "%Y-%m-%d").date()
    days_inactive = (date.today() - last_date).days
    activity_multiplier = 0.75 if days_inactive > 180 else 1.0
    
    # AI skills boost
    ai_count = count_ai_skills(candidate)
    ai_boost = 1 + (ai_count * 0.05)
    
    return tfidf_score * activity_multiplier * ai_boost

def generate_reasoning(candidate, score):
    title = candidate['profile']['current_title']
    yrs = candidate['profile']['years_of_experience']
    response_rate = candidate['redrob_signals']['recruiter_response_rate']
    ai_skills = count_ai_skills(candidate)
    return f"{title} with {yrs} yrs; {ai_skills} AI core skills; response rate {response_rate:.2f}."

def build_resume_text(candidate):
    parts = []
    
    # Profile summary
    parts.append(candidate['profile'].get('summary', ''))
    
    # Current title
    parts.append(candidate['profile'].get('current_title', ''))
    
    # Career descriptions
    for job in candidate.get('career_history', []):
        parts.append(job.get('description', ''))
    
    # Skills
    skill_names = [s['name'] for s in candidate.get('skills', [])]
    parts.append(' '.join(skill_names))
    
    return ' '.join(parts)

def rank_candidates(candidates, query):
    """
    Ranks candidates using TF-IDF + Cosine Similarity based on query.
    candidates: List of candidate dictionaries (preprocessed or raw).
    query: The search query string.
    """
    if not candidates:
        return []
        
    cleaned_query = query.strip()
    if not cleaned_query:
        # Fallback: sort by behavior_score (descending) and candidate_id (ascending)
        return sorted(candidates, key=lambda x: (-x.get("behavior_score", 0.0), x.get("candidate_id", "")))
        
    # Build text corpus for TF-IDF. 
    # Use pre-computed combined_text if available, otherwise build it.
    corpus = []
    for c in candidates:
        if "combined_text" in c:
            corpus.append(c["combined_text"])
        else:
            raw_c = c.get("raw_candidate", c)
            corpus.append(build_resume_text(raw_c))
            
    # TF-IDF fit
    vectorizer = TfidfVectorizer(stop_words='english')
    all_docs = [cleaned_query] + corpus
    
    try:
        tfidf_matrix = vectorizer.fit_transform(all_docs)
        query_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]
        scores = cosine_similarity(query_vector, resume_vectors)[0]
    except Exception:
        scores = [0.0] * len(candidates)
        
    # Rank candidates and assign scores
    ranked_list = []
    for c, score in zip(candidates, scores):
        raw = c.get("raw_candidate", c)
        
        # Calculate final adjusted score
        try:
            adj_score = final_score(raw, score)
        except Exception:
            adj_score = score
            
        try:
            reasoning = generate_reasoning(raw, adj_score)
        except Exception:
            reasoning = "TF-IDF matching candidate profile."
            
        ranked_c = dict(c)
        # Store scores and reasoning in candidate dictionary
        ranked_c["match_score"] = round(adj_score, 4)
        ranked_c["similarity_score"] = round(score, 4)
        ranked_c["reasoning"] = reasoning
        
        # If behavior_score is not in the dictionary, ensure it's there
        if "behavior_score" not in ranked_c:
            ranked_c["behavior_score"] = c.get("behavior_signals", {}).get("behavior_score", 0.0)
            
        ranked_list.append(ranked_c)
        
    # Enforce candidate_id ascending tie-break rule during sorting
    ranked_list.sort(key=lambda x: (-x["match_score"], x.get("candidate_id", "")))
    
    return ranked_list

if __name__ == "__main__":
    # Standalone execution logic (Sapna's pipeline)
    print("Running standalone ranking pipeline...")
    
    # ── Step 1: Data Load ──────────────────────────
    data_file = "data/sample_candidates.json"
    if not os.path.exists(data_file) and os.path.exists("backend/data/sample_candidates.json"):
        data_file = "backend/data/sample_candidates.json"
        
    with open(data_file, "r") as f:
        candidates = json.load(f)

    print(f"Total candidates: {len(candidates)}")
    print(f"First ID: {candidates[0]['candidate_id']}")
    print(f"Keys: {list(candidates[0].keys())}")

    # Test karo
    print("Testing resume text builder on top 3 candidates:")
    for c in candidates[:3]:
        text = build_resume_text(c)
        print(f"{c['candidate_id']}: {text[:100]}...")
        print()

    # ── Step 3: JD Load ────────────────────────────
    jd_file = "data/job_description.docx"
    if not os.path.exists(jd_file) and os.path.exists("backend/data/job_description.docx"):
        jd_file = "backend/data/job_description.docx"
        
    doc = Document(jd_file)
    jd_text = ""
    for para in doc.paragraphs:
        if para.text.strip():
            jd_text += para.text + " "

    print("JD loaded!")
    print(jd_text[:500])

    # ── Step 4: TF-IDF Ranking ─────────────────────
    # Sabke resume text banao
    corpus = []
    for c in candidates:
        corpus.append(build_resume_text(c))

    # TF-IDF fit karo JD + sabke resumes pe
    vectorizer = TfidfVectorizer(stop_words='english')
    all_docs = [jd_text] + corpus
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    # JD vs har candidate ka cosine similarity
    jd_vector = tfidf_matrix[0]
    resume_vectors = tfidf_matrix[1:]
    scores = cosine_similarity(jd_vector, resume_vectors)[0]

    print("Top 5 scores:", sorted(scores, reverse=True)[:5])

    # ── Step 5: Reasoning + CSV ────────────────────
    # Sort + Top 100
    adjusted_scores = [final_score(c, s) for c, s in zip(candidates, scores)]
    ranked = sorted(zip(candidates, adjusted_scores), key=lambda x: -x[1])
    top100 = ranked[:100]

    # CSV banao
    rows = []
    for rank, (candidate, score) in enumerate(top100, 1):
        rows.append({
            "candidate_id": candidate['candidate_id'],
            "rank": rank,
            "score": round(score, 4),
            "reasoning": generate_reasoning(candidate, score)
        })

    df = pd.DataFrame(rows)
    os.makedirs("output", exist_ok=True)
    df.to_csv("output/top100_candidates.csv", index=False)
    print("CSV saved to output/top100_candidates.csv!")
    print(df.head(5))