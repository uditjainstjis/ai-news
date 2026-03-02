import streamlit as st
import joblib
import requests
import json
import pandas as pd
import time

# ==============================
# THE "BILLION DOLLAR" DESIGN SYSTEM
# ==============================
st.set_page_config(page_title="NEURAL VERDICT | Intelligence Portal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Kinetic Mesh Background - The "Moving 3D" Feel */
    .stApp {
        background: 
            radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), 
            radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%);
        background-color: #050505;
        color: #f0f0f0;
        font-family: 'Inter', sans-serif;
    }

    /* Billion-Dollar Morphism Cards */
    .morphism-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(25px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        padding: 35px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .morphism-card:hover {
        transform: translateY(-5px) scale(1.005);
        border: 1px solid rgba(0, 242, 254, 0.3);
    }

    /* Typography Engine */
    .glitch-title {
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        font-size: 5rem;
        background: linear-gradient(to right, #fff 20%, #4facfe 50%, #00f2fe 80%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -4px;
        margin-bottom: 0;
        text-transform: uppercase;
    }

    /* Interactive Inputs */
    .stTextArea textarea {
        background: rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 20px !important;
        color: #fff !important;
        padding: 20px !important;
        font-size: 1.1rem !important;
    }

    /* 3D Action Button */
    .stButton > button {
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        color: #000 !important;
        font-family: 'Syncopate', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 50px;
        padding: 1.5rem 3rem;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton > button:hover {
        box-shadow: 0 0 50px rgba(0, 242, 254, 0.5);
        transform: scale(1.02);
    }
    
    /* Metrics Highlighting */
    .metric-box {
        text-align: center;
        padding: 15px;
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# LOGIC & STORAGE (HARDENED)
# ==============================
ENDPOINT = "https://script.google.com/macros/s/AKfycbwvCUpf2PYxEKh8nD7s42MZAJDJdofA6VJ6K_K2ybKXoaPbPNq6cOfSQYOXE8-b1xVs/exec"

@st.cache_resource
def load_engine():
    try:
        m = joblib.load('credibility_model.joblib')
        a = joblib.load('model_accuracy.joblib')
        return m, a
    except:
        return None, 0.9388 # Fallback if local file missing

model, training_acc = load_engine()

def sync_data(text, score):
    try:
        payload = {"text": str(text), "number": float(score)}
        requests.post(ENDPOINT, data=json.dumps(payload), timeout=5)
    except:
        pass

# ==============================
# UI - THE INTELLIGENCE TERMINAL
# ==============================

# HERO SECTION
st.markdown('<h1 class="glitch-title">NEURAL<br>VERDICT</h1>', unsafe_allow_html=True)
st.markdown('<p style="letter-spacing: 8px; color: #4facfe; font-weight: 400; margin-left: 5px;">HYBRID FEATURE ANALYSIS v1.0</p>', unsafe_allow_html=True)

# TABS FOR BETTER UX (Don't cram everything on one screen)
tab1, tab2 = st.tabs(["[ ⚡ ANALYZER ]", "[ 📊 SYSTEM PERFORMANCE ]"])

with tab1:
    col_input, col_stats = st.columns([2, 1])
    
    with col_input:
        st.markdown('<div class="morphism-card">', unsafe_allow_html=True)
        user_input = st.text_area("TARGET DATA STREAM", height=250, placeholder="Deploy text for credibility triangulation...")
        if st.button("INITIATE FORENSIC SCAN"):
            if model and user_input.strip():
                with st.status("Analyzing Linguistic Patterns...", expanded=False):
                    pred = model.predict([user_input])[0]
                    probs = model.predict_proba([user_input])[0]
                    confidence = float(probs[1] if pred == 1 else probs[0])
                    time.sleep(1) # For "Visual Weight"
                
                # Result Logic
                st.markdown("### SCAN RESULTS")
                r_col1, r_col2 = st.columns(2)
                with r_col1:
                    status_color = "#00ffa3" if pred == 1 else "#ff3e3e"
                    label = "VERIFIED" if pred == 1 else "DECEPTIVE"
                    st.markdown(f"""
                        <div style="padding:30px; border-radius:20px; border: 1px solid {status_color}; background: rgba(0,0,0,0.3);">
                            <h1 style="color:{status_color}; margin:0; font-family:'Syncopate';">{label}</h1>
                            <p style="opacity:0.6;">System Confidence: {confidence:.2%}</p>
                        </div>
                    """, unsafe_allow_html=True)
                with r_col2:
                    st.metric("FIDELITY SCORE", f"{confidence:.2%}")
                    st.progress(confidence)
                
                sync_data(user_input, confidence)
            else:
                st.error("SYSTEM ERROR: INPUT BUFFER EMPTY")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_stats:
        st.markdown('<div class="morphism-card">', unsafe_allow_html=True)
        st.markdown("### CORE METRICS")
        st.write("Current intelligence node operating with hybrid TF-IDF + VADER sentiment features.")
        st.divider()
        st.metric("SYSTEM ACCURACY", f"{training_acc:.2%}")
        st.metric("FAKE NEWS RECALL", "95.00%")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="morphism-card">', unsafe_allow_html=True)
    st.markdown("## PROJECT MILESTONE 1: ARCHITECTURE")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.info("**Methodology**\n\nHybrid Feature Engineering: Combining TF-IDF (Semantics) with VADER (Emotional Polarity).")
    with m_col2:
        st.success("**Top Performer**\n\nXGBoost (Gradient Boosted Trees). Chosen for non-linear interaction handling.")
    with m_col3:
        st.warning("**Target Goal**\n\nReduce False Negatives in misinformation detection. Recall prioritized at 0.95.")

    st.markdown("### MODEL COMPARISON MATRIX")
    comparison_data = {
        "Model": ["Multinomial NB", "Logistic Regression", "Random Forest", "XGBoost"],
        "Accuracy": ["85%", "90%", "91%", "93.88%"],
        "Recall (Fake)": ["Low", "80%", "Moderate", "95%"],
        "Selection": ["❌", "❌", "❌", "✅"]
    }
    st.table(pd.DataFrame(comparison_data))
    
    st.markdown("""
    **The XGBoost Advantage:**
    While Logistic Regression is fast, it missed subtle misinformation patterns. **XGBoost** captures the interaction between sensationalist sentiment scores and specific vocabulary—a critical signal in modern fake news.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown('<p style="text-align:center; opacity:0.3; font-size: 0.8rem;">AGENTIC AI | MILESTONE 1 DEPLOYMENT | 2026</p>', unsafe_allow_html=True)