import streamlit as st
import joblib
import requests
import xgboost

# ==============================
# CONFIG
# ==============================
ANALYTICS_ENDPOINT = "https://script.google.com/macros/s/AKfycbwvCUpf2PYxEKh8nD7s42MZAJDJdofA6VJ6K_K2ybKXoaPbPNq6cOfSQYOXE8-b1xVs/exec"

st.set_page_config(page_title="News Credibility AI", layout="wide")

# ==============================
# LOAD MODEL
# ==============================
@st.cache_resource
def load_data():
    try:
        model = joblib.load('credibility_model.joblib')
        acc = joblib.load('model_accuracy.joblib')
        return model, acc
    except:
        return None, None

model, training_accuracy = load_data()

# ==============================
# SILENT LOGGER
# ==============================
def log_usage(text, number):
    try:
        requests.post(
            ANALYTICS_ENDPOINT,
            json={
                "text": text,        # MATCHES YOUR SCRIPT
                "number": number     # MATCHES YOUR SCRIPT
            },
            timeout=2
        )
    except:
        pass  # never break UX

# ==============================
# UI
# ==============================
st.sidebar.header("📊 Model Metrics")
if training_accuracy:
    st.sidebar.metric("Training Accuracy", f"{training_accuracy:.2%}")

st.title("🛡️ News Credibility Analyzer")

placeholder_text = (
    "Example: The global economy is expected to grow by 3% in 2024 "
    "according to recent financial reports."
)

user_input = st.text_area(
    "Analyze news content:",
    height=150,
    placeholder=placeholder_text
)

if st.button("Analyze"):
    if model and user_input.strip():

        pred = model.predict([user_input])[0]
        probs = model.predict_proba([user_input])[0]
        confidence = float(probs[1] if pred == 1 else probs[0])

        col1, col2 = st.columns(2)

        with col1:
            if pred == 1:
                st.success("### ✅ High Credibility")
            else:
                st.error("### 🚨 Low Credibility")

        with col2:
            st.metric("Confidence", f"{confidence:.2%}")
            st.progress(confidence)

        # 🔥 Send EXACT expected fields
        log_usage(user_input, confidence)

    else:
        st.error("Check model files or input text.")