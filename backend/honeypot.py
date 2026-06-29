def detect_impossible_experience(candidate):

    profile = candidate.get("profile", {})

    experience = profile.get("years_of_experience", 0)

    career = candidate.get("career_history", [])

    total_months = 0

    for job in career:
        total_months += job.get("duration_months", 0)

    total_years = total_months / 12

    if experience > total_years + 2:
        return True

    return False
from collections import Counter


def detect_keyword_stuffing(candidate):

    skills = []

    for skill in candidate.get("skills", []):

        skills.append(
            skill.get("name", "").lower()
        )

    counter = Counter(skills)

    for value in counter.values():

        if value > 3:
            return True

    return False
def detect_empty_profile(candidate):

    profile = candidate.get("profile", {})

    summary = profile.get("summary", "")

    skills = candidate.get("skills", [])

    if len(summary) < 50:
        return True

    if len(skills) < 2:
        return True

    return False
def calculate_honeypot_score(candidate):

    score = 0

    if detect_impossible_experience(candidate):
        score += 40

    if detect_keyword_stuffing(candidate):
        score += 30

    if detect_empty_profile(candidate):
        score += 30

    return score
def is_honeypot(candidate):

    return calculate_honeypot_score(candidate) >= 40