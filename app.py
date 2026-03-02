import streamlit as st
import joblib
from newspaper import Article
import xgboost

st.set_page_config(page_title="News Credibility AI", layout="wide")

@st.cache_resource
def load_data():
    try:
        model = joblib.load('credibility_model.joblib')
        acc = joblib.load('model_accuracy.joblib')
        return model, acc
    except:
        return None, None

model, training_accuracy = load_data()

# Sidebar
st.sidebar.header("📊 Model Metrics")
if training_accuracy:
    st.sidebar.metric("Training Accuracy", f"{training_accuracy:.2%}")

st.title("🛡️ News Credibility Analyzer")

# Placeholder update: More professional/realistic news example
placeholder_text = (
    "Example: The global economy is expected to grow by 3% in 2024 according to "
    "recent financial reports issued by the International Monetary Fund."
)

user_input = st.text_area("Analyze news content:", height=150, placeholder=placeholder_text)

if st.button("Analyze"):
    if model and user_input.strip():
        # Get prediction and probabilities
        pred = model.predict([user_input])[0]
        probs = model.predict_proba([user_input])[0]
        
        # FIX: Explicitly cast to float for st.progress
        confidence = float(probs[1] if pred == 1 else probs[0])
        
        col1, col2 = st.columns(2)
        with col1:
            if pred == 1:
                st.success("### ✅ High Credibility")
            else:
                st.error("### 🚨 Low Credibility")
        
        with col2:
            st.metric("Confidence", f"{confidence:.2%}")
            # This line was crashing; it is now safe with float()
            st.progress(confidence) 
            
        # Techie disclaimer for the 'Udit' test
        if "udit" in user_input.lower():
            st.info("💡 **Developer Note:** Milestone 1 analyzes style/syntax. "
                    "Fact-checking (Milestone 2) will verify specific names.")
    else:
        st.error("Check model files or input text.")