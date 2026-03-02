import streamlit as st
import joblib
import pandas as pd
from newspaper import Article

# Load the model pipeline
# Ensure this file is in the same directory as app.py
try:
    model = joblib.load('credibility_model.joblib')
except Exception as e:
    st.error(f"Could not load model file. Error: {e}")

st.set_page_config(page_title="News Credibility AI", page_icon="🛡️")
st.title("🛡️ News Credibility Analyzer")

# Input Section
input_type = st.radio("Select Input Method:", ["Article URL", "Raw Text"])

text_to_analyze = ""

if input_type == "Article URL":
    url = st.text_input("Paste the news URL here:")
    if url:
        with st.spinner('Extracting article content...'):
            try:
                article = Article(url)
                article.download()
                article.parse()
                text_to_analyze = article.text
                st.info(f"**Extracted Title:** {article.title}")
            except Exception as e:
                st.error(f"Failed to extract text. Error: {e}")

else:
    text_to_analyze = st.text_area("Paste the full article text here:", height=300)

# Prediction Logic
if st.button("Analyze Credibility"):
    if text_to_analyze.strip():
        # The model expects a list/array of strings
        prediction = model.predict([text_to_analyze])[0]
        
        # Based on WELFake dataset: 1 = Real, 0 = Fake
        if prediction == 1:
            st.success("### ✅ High Credibility\nThis article matches patterns of reliable news.")
        else:
            st.error("### 🚨 Low Credibility\nWarning: This article shows signals of potential misinformation.")
            
        st.write("---")
        st.subheader("Extracted Content Preview")
        st.write(text_to_analyze[:500] + "...")
    else:
        st.warning("Please provide a URL or text content first.")