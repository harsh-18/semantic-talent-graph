import streamlit as st
from typing import Dict, Any

def inject_custom_css():
    """
    Injects global modern styling, custom typography, dark mode foundations,
    and premium styling for the Redrob Semantic Talent Graph dashboard.
    """
    css_styles = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* Global App View Overrides */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0b0f19; /* Dark slate */
        font-family: 'Inter', sans-serif;
        color: #f1f5f9;
    }

    [data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.8);
        backdrop-filter: blur(12px);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        color: #ffffff;
        margin-top: 0;
    }

    /* Custom Streamlit component styling */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: #ffffff;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45);
        color: #ffffff;
    }

    div.stTextInput input {
        background-color: #1e293b !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #f1f5f9 !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif;
        padding: 10px 14px !important;
    }

    div.stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 1px #3b82f6 !important;
    }

    /* Premium Candidate Card Styling */
    .candidate-card-wrapper {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        transition: all 0.25s ease;
    }

    .candidate-card-wrapper:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.4);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.4);
    }

    .card-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .rank-tag {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%); /* Green gradient */
        color: #ffffff;
        padding: 4px 10px;
        border-radius: 6px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }

    .candidate-title-info {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .candidate-name-text {
        font-family: 'Outfit', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }

    .candidate-id-sub {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .meta-pills-row {
        display: flex;
        gap: 15px;
        margin-bottom: 16px;
        font-size: 0.85rem;
        color: #94a3b8;
    }

    .meta-pill {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 4px 10px;
        border-radius: 6px;
    }

    .skills-section-header {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 8px;
        font-weight: 700;
    }

    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }

    .skill-badge-matched {
        background-color: rgba(16, 185, 129, 0.15); /* Green translucent */
        color: #34d399; /* Green text */
        border: 1px solid rgba(16, 185, 129, 0.35);
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }

    .skill-badge-other {
        background-color: rgba(148, 163, 184, 0.08); /* Slate translucent */
        color: #94a3b8; /* Slate text */
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
    }

    .custom-progress-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        margin-bottom: 4px;
        color: #e2e8f0;
    }
    </style>
    """
    st.markdown(css_styles, unsafe_allow_html=True)

def render_candidate_card(candidate_dict: Dict[str, Any]):
    """
    Renders a beautifully styled candidate card with metadata, progress bar,
    and distinguished skills highlighting.
    """
    name = candidate_dict.get("name", "Unknown Candidate")
    rank = candidate_dict.get("rank", 0)
    cid = candidate_dict.get("candidate_id", "N/A")
    match_score = candidate_dict.get("match_score", 0.0)
    experience_years = candidate_dict.get("experience_years", 0)
    core_skills = candidate_dict.get("core_skills", [])
    matched_skills = candidate_dict.get("matched_skills", [])
    reasoning = candidate_dict.get("reasoning", "No evaluation details available.")

    # Convert match_score to a value between 0.0 and 1.0 for st.progress
    progress_val = max(0.0, min(1.0, float(match_score) / 100.0))

    # Skill tag generation
    skills_badges = []
    for skill in core_skills:
        if skill in matched_skills:
            skills_badges.append(f'<span class="skill-badge-matched">✓ {skill}</span>')
        else:
            skills_badges.append(f'<span class="skill-badge-other">{skill}</span>')
    skills_html = " ".join(skills_badges)

    # Use st.container to group elements inside a card structure using CSS styles injected
    with st.container():
        st.markdown(
            f"""
            <div class="candidate-card-wrapper">
                <div class="card-header-row">
                    <div class="candidate-title-info">
                        <span class="rank-tag">Rank {rank}</span>
                        <h3 class="candidate-name-text">{name}</h3>
                        <span class="candidate-id-sub">{cid}</span>
                    </div>
                    <div style="font-weight: 600; color: #3b82f6; font-family: 'Outfit'; font-size: 1.05rem;">
                        {experience_years} Years Experience
                    </div>
                </div>
                
                <div class="meta-pills-row">
                    <div class="meta-pill">🧬 Core Skills: {len(core_skills)}</div>
                    <div class="meta-pill">🎯 Matched Skills: {len(matched_skills)}</div>
                </div>
                
                <div class="custom-progress-info">
                    <strong>Match Relevance Score</strong>
                    <strong>{match_score}%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # We place st.progress in the column layout just below the card header text to keep it integrated
        st.progress(progress_val)
        
        # Skill pills block
        st.markdown(
            f"""
            <div style="margin-top: 12px; margin-bottom: 12px;">
                <div class="skills-section-header">Skills Inventory</div>
                <div class="skills-container">
                    {skills_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Reasoning details
        st.info(f"**Semantic Alignment Analysis:**  \n{reasoning}")
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
