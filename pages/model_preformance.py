
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Model Performance | AgroPredict AI",
    page_icon="🌾",
    layout="wide"
)

# ---------------- PAGE THEME ----------------

st.markdown("""
<style>
.stApp {
    background-color: #f1f7ed;
}

section[data-testid="stSidebar"] {
    background-color: #143d25;
}

section[data-testid="stSidebar"] * {
    color: white;
}

h1, h2, h3 {
    color: #205b32;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 22px;
    border-radius: 12px;
    border-left: 5px solid #438b50;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

hr {
    border-color: #c9ddc4;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("🌾 Model Performance")

st.markdown("""
Evaluate the performance of machine learning models
trained for Kerala crop productivity prediction.
""")

# ---------------- BEST MODEL ----------------

st.subheader("🏆 Best Model: Decision Tree Regressor")

col1, col2, col3 = st.columns(3)

col1.metric("R² Score", "78.55%")
col2.metric("MAE", "1,295.17")
col3.metric("RMSE", "5,363.31")

st.success(
    "The Decision Tree model achieved an R² score of 0.7855 "
    "on the final test dataset."
)

st.divider()

# ---------------- MODEL COMPARISON ----------------

st.subheader("📊 Machine Learning Model Comparison")

results = pd.DataFrame({
    "Model": [
        "Decision Tree",
        "Extra Trees",
        "Random Forest",
        "Linear Regression",
        "Gradient Boosting"
    ],
    "MAE": [
        1290.512,
        1360.685,
        1514.104,
        3255.311,
        2860.137
    ],
    "RMSE": [
        4403.094,
        6036.323,
        7014.460,
        12093.990,
        20675.984
    ],
    "R2 Score": [
        0.864,
        0.744,
        0.655,
        -0.026,
        -1.998
    ]
})

st.dataframe(
    results.style.format({
        "MAE": "{:,.3f}",
        "RMSE": "{:,.3f}",
        "R2 Score": "{:.3f}"
    }),
    use_container_width=True,
    hide_index=True
)

# ---------------- VALIDATION NOTE ----------------

st.caption(
    "Note: Comparison scores are validation results. "
    "Best model metrics above are from the final test dataset."
)

st.divider()

# ---------------- FOOTER ----------------

st.markdown("""
<div style="text-align:center; color:#52745a; padding:15px;">
    🌱 AgroPredict AI | Machine Learning Model Evaluation
</div>
""", unsafe_allow_html=True)