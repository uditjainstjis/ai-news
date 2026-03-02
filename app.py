import streamlit as st
import joblib
import requests
import xgboost
import json

# ==============================
# THE $1B VISUAL ENGINE (CSS)
# ==============================
st.set_page_config(page_title="NEURAL VERDICT PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Space+Grotesk:wght@300;500;700&display=swap');

    /* Kinetic Mesh Background */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0f0f1a 100%);
        background-attachment: fixed;
    }

    /* Floating Glassmorphism Container */
    .glass-container {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-top: 20px;
    }

    /* 3D Moving Title */
    .hero-text {
        font-family: 'Syncopate', sans-serif;
        font-size: clamp(2rem, 8vw, 5rem);
        background: linear-gradient(90deg, #00f2fe, #4facfe, #7000ff, #00f2fe);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        text-align: center;
        letter-spacing: -3px;
        margin-bottom: 0px;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    /* Neon Button */
    .stButton > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #000 !important;
        font-family: 'Syncopate', sans-serif;
        border: none;
        padding: 20px 40px;
        border-radius: 15px;
        font-weight: 700;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        box-shadow: 0 10px 20px rgba(79, 172, 254, 0.3);
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 0 20px 40px rgba(79, 172, 254, 0.5);
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif;
        color: #00f2fe !important;
        font-size: 2.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# CORE LOGIC (FIXED & TESTED)
# ==============================
ENDPOINT = "https://script.google.com/macros/s/AKfycbwvCUpf2PYxEKh8nD7s42MZAJDJdofA6VJ6K_K2ybKXoaPbPNq6cOfSQYOXE8-b1xVs/exec"

@st.cache_resource
def load_assets():
    try:
        m = joblib.load('credibility_model.joblib')
        a = joblib.load('model_accuracy.joblib')
        return m, a
    except:
        return None, None

model, training_acc = load_assets()

def push_to_sheets(text, score):
    """Restored: Hard-coded JSON structure for your AppScript"""
    payload = {"text": str(text), "number": float(score)}
    try:
        # Standard POST request with proper headers
        r = requests.post(ENDPOINT, data=json.dumps(payload), timeout=5)
        return r.status_code
    except Exception as e:
        return str(e)

# ==============================
# THE INTERFACE
# ==============================
st.markdown('<h1 class="hero-text">NEURAL VERDICT</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:rgba(255,255,255,0.5); font-family:Space Grotesk;">QUANTUM-GRADE NEWS VALIDATION ENGINE</p>', unsafe_allow_html=True)

# Main glass card
st.markdown('<div class="glass-container">', unsafe_allow_html=True)

user_input = st.text_area(
    "FEED DATA STREAM",
    height=200,
    placeholder="Paste news content here..."
)

col_btn, col_space = st.columns([1, 2])
with col_btn:
    analyze_trigger = st.button("RUN FORENSIC SCAN")

if analyze_trigger:
    if model and user_input.strip():
        # ML Logic
        pred = model.predict([user_input])[0]
        probs = model.predict_proba([user_input])[0]
        confidence = float(probs[1] if pred == 1 else probs[0])
        
        # UI Feedback
        c1, c2 = st.columns(2)
        with c1:
            if pred == 1:
                st.markdown("<h2 style='color:#00ffa3;'>✅ VERIFIED AUTHENTIC</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color:#ff3e3e;'>🚨 SYNTHETIC/FALSE</h2>", unsafe_allow_html=True)
        
        with c2:
            st.metric("CONFIDENCE", f"{confidence:.2%}")
            st.progress(confidence)

        status_code = push_to_sheets(user_input, confidence)
    else:
        st.warning("SYSTEM READY: Waiting for Input Stream.")

st.markdown('</div>', unsafe_allow_html=True)

# Sidebar / Background Metrics
with st.sidebar:
    st.markdown("### SYSTEM METRICS")
    if training_acc:
        st.metric("MODEL FIDELITY", f"{training_acc:.2%}")
    st.markdown("---")
    st.caption("Active Node: 0x99-ALPHA")