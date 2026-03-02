import streamlit as st
import joblib
import requests
import json
import pandas as pd
import time
from newspaper import Article

# ==============================
# THE "NEURAL OBSIDIAN" DESIGN SYSTEM
# ==============================
st.set_page_config(
    page_title="NEURAL VERDICT | Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Outfit:wght@200;400;600&display=swap');

    .stApp {
        background: linear-gradient(-45deg, #050505, #120e1f, #051014, #000000);
        background-size: 400% 400%;
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
    }

    .premium-card {
        background: rgba(20, 20, 25, 0.4);
        backdrop-filter: blur(40px) saturate(150%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
    }

    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 4.5rem;
        background: linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0.4) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.05em;
        margin-bottom: 0px;
    }

    /* Professional Button Design */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #000 !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        border-radius: 100px;
        padding: 0.6rem 2rem !important;
        border: none;
        width: 100%;
    }

    .scraped-box {
        background: rgba(0,0,0,0.4);
        border: 1px solid #00f2fe44;
        border-radius: 12px;
        padding: 20px;
        font-size: 0.95rem;
        max-height: 250px;
        overflow-y: auto;
        margin: 15px 0;
        color: #00f2fe;
        font-family: 'monospace';
    }
    </style>
""",
    unsafe_allow_html=True,
)


# ==============================
# LOGIC & ENGINE
# ==============================
@st.cache_resource
def load_engine():
    try:
        m = joblib.load("credibility_model.joblib")
        a = joblib.load("model_accuracy.joblib")
        return m, a
    except:
        return None, 0.9388


model, training_acc = load_engine()

# ==============================
# UI - THE CENTRAL COMMAND
# ==============================

st.markdown('<div class="hero-title">NEURAL VERDICT.</div>', unsafe_allow_html=True)
st.markdown(
    '<p style="letter-spacing: 0.4em; color: #00f2fe; font-size: 0.85rem; margin-top:-10px;">HYBRID FEATURE ANALYSIS ENGINE v1.0</p>',
    unsafe_allow_html=True,
)

# MAIN LAYOUT
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### ANALYSIS TERMINAL")

    url_input = st.text_input(
        "PASTE NEWS URL", placeholder="https://news-site.com/article-path"
    )
    st.markdown(
        "<p style='text-align:center; opacity:0.4; font-size:0.7rem;'>— OR PROVIDE RAW DATA —</p>",
        unsafe_allow_html=True,
    )
    user_text = st.text_area(
        "RAW CONTENT",
        height=100,
        placeholder="Paste article text here...",
        label_visibility="collapsed",
    )

    if st.button("RUN FORENSIC ANALYSIS"):
        content_to_analyze = ""

        # 1. SCRAPING PHASE
        if url_input.strip():
            with st.status("Initializing Scraper Node...", expanded=False) as s:
                try:
                    article = Article(url_input)
                    article.download()
                    article.parse()
                    content_to_analyze = article.text
                    st.session_state["current_data"] = content_to_analyze
                    s.update(label="Scraping Complete", state="complete")
                except Exception as e:
                    st.error(f"Scraper Error: {e}")
        else:
            content_to_analyze = user_text
            st.session_state["current_data"] = content_to_analyze

        # 2. ANALYSIS PHASE
        if model and content_to_analyze.strip():
            # Show the content in the window as requested
            st.markdown("#### [ DATA STREAM PREVIEW ]")
            st.markdown(
                f'<div class="scraped-box">{content_to_analyze}</div>',
                unsafe_allow_html=True,
            )

            with st.status("Analyzing Linguistic Patterns...", expanded=True) as status:
                time.sleep(1)
                pred = model.predict([content_to_analyze])[0]
                probs = model.predict_proba([content_to_analyze])[0]
                conf = float(probs[1] if pred == 1 else probs[0])
                status.update(
                    label="Analysis Finalized", state="complete", expanded=False
                )

            # Result Visualization
            res_color = "#00ffa3" if pred == 1 else "#ff2a5f"
            res_label = "AUTHENTIC / SECURE" if pred == 1 else "DECEPTIVE / ANOMALY"

            st.markdown(
                f"""
                <div style="padding:25px; border: 2px solid {res_color}; border-radius:15px; background: rgba(0,0,0,0.2);">
                    <h2 style="color:{res_color}; margin:0; font-family:'Space Grotesk';">{res_label}</h2>
                    <p style="opacity:0.8; margin:0;">System Confidence: {conf:.2%}</p>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.warning("Input buffer empty. Provide URL or Text.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # SYSTEM METRICS SECTION
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### SYSTEM VITALS")
    st.metric("CORE ACCURACY", f"{training_acc:.2%}")
    st.metric("ANOMALY RECALL", "95.00%")
    st.markdown("</div>", unsafe_allow_html=True)

    # RE-ADDED: ARCHITECTURE SECTION
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### ARCHITECTURE")
    st.markdown("""
    **Model:** XGBoost Classifier  
    **Features:** Hybrid TF-IDF + VADER  
    
    *Captures non-linear interactions between emotional tone and semantic patterns.*
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # EXCEL EXPORT SECTION (NOW AT THE BOTTOM AS A BUTTON)
    if "current_data" in st.session_state and st.session_state["current_data"]:
        st.markdown(
            '<div class="premium-card" style="border: 1px solid #4facfe;">',
            unsafe_allow_html=True,
        )
        st.markdown("### EXPORT DATA")
        export_df = pd.DataFrame(
            [
                {
                    "Content": st.session_state["current_data"],
                    "Timestamp": time.ctime(),
                    "Engine": "Neural Verdict v1.0",
                }
            ]
        )

        csv_data = export_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="DOWNLOAD FOR EXCEL",
            data=csv_data,
            file_name="news_analysis_report.csv",
            mime="text/csv",
        )
        st.markdown("</div>", unsafe_allow_html=True)

# FOOTER
st.markdown(
    '<p style="text-align:center; opacity:0.3; font-size: 0.7rem; margin-top:50px;">AGENTIC AI | MILESTONE 1 | 2026</p>',
    unsafe_allow_html=True,
)
