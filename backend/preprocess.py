import json
import re
from docx import Document
from behavior import extract_behavior
from honeypot import (
    calculate_honeypot_score,
    is_honeypot
)

# --------------------------------------------------
# Load Candidate Dataset
# --------------------------------------------------

def load_candidates(file_path):
    """
    Load candidates from JSONL file.
    Returns a list of dictionaries.
    """

    candidates = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                candidates.append(json.loads(line))

    return candidates


# --------------------------------------------------
# Load Job Description
# --------------------------------------------------

def load_job_description(doc_path):
    """
    Load the recruiter job description from DOCX.
    """

    document = Document(doc_path)

    paragraphs = []

    for para in document.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text)

    return "\n".join(paragraphs)


# --------------------------------------------------
# Text Cleaning
# --------------------------------------------------

def clean_text(text):
    """
    Clean text before TF-IDF.

    - lowercase
    - remove punctuation
    - remove extra spaces
    """

    if text is None:
        return ""

    text = str(text).lower()

    text = re.sub(r"[^a-z0-9\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

def create_combined_text(candidate):
    """
    Convert nested candidate profile into one clean
    searchable document for TF-IDF.
    """

    text_parts = []

    # ----------------------------
    # Profile
    # ----------------------------

    profile = candidate.get("profile", {})

    text_parts.extend([
        profile.get("headline", ""),
        profile.get("summary", ""),
        profile.get("current_title", ""),
        profile.get("current_company", ""),
        profile.get("current_industry", "")
    ])

    # ----------------------------
    # Career History
    # ----------------------------

    for job in candidate.get("career_history", []):

        text_parts.extend([
            job.get("title", ""),
            job.get("company", ""),
            job.get("description", ""),
            job.get("industry", "")
        ])

    # ----------------------------
    # Education
    # ----------------------------

    for edu in candidate.get("education", []):

        text_parts.extend([
            edu.get("institution", ""),
            edu.get("degree", ""),
            edu.get("field_of_study", "")
        ])

    # ----------------------------
    # Skills
    # ----------------------------

    for skill in candidate.get("skills", []):

        text_parts.append(skill.get("name", ""))

    # ----------------------------
    # Certifications
    # ----------------------------

    for cert in candidate.get("certifications", []):

        if isinstance(cert, dict):
            text_parts.append(cert.get("name", ""))

        else:
            text_parts.append(str(cert))

    # ----------------------------
    # Languages
    # ----------------------------

    for language in candidate.get("languages", []):

        text_parts.append(language.get("language", ""))

    combined_text = " ".join(text_parts)

    return clean_text(combined_text)


# --------------------------------------------------
# Extract Behavioral Signals
# --------------------------------------------------

def extract_behavior_signals(candidate):
    """
    Extract Redrob behavioral metadata.
    """

    return candidate.get("redrob_signals", {})
def preprocess_candidates(file_path):
    """
    Complete preprocessing pipeline.

    Loads candidates, creates searchable text,
    extracts behavioral signals, detects honeypots,
    and returns processed candidates.
    """

    candidates = load_candidates(file_path)

    processed_candidates = []

    for candidate in candidates:

        # Create searchable text
        combined_text = create_combined_text(candidate)

        # Extract behavior information
        behavior = extract_behavior(candidate)

        # Honeypot detection
        honeypot_score = calculate_honeypot_score(candidate)

        processed_candidate = {

            "candidate_id": candidate.get("candidate_id"),

            "combined_text": combined_text,

            "behavior_score": behavior["behavior_score"],

            "active": behavior["active"],

            "behavior_signals": behavior["signals"],

            "honeypot_score": honeypot_score,

            "is_honeypot": is_honeypot(candidate),

            "raw_candidate": candidate
        }

        processed_candidates.append(processed_candidate)

    return processed_candidates