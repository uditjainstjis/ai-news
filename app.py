import streamlit as st
import joblib
from newspaper import Article
import xgboost

st.set_page_config(page_title="News Credibility AI", page_icon="🛡️")

@st.cache_resource
def load_model():
    try:
        return joblib.load('credibility_model.joblib')
    except Exception as e:
        st.error(f"Model Load Error: {e}")
        return None

model = load_model()

st.title("🛡️ News Credibility Analyzer")

# Input section
choice = st.radio("Input Method:", ("URL", "Paste Text"))
input_text = ""

if choice == "URL":
    url = st.text_input("Link:")
    if url:
        try:
            article = Article(url)
            article.download()
            article.parse()
            input_text = article.text
            st.info(f"Analyzing: {article.title}")
        except:
            st.error("Failed to parse URL.")
else:
    input_text = st.text_area("Content:", height=200)

# Prediction
if st.button("Check Credibility"):
    if model is None:
        st.error("Model file missing or corrupted.")
    elif not input_text.strip():
        st.warning("No text provided.")
    else:
        # Predict using the bundled pipeline
        prediction = model.predict([input_text])[0]
        
        if prediction == 1:
            st.success("### ✅ High Credibility")
        else:
            st.error("### 🚨 Low Credibility / Fake News Risk")