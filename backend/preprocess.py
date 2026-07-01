import json
import re
from docx import Document

from behavior import extract_behavior
from honeypot import (
    calculate_honeypot_score,
    is_honeypot
)


# ==================================================
# Load Candidate Dataset
# ==================================================

def load_candidates(file_path):
    """
    Load candidates from JSON, JSONL, or JSONL.GZ file.
    Supports gzip compression, fallbacks, and handles large datasets.
    """
    import os
    import json
    import gzip

    # Fallback checks
    if not os.path.exists(file_path):
        # If looking for candidates.jsonl but candidates.jsonl.gz exists, use it
        if file_path.endswith("candidates.jsonl") and os.path.exists(file_path + ".gz"):
            file_path = file_path + ".gz"
        elif file_path.endswith("candidates.jsonl") and os.path.exists(file_path.replace("candidates.jsonl", "candidates.jsonl.gz")):
            file_path = file_path.replace("candidates.jsonl", "candidates.jsonl.gz")
        else:
            dir_name = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            
            # If looking for candidates.jsonl but not found, try sample_candidates.json
            if "candidates.jsonl" in base_name:
                fallback_path = os.path.join(dir_name if dir_name else "data", "sample_candidates.json")
                if os.path.exists(fallback_path):
                    file_path = fallback_path
                elif os.path.exists("backend/data/sample_candidates.json"):
                    file_path = "backend/data/sample_candidates.json"
                elif os.path.exists("data/sample_candidates.json"):
                    file_path = "data/sample_candidates.json"
            
            # If file_path still does not exist, throw FileNotFoundError
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Could not find candidate data file at {file_path}")

    # Determine if the file is gzipped
    is_gzip = file_path.endswith(".gz")

    def open_file(path):
        if is_gzip:
            return gzip.open(path, "rt", encoding="utf-8")
        return open(path, "r", encoding="utf-8")

    # Peek at first non-whitespace char to detect JSON array vs JSONL
    with open_file(file_path) as file:
        first_char = ""
        for line in file:
            line_s = line.strip()
            if line_s:
                first_char = line_s[0]
                break

    # If JSON array
    if first_char == "[":
        with open_file(file_path) as file:
            return json.load(file)

    # If JSONL
    candidates = []
    with open_file(file_path) as file:
        for line in file:
            line = line.strip()
            if line:
                candidates.append(json.loads(line))
    return candidates


# ==================================================
# Load Job Description
# ==================================================

def load_job_description(doc_path):
    """
    Read recruiter job description from DOCX.
    """

    document = Document(doc_path)

    paragraphs = []

    for para in document.paragraphs:

        if para.text.strip():
            paragraphs.append(para.text)

    return "\n".join(paragraphs)


# ==================================================
# Text Cleaning
# ==================================================

def clean_text(text):
    """
    Clean text before TF-IDF.
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==================================================
# Create Searchable Candidate Document
# ==================================================

def create_combined_text(candidate):
    """
    Convert complete candidate profile into one
    searchable document.
    """

    text_parts = []

    # --------------------
    # Profile
    # --------------------

    profile = candidate.get("profile", {})

    text_parts.extend([
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", ""),
        profile.get("current_company", ""),
        profile.get("current_industry", "")
    ])

    # --------------------
    # Career History
    # --------------------

    for job in candidate.get("career_history", []):

        text_parts.extend([
            job.get("title", ""),
            job.get("company", ""),
            job.get("description", ""),
            job.get("industry", "")
        ])

    # --------------------
    # Education
    # --------------------

    for edu in candidate.get("education", []):

        text_parts.extend([
            edu.get("institution", ""),
            edu.get("degree", ""),
            edu.get("field_of_study", "")
        ])

    # --------------------
    # Skills
    # --------------------

    for skill in candidate.get("skills", []):

        text_parts.append(
            skill.get("name", "")
        )

    # --------------------
    # Certifications
    # --------------------

    for cert in candidate.get("certifications", []):

        if isinstance(cert, dict):

            text_parts.append(
                cert.get("name", "")
            )

        else:

            text_parts.append(str(cert))

    # --------------------
    # Languages
    # --------------------

    for language in candidate.get("languages", []):

        text_parts.append(
            language.get("language", "")
        )

    combined_text = " ".join(text_parts)

    return clean_text(combined_text)


# ==================================================
# Extract Raw Behavioral Signals
# ==================================================

def extract_behavior_signals(candidate):

    return candidate.get(
        "redrob_signals",
        {}
    )


# ==================================================
# Main Preprocessing Pipeline
# ==================================================

def preprocess_candidates(candidates):
    """
    Main preprocessing pipeline.

    Generates:
    - Combined Text
    - Behavior Score
    - Active Status
    - Honeypot Score
    """

    processed_candidates = []

    for candidate in candidates:

        # --------------------
        # Combined Text
        # --------------------

        combined_text = create_combined_text(candidate)

        # --------------------
        # Behavior Analysis
        # --------------------

        behavior = extract_behavior(candidate)

        # Down-weight inactive candidates

        if not behavior["active"]:

            behavior["behavior_score"] *= 0.70

        behavior["behavior_score"] = round(
            behavior["behavior_score"],
            2
        )

        # --------------------
        # Honeypot Analysis
        # --------------------

        honeypot_score = calculate_honeypot_score(
            candidate
        )

        processed_candidate = {

            "candidate_id":
                candidate.get("candidate_id"),

            "combined_text":
                combined_text,

            "behavior_score":
                behavior["behavior_score"],

            "active":
                behavior["active"],

            "behavior_signals":
                behavior["signals"],

            "honeypot_score":
                honeypot_score,

            "is_honeypot":
                is_honeypot(candidate),

            "raw_candidate":
                candidate
        }

        processed_candidates.append(
            processed_candidate
        )

    return processed_candidates


# ==================================================
# Testing
# ==================================================

if __name__ == "__main__":

    DATA_PATH = "data/candidates.jsonl.gz"

    candidates = load_candidates(DATA_PATH)

    processed = preprocess_candidates(candidates)

    print("=" * 50)
    print("Total Candidates :", len(processed))
    print("=" * 50)

    print("\nFirst Candidate\n")

    print(processed[0])