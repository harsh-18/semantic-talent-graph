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
        background-color: #090d16; /* Deep space dark */
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background-color: rgba(9, 13, 22, 0.85);
        backdrop-filter: blur(16px);
    }

    [data-testid="stSidebar"] {
        background-color: #0d1527 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        color: #ffffff;
        margin-top: 0;
    }

    /* Custom Streamlit component styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
        margin-top: 10px;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
        color: #ffffff;
    }

    div.stTextInput input {
        background-color: #111b2f !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #f8fafc !important;
        border-radius: 10px !important;
        font-family: 'Inter', sans-serif;
        padding: 12px 16px !important;
    }

    div.stTextInput input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.25) !important;
    }

    /* Premium Candidate Card Styling */
    .candidate-card-wrapper {
        background: linear-gradient(135deg, rgba(17, 27, 47, 0.7) 0%, rgba(13, 21, 37, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .candidate-card-wrapper:hover {
        transform: translateY(-3px);
        border-color: rgba(37, 99, 235, 0.4);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7);
    }

    .card-header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        flex-wrap: wrap;
        gap: 12px;
    }

    .rank-tag {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }

    .honeypot-badge-flagged {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
    }

    .honeypot-badge-passed {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: #ffffff;
        padding: 6px 14px;
        border-radius: 8px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
    }

    .candidate-title-info {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
    }

    .candidate-name-text {
        font-family: 'Outfit', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
    }

    .candidate-id-sub {
        color: #475569;
        font-size: 0.9rem;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.05);
        padding: 2px 8px;
        border-radius: 4px;
    }

    .headline-text {
        font-size: 1.05rem;
        color: #94a3b8;
        font-weight: 500;
        margin-bottom: 12px;
        line-height: 1.4;
    }

    .summary-text {
        font-size: 0.95rem;
        color: #cbd5e1;
        line-height: 1.6;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.02);
        padding: 14px;
        border-radius: 8px;
        border-left: 3px solid #3b82f6;
    }

    /* Behavioral signals display grid */
    .behavior-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .behavior-stat-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 12px;
        border-radius: 10px;
        text-align: center;
    }

    .behavior-stat-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #3b82f6;
        margin-top: 4px;
    }

    .behavior-stat-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.05em;
    }

    .skills-section-header {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 10px;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .skills-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }

    .skill-badge-matched {
        background-color: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }

    .skill-badge-other {
        background-color: rgba(255, 255, 255, 0.03);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
    }

    .skill-prof {
        font-size: 0.65rem;
        opacity: 0.8;
        margin-left: 4px;
        text-transform: uppercase;
        font-weight: 700;
    }

    .custom-progress-info {
        display: flex;
        justify-content: space-between;
        font-size: 0.9rem;
        margin-bottom: 6px;
        color: #e2e8f0;
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.02);
        padding: 4px;
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
        font-family: 'Outfit', sans-serif;
        color: #94a3b8;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #2563eb;
        color: white;
    }
    </style>
    """
    st.markdown(css_styles, unsafe_allow_html=True)

def render_candidate_card(candidate_item: Dict[str, Any]):
    """
    Renders a beautifully styled, high-impact candidate card following
    the official Candidate Profile Schema.
    """
    cid = candidate_item.get("candidate_id", "N/A")
    rank = candidate_item.get("rank", 0)
    match_score = candidate_item.get("match_score", 0.0)
    sim_score = candidate_item.get("similarity_score", 0.0)
    beh_score = candidate_item.get("behavior_score", 0.0)
    honeypot_score = candidate_item.get("honeypot_score", 0)
    is_honeypot = candidate_item.get("is_honeypot", False)
    matched_skills = candidate_item.get("matched_skills", [])
    reasoning = candidate_item.get("reasoning", "")
    
    raw = candidate_item.get("raw_candidate", {})
    profile = raw.get("profile", {})
    
    name = profile.get("anonymized_name", "Anonymous Candidate")
    headline = profile.get("headline", "Professional Candidate")
    summary = profile.get("summary", "No professional summary provided.")
    location = profile.get("location", "Unknown City")
    country = profile.get("country", "")
    years_exp = profile.get("years_of_experience", 0.0)
    current_title = profile.get("current_title", "Candidate")
    current_company = profile.get("current_company", "N/A")
    current_industry = profile.get("current_industry", "N/A")
    
    # Progress value for streamlit progress bar (0.0 to 1.0)
    progress_val = max(0.0, min(1.0, float(match_score) / 100.0))
    
    # Header tags
    rank_html = f'<span class="rank-tag">Rank {rank}</span>'
    if is_honeypot:
        rank_html += f' <span class="honeypot-badge-flagged">⚠️ Honeypot Flagged ({honeypot_score})</span>'
    else:
        rank_html += f' <span class="honeypot-badge-passed">🛡️ Honeypot Detection: Passed</span>'
        
    # Skills mapping
    skills = raw.get("skills", [])
    skills_badges = []
    for s in skills:
        s_name = s.get("name", "")
        s_prof = s.get("proficiency", "beginner")
        s_dur = s.get("duration_months", 0)
        
        prof_suffix = f'<span class="skill-prof">({s_prof} • {s_dur}m)</span>'
        
        if s_name in matched_skills:
            skills_badges.append(f'<span class="skill-badge-matched">✓ {s_name} {prof_suffix}</span>')
        else:
            skills_badges.append(f'<span class="skill-badge-other">{s_name} {prof_suffix}</span>')
            
    skills_html = " ".join(skills_badges) if skills_badges else "<span style='color: #475569;'>No skills listed</span>"

    # Redrob Signals parsing
    signals = raw.get("redrob_signals", {})
    active_status = "Active" if candidate_item.get("active", True) else "Inactive"
    open_flag = "Yes 🟢" if signals.get("open_to_work_flag", False) else "No"
    gh_score = signals.get("github_activity_score", -1)
    gh_display = f"{gh_score}/100" if gh_score >= 0 else "N/A"
    
    # Render main card container
    with st.container():
        st.markdown(
            f"""
            <div class="candidate-card-wrapper">
                <div class="card-header-row">
                    <div class="candidate-title-info">
                        {rank_html}
                        <h3 class="candidate-name-text">{name}</h3>
                        <span class="candidate-id-sub">{cid}</span>
                    </div>
                    <div style="font-weight: 600; color: #3b82f6; font-family: 'Outfit'; font-size: 1.1rem;">
                        💼 {current_title} @ {current_company}
                    </div>
                </div>
                
                <div class="headline-text">{headline}</div>
                <div class="summary-text">"{summary}"</div>
                
                <div class="meta-pills-row">
                    <div class="meta-pill">🧬 Core Skills: {len(skills)}</div>
                    <div class="meta-pill">🎯 Matched Skills: {len(matched_skills)}</div>
                    <div class="meta-pill">⚡ Behavior Score: {beh_score}/100</div>
                </div>
                
                <!-- Match Score Section -->
                <div class="custom-progress-info">
                    <strong>Composite Match Score</strong>
                    <strong>{match_score}%</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Streamlit progress bar just underneath
        st.progress(progress_val)
        
        # Display Reasoning analysis in st.info box
        if is_honeypot:
            st.error(f"**Honeypot Evaluation:**  \n{reasoning}")
        else:
            st.info(f"**Semantic Alignment Analysis:**  \n{reasoning}")
            
        # Skill pills block
        st.markdown(
            f"""
            <div style="margin-top: 15px; margin-bottom: 20px;">
                <div class="skills-section-header">🧬 Skills & Credentials</div>
                <div class="skills-container">
                    {skills_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Interactive tabs for Career History, Academic Background, and Engagement Signals
        tab_history, tab_education, tab_signals = st.tabs([
            "💼 Career History", 
            "🎓 Education", 
            "📊 Platform Signals"
        ])
        
        with tab_history:
            career_history = raw.get("career_history", [])
            if not career_history:
                st.write("No employment history listed.")
            for job in career_history:
                company = job.get("company", "Company")
                title = job.get("title", "Role")
                start = job.get("start_date", "")
                end = job.get("end_date", "Present") or "Present"
                dur = job.get("duration_months", 0)
                size = job.get("company_size", "unknown")
                ind = job.get("industry", "")
                desc = job.get("description", "")
                
                st.markdown(
                    f"""
                    **{title}** at **{company}**  
                    *{start} to {end} ({dur} months) | Company Size: {size} | Industry: {ind}*  
                    {desc}
                    """
                )
                st.markdown("---")
                
        with tab_education:
            education = raw.get("education", [])
            if not education:
                st.write("No education details listed.")
            for edu in education:
                inst = edu.get("institution", "Institution")
                degree = edu.get("degree", "Degree")
                field = edu.get("field_of_study", "")
                start = edu.get("start_year", "")
                end = edu.get("end_year", "")
                grade = edu.get("grade", "N/A")
                tier = edu.get("tier", "unknown").replace("_", " ").upper()
                
                st.markdown(
                    f"""
                    🎓 **{degree} in {field}**  
                    **{inst}** ({start} - {end})  
                    *Grade: {grade} | Institution Tier: {tier}*
                    """
                )
                st.markdown("---")
                
        with tab_signals:
            st.markdown(
                f"""
                <div class="behavior-grid">
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Profile Completeness</div>
                        <div class="behavior-stat-value">{signals.get('profile_completeness_score', 0)}%</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Behavior Score</div>
                        <div class="behavior-stat-value">{beh_score}</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Honeypot Score</div>
                        <div class="behavior-stat-value">{honeypot_score}</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Open to Work</div>
                        <div class="behavior-stat-value">{open_flag}</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">GitHub Score</div>
                        <div class="behavior-stat-value">{gh_display}</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Connections</div>
                        <div class="behavior-stat-value">{signals.get('connection_count', 0)}</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Recruiter Response</div>
                        <div class="behavior-stat-value">{int(signals.get('recruiter_response_rate', 0) * 100)}%</div>
                    </div>
                    <div class="behavior-stat-card">
                        <div class="behavior-stat-label">Response Speed</div>
                        <div class="behavior-stat-value">{signals.get('avg_response_time_hours', 0):.1f}h</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Display extra signals using columns
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Expected Salary", f"{signals.get('expected_salary_range_inr_lpa', {}).get('min', 0)} - {signals.get('expected_salary_range_inr_lpa', {}).get('max', 0)} LPA")
            with c2:
                st.metric("Notice Period", f"{signals.get('notice_period_days', 0)} Days")
            with c3:
                mode = signals.get('preferred_work_mode', 'remote').upper()
                reloc = "Yes" if signals.get('willing_to_relocate', False) else "No"
                st.metric("Work Mode / Reloc", f"{mode} / Reloc: {reloc}")
                
        # Space divisor
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)
