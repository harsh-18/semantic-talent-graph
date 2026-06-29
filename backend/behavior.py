from datetime import datetime


def calculate_behavior_score(candidate):
    """
    Calculate candidate behavior score using
    Redrob behavioral signals.
    """

    signals = candidate.get("redrob_signals", {})

    score = 0

    # -------------------------
    # Profile Completeness
    # -------------------------

    score += signals.get(
        "profile_completeness_score",
        0
    ) * 0.20

    # -------------------------
    # Open To Work
    # -------------------------

    if signals.get("open_to_work_flag", False):
        score += 15

    # -------------------------
    # Recruiter Response
    # -------------------------

    score += signals.get(
        "recruiter_response_rate",
        0
    ) * 20

    # -------------------------
    # Interview Completion
    # -------------------------

    score += signals.get(
        "interview_completion_rate",
        0
    ) * 20

    # -------------------------
    # Offer Acceptance
    # -------------------------

    score += signals.get(
        "offer_acceptance_rate",
        0
    ) * 10

    # -------------------------
    # Github Activity
    # -------------------------

    score += signals.get(
        "github_activity_score",
        0
    )

    # -------------------------
    # Saved By Recruiters
    # -------------------------

    score += signals.get(
        "saved_by_recruiters_30d",
        0
    )

    return round(score, 2)
def is_active_candidate(candidate):
    """
    Returns True if candidate
    was recently active.
    """

    signals = candidate.get("redrob_signals", {})

    last_active = signals.get(
        "last_active_date"
    )

    if not last_active:
        return False

    last_active = datetime.strptime(
        last_active,
        "%Y-%m-%d"
    )

    today = datetime.today()

    days = (today - last_active).days

    return days <= 90
def extract_behavior(candidate):

    return {

        "behavior_score":
            calculate_behavior_score(candidate),

        "active":
            is_active_candidate(candidate),

        "signals":
            candidate.get("redrob_signals", {})
    }