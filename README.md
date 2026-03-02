PROJECT 11: Intelligent News Credibility Analysis
From Predictive NLP to Autonomous Fact-Checking
Streamlit AppPython 3.9License: MIT

🎯 Project Overview
This project is an AI-driven content analytics system designed to evaluate the credibility of news articles. Developed as part of the Intro to GenAI course, this system currently fulfills Milestone 1 by using classical Machine Learning and NLP techniques to classify news as "Credible" or "Misinformation."

The system evolves beyond simple text classification by incorporating Hybrid Feature Engineering (combining linguistic patterns with emotional sentiment) and Live URL Scraping capabilities.

🏗️ System Architecture (Milestone 1)
The current architecture follows a robust ML Pipeline:

Input Module: Accepts raw text or URL (scraped via newspaper3k).
Preprocessing: Text cleaning, stop-word removal, and normalization.
Feature Engineering:
TF-IDF Vectorization: Captures the importance of specific words/n-grams.
Sentiment Analysis (VADER): Measures emotional tone (Fake news often exhibits extreme sentiment).
Stylistic Features: Analyzes text length and structure.
Prediction Engine: XGBoost Classifier trained on a hybrid feature set.
Output: Binary classification (Real/Fake) with confidence score.

🚀 Key Features
High Accuracy Classification: Achieves 94% accuracy using an XGBoost model trained on hybrid features.
URL Support: Users can paste a news article URL; the system automatically scrapes and analyzes the content.
Sentiment Analysis: Integrates VADER sentiment analysis to detect sensationalism, a common trait in misinformation.
Interactive UI: Built with Streamlit for ease of use and real-time analysis.
Public Deployment: Hosted live on Streamlit Community Cloud.

🛠️ Tech Stack & Tools
Component	Technology
Language	Python 3.9+
ML Framework	Scikit-Learn, XGBoost
NLP	NLTK (Stopwords), VADER (Sentiment)
Feature Extraction	TF-IDF Vectorizer
Web Scraping	Newspaper3k
UI Framework	Streamlit
Deployment	Streamlit Community Cloud
Environment	Google Colab (Training), VS Code (Dev)

📊 Model Performance
The model was evaluated on a test split of news articles. The hybrid approach (TF-IDF + Sentiment) proved highly effective.

Overall Accuracy: 93.88%

Metric	Class 0 (Real)	Class 1 (Fake)
Precision	0.96	0.91
Recall	0.93	0.95
F1-Score	0.94	0.93
Key Insight: The model maintains a high recall (0.95) for Fake News, meaning it successfully catches 95% of misinformation attempts.

📁 Project Structure
├── app.py # Streamlit Application Script
├── xgb_credibility_model.pkl # Trained XGBoost Model
├── tfidf_vectorizer.pkl # Fitted TF-IDF Vectorizer
├── cleaned_news.csv # Dataset used for training
├── requirements.txt # Python dependencies
└── README.md # Project Documentation

Shobhit- Research & Data Analysis
Vaidehi Sahu- Model Training & documentation
Udit Jain- UI & Deployment

