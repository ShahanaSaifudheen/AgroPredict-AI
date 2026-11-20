
import streamlit as st
import joblib
import os

st.set_page_config(
    page_title="AgroPredict AI",
    page_icon="🌾",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best_model.pkl")

# Load model
try:
    artifact = joblib.load(MODEL_PATH)
    model = artifact["model"]
    preprocessor = artifact["preprocessor"]
    model_loaded = True
except Exception:
    model_loaded = False

# Agriculture theme CSS
st.markdown("""
<style>
.stApp {
    background-color: #f1f7ed;
}

[data-testid="stSidebar"] {
    background-color: #143d25;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: #174d2a;
}

.subtitle {
    color: #52745b;
    font-size: 19px;
}

.hero {
    background: linear-gradient(90deg, #143d25, #387849);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-top: 15px;
}

.hero h1 {
    color: white;
    font-size: 38px;
}

.hero p {
    color: #e5f3e6;
    font-size: 17px;
}

[data-testid="stMetric"] {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #d5e5d2;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

h2, h3 {
    color: #205b32;
}

</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="main-title">🌾 AgroPredict AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart Agriculture | Kerala Crop Productivity Prediction</div>',
    unsafe_allow_html=True
)

# Hero section
st.markdown("""
<div class="hero">
    <h1>Growing Smarter with Artificial Intelligence</h1>
    <p>
    Discover agricultural insights, compare crop productivity
    and predict future productivity using Machine Learning.
    </p>
</div>
""", unsafe_allow_html=True)

# Hero image
st.image(
    "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1600",
    use_container_width=True
)

st.divider()

# Overview
st.header("🌱 Agricultural Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Dataset", "Kerala EARAS")
c2.metric("Districts", "14")
c3.metric("Best Model", "Decision Tree")
c4.metric("Model R² Score", "78.55%")

st.divider()

# Features
st.header("🌿 Explore Our Platform")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 📊 Exploratory Data Analysis
    Understand Kerala's agricultural patterns through data.

    ### 🌾 Crop Comparison
    Compare historical productivity across districts.
    """)

with col2:
    st.markdown("""
    ### 🤖 Crop Productivity Prediction
    Estimate productivity using machine learning.

    ### 📈 Model Performance
    Explore model evaluation and comparison results.
    """)

st.divider()

# System status
st.header("⚙️ System Status")

if model_loaded:
    st.success("AgroPredict AI prediction model is ready.")
else:
    st.error("Model file not found or unable to load.")

st.markdown("""
<div style="
text-align:center;
background:#143d25;
color:white;
padding:25px;
border-radius:12px;
margin-top:25px;">

<h3 style="color:white;">🌾 AgroPredict AI</h3>
Smart Agriculture for a Better Tomorrow<br>
Kerala Crop Productivity Prediction System

</div>
""", unsafe_allow_html=True)