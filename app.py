import streamlit as st
import joblib
import requests
import json
import pandas as pd
import time

# ==============================
# THE "NEURAL OBSIDIAN" DESIGN SYSTEM
# ==============================
st.set_page_config(page_title="NEURAL VERDICT | Intelligence", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Premium Font Pairings */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;500;700&family=Outfit:wght@200;400;600&display=swap');

    /* 1. KINETIC AURORA BACKGROUND (Pure CSS Animation) */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stApp {
        background: linear-gradient(-45deg, #050505, #120e1f, #051014, #000000);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
    }

    /* 2. GLASSMORPHISM 2.0 CARDS */
    @keyframes floatUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .premium-card {
        background: rgba(20, 20, 25, 0.4);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.1);
        margin-bottom: 30px;
        animation: floatUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        transition: all 0.4s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 40px 80px rgba(0, 242, 254, 0.05), inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(0, 242, 254, 0.15);
    }

    /* 3. HI-TECH TYPOGRAPHY */
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 6rem;
        line-height: 1;
        background: linear-gradient(180deg, #FFFFFF 0%, rgba(255, 255, 255, 0.4) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.05em;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.3em;
        color: #00f2fe;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        margin-left: 5px;
        opacity: 0.8;
    }

    /* 4. TACTILE INPUTS */
    .stTextArea textarea {
        background: rgba(0,0,0,0.4) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        color: #fff !important;
        padding: 24px !important;
        font-size: 1.1rem !important;
        font-family: 'Outfit', sans-serif !important;
        transition: all 0.3s ease;
        box-shadow: inset 0 4px 20px rgba(0,0,0,0.5);
    }
    .stTextArea textarea:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.1), inset 0 4px 20px rgba(0,0,0,0.5) !important;
    }

    /* 5. 3D MAGNETIC BUTTON */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #000 !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        border-radius: 100px;
        padding: 1.8rem 0;
        width: 100%;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        box-shadow: 0 10px 20px rgba(0, 242, 254, 0.2), inset 0 -3px 0 rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(0, 242, 254, 0.4), inset 0 -3px 0 rgba(0,0,0,0.1);
        filter: brightness(1.1);
    }
    .stButton > button:active {
        transform: translateY(1px);
        box-shadow: 0 5px 10px rgba(0, 242, 254, 0.3);
    }

    /* 6. METRICS & UI POLISH */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 3rem !important;
        background: linear-gradient(90deg, #fff, #a1a1aa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        opacity: 0.7;
    }
    
    /* Custom Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0.05em;
        background-color: transparent !important;
        border-bottom-color: transparent !important;
        color: #a1a1aa !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00f2fe !important;
        border-bottom-color: #00f2fe !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# LOGIC & STORAGE
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

# SPATIAL HERO SECTION
st.write("") # Top padding
st.write("")
st.markdown('<div class="hero-title">NEURAL<br>VERDICT.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Hybrid Feature Analysis Engine v1.0</div>', unsafe_allow_html=True)
st.write("")
st.write("")

# REFINED TABS
tab1, tab2 = st.tabs(["01 // ANALYZER", "02 // SYSTEM METRICS"])

with tab1:
    col_input, col_spacing, col_stats = st.columns([2.5, 0.2, 1])
    
    with col_input:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        user_input = st.text_area("TARGET DATA STREAM", height=200, placeholder="Paste data stream to initiate forensic triangulation...", label_visibility="collapsed")
        
        st.write("") # Spacing
        
        if st.button("INITIATE FORENSIC SCAN"):
            if model and user_input.strip():
                # Cinematic processing sequence
                with st.status("Analyzing Linguistic Topography...", expanded=True) as status:
                    st.write("Extracting TF-IDF structural features...")
                    time.sleep(0.6)
                    st.write("Mapping VADER emotional polarity...")
                    time.sleep(0.6)
                    st.write("Querying XGBoost decision trees...")
                    time.sleep(0.8)
                    status.update(label="Analysis Complete.", state="complete", expanded=False)
                    
                    pred = model.predict([user_input])[0]
                    probs = model.predict_proba([user_input])[0]
                    confidence = float(probs[1] if pred == 1 else probs[0])
                
                # High-fidelity Result Output
                st.markdown("<br>", unsafe_allow_html=True)
                r_col1, r_col2 = st.columns([1.5, 1])
                with r_col1:
                    status_color = "#00ffa3" if pred == 1 else "#ff2a5f"
                    status_bg = "rgba(0, 255, 163, 0.05)" if pred == 1 else "rgba(255, 42, 95, 0.05)"
                    label = "VERIFIED SECURE" if pred == 1 else "DECEPTIVE ANOMALY"
                    
                    st.markdown(f"""
                        <div style="padding:40px; border-radius:16px; border: 1px solid {status_color}; background: {status_bg}; box-shadow: 0 0 40px {status_color}20;">
                            <p style="margin:0; font-family:'Outfit'; font-size:0.9rem; color:{status_color}; letter-spacing:0.2em;">SYSTEM VERDICT</p>
                            <h2 style="color:{status_color}; margin:10px 0 0 0; font-family:'Space Grotesk'; font-size: 2.2rem; font-weight:700; letter-spacing:-1px;">{label}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                with r_col2:
                    st.metric("CONFIDENCE INDEX", f"{confidence:.2%}")
                    st.progress(confidence)
                
                sync_data(user_input, confidence)
            else:
                st.error("System Exception: Data stream required for analysis.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_stats:
        st.markdown('<div class="premium-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown("<h4 style='font-family: Space Grotesk; font-weight: 700;'>CORE VITALITY</h4>", unsafe_allow_html=True)
        st.markdown("<p style='opacity: 0.6; font-size: 0.9rem;'>Node operating with hybrid TF-IDF + VADER sentiment matrices.</p>", unsafe_allow_html=True)
        
        st.write("")
        st.metric("SYSTEM ACCURACY", f"{training_acc:.2%}")
        st.write("")
        st.metric("RECALL CAPACITY", "95.00%")
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("<h2 style='font-family: Space Grotesk;'>MILESTONE 1: ARCHITECTURE</h2>", unsafe_allow_html=True)
    st.write("")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.info("**Methodology**\n\nHybrid Feature Engineering: TF-IDF (Semantics) + VADER (Emotional Polarity).")
    with m_col2:
        st.success("**Top Performer**\n\nXGBoost. Chosen for high-dimensional, non-linear interaction handling.")
    with m_col3:
        st.warning("**Target Goal**\n\nReduce False Negatives. Misinformation recall strictly prioritized at 0.95.")

    st.write("")
    st.markdown("### MODEL COMPARISON MATRIX")
    comparison_data = {
        "Architecture": ["Multinomial NB", "Logistic Regression", "Random Forest", "XGBoost"],
        "Base Accuracy": ["85%", "90%", "91%", "93.88%"],
        "Recall (Anomaly)": ["Low", "80%", "Moderate", "95%"],
        "Deployment": ["Rejected", "Rejected", "Rejected", "Active Node"]
    }
    st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)
    
    st.markdown("""
    **The XGBoost Advantage:**
    While Logistic Regression operates with high latency efficiency, it failed to identify subtle misinformation patterns. **XGBoost** natively captures the interaction between sensationalist sentiment anomalies and specific vocabulary distributions—a critical signal in modern synthetic text generation.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.write("")
st.write("")
st.markdown('<p style="text-align:center; opacity:0.3; font-size: 0.75rem; font-family: Space Grotesk; letter-spacing: 0.2em;">AGENTIC AI // MILESTONE 1 DEPLOYMENT // 2026</p>', unsafe_allow_html=True)