import streamlit as st
import json
import os
import time
from components import inject_custom_css, render_candidate_card

# Set up page configurations
st.set_page_config(
    page_title="Redrob Semantic Talent Graph",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom premium CSS rules
inject_custom_css()

# Render gradient header
st.markdown(
    """
    <div style="text-align: center; padding: 30px 0 15px 0;">
        <h1 style="background: linear-gradient(135deg, #60a5fa 0%, #34d399 50%, #818cf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.2rem; font-weight: 800; font-family: 'Outfit', sans-serif; letter-spacing: -0.02em; margin-bottom: 8px;">
            Redrob Semantic Talent Graph
        </h1>
        <p style="color: #94a3b8; font-size: 1.2rem; max-width: 700px; margin: 0 auto; font-family: 'Inter', sans-serif; font-weight: 300; line-height: 1.6;">
            7-Day Hackathon Setup: Real-time semantic profile scoring and candidate matching.
        </p>
    </div>
    <div style="height: 1px; background: linear-gradient(90deg, rgba(96, 165, 250, 0) 0%, rgba(96, 165, 250, 0.25) 50%, rgba(96, 165, 250, 0) 100%); margin-bottom: 30px;"></div>
    """,
    unsafe_allow_html=True
)

# Recruiter Query Input
st.markdown("### 🔍 Semantic Match Query")
search_query = st.text_input(
    label="Search by job description, core skills, or role description:",
    value="Looking for an AI Engineer with backend integration skills",
    placeholder="Type candidate profiles requirements (e.g. React Developer with FastAPI skills)..."
)

# Let's create search actions
search_btn = st.button("Search Candidates ⚡", use_container_width=True)

# Helper function to safely resolve and load mock_data.json
def get_mock_data():
    # Search paths relative to app.py location
    paths = [
        "mock_data.json",
        "../mock_data.json",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "mock_data.json"),
        os.path.join(os.path.dirname(__file__), "mock_data.json")
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return None

# Load mock data when search is triggered or if we have an initial query
if search_btn or search_query:
    # Simulate processing time delay for rich UX
    with st.spinner("Executing semantic search across talent database..."):
        if search_btn:
            time.sleep(0.3)
        
        mock_data = get_mock_data()
        
        if mock_data is None:
            st.error("Error: Could not locate `mock_data.json` at root directory. Please verify project scaffolding.")
        else:
            # Stats row at the top using st.metric as requested
            st.markdown("### 📊 Matching Metrics Summary")
            
            # Extract statistics
            time_ms = mock_data.get("processing_time_ms", 0)
            total_matches = mock_data.get("total_matches_found", 0)
            total_candidates = mock_data.get("total_candidates", 0)
            
            col_time, col_matches, col_space = st.columns(3)
            with col_time:
                st.metric(label="Processing Time", value=f"{time_ms} ms")
            with col_matches:
                st.metric(label="Total Matches Found", value=f"{total_matches} Profiles")
            with col_space:
                st.metric(label="Total Candidates Evaluated", value=f"{total_candidates:,}")
                
            st.markdown("<hr style='border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 25px 0;'>", unsafe_allow_html=True)
            
            # Render matches header
            st.markdown(f"### 🏆 Top Matches for: *\"{search_query}\"*")
            
            # Candidate list
            candidates = mock_data.get("top_candidates", [])
            if not candidates:
                st.warning("No candidate records found in `mock_data.json` matching API schema structure.")
            else:
                for candidate in candidates:
                    render_candidate_card(candidate)
else:
    # Landing state helper info
    st.markdown(
        """
        <div style="background: rgba(255, 255, 255, 0.02); border: 1px dashed rgba(255, 255, 255, 0.1); padding: 40px; border-radius: 16px; text-align: center; margin-top: 20px;">
            <p style="color: #64748b; font-size: 1.1rem; margin: 0;">
                Provide a search query or press the button to execute semantic query retrieval.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
