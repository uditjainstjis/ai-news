import streamlit as st
import joblib
from newspaper import Article
import xgboost

st.set_page_config(page_title="News Credibility AI", layout="wide")

# Load artifacts
@st.cache_resource
def load_data():
    try:
        model = joblib.load('credibility_model.joblib')
        acc = joblib.load('model_accuracy.joblib')
        return model, acc
    except:
        return None, None

model, training_accuracy = load_data()

# Sidebar for the "Sir/Professor" View
st.sidebar.header("📊 Model Evaluation")
if training_accuracy:
    st.sidebar.metric("System Accuracy", f"{training_accuracy:.2%}")
    st.sidebar.write("**Model:** XGBoost Classifier")
    st.sidebar.write("**Feature Engine:** TF-IDF Vectorizer")
    st.sidebar.info("This model analyzes linguistic patterns to determine credibility.")
else:
    st.sidebar.warning("Upload model files to GitHub to see metrics.")

st.title("🛡️ Intelligent News Credibility Analysis")
st.markdown("---")

# User Input
input_text = st.text_area("Analyze news content or a statement:", height=150, 
                          placeholder="e.g., Is Udit the PM of India?")

if st.button("Analyze Credibility"):
    if not model:
        st.error("Model files not found on server.")
    elif not input_text.strip():
        st.warning("Please enter some text.")
    else:
        # Prediction
        pred = model.predict([input_text])[0]
        probs = model.predict_proba([input_text])[0]
        confidence = probs[1] if pred == 1 else probs[0]
        
        # UI Display
        col1, col2 = st.columns(2)
        with col1:
            if pred == 1:
                st.success("### ✅ High Credibility Pattern")
                st.write("The text structure matches reliable news sources.")
            else:
                st.error("### 🚨 Low Credibility Signal")
                st.write("Warning: This text matches patterns often found in misinformation.")
        
        with col2:
            st.metric("Model Confidence", f"{confidence:.2%}")
            st.progress(confidence)

        # Techie explanation for the PM question
        if "udit" in input_text.lower():
            st.info("**Note for User:** Milestone 1 detects *how* something is written. "
                    "Since this sentence is grammatically clean, the model sees it as 'Real Style'. "
                    "Fact-checking (Milestone 2) will verify the actual names.")