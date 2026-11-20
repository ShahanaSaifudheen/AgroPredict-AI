
import streamlit as st
import pandas as pd
import joblib
import os

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="Crop Prediction | AgroPredict AI",
    page_icon="🌾",
    layout="wide"
)

# --------------------------------
# AGRICULTURE THEME
# --------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #f1f7ed;
}

h1, h2, h3 {
    color: #205b32;
}

[data-testid="stSidebar"] {
    background-color: #143d25;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

[data-testid="stMetric"] {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #d5e5d2;
}

.result-box {
    background: linear-gradient(120deg, #174d2a, #43864d);
    color: white;
    padding: 25px;
    border-radius: 16px;
    text-align: center;
}

.result-box h2 {
    color: white;
}

.result-value {
    font-size: 34px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

st.title("🌱 Crop Productivity Prediction")

st.markdown("""
Estimate crop productivity across Kerala using
historical agricultural data and Machine Learning.
""")

st.divider()

# --------------------------------
# LOAD MODEL AND DATA
# --------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "best_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "historical_productivity.csv")

artifact = joblib.load(MODEL_PATH)

model = artifact["model"]
preprocessor = artifact["preprocessor"]

history_data = pd.read_csv(DATA_PATH)

# --------------------------------
# INPUT SECTION
# --------------------------------

st.subheader("🚜 Enter Agricultural Details")

st.write("Provide the following details to estimate productivity.")

districts = [
    "Thiruvananthapuram", "Kollam", "Pathanamthitta",
    "Alappuzha", "Kottayam", "Idukki", "Ernakulam",
    "Thrissur", "Palakkad", "Malappuram",
    "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
]

crops = [
    "Paddy", "Banana", "Coconut", "Tapioca",
    "Pepper", "Ginger", "Turmeric", "Rubber",
    "Arecanut", "Cashew", "Cocoa", "Coffee",
    "Cardamom", "Jack", "Mango", "Pineapple",
    "Plantain", "Nutmeg", "Tea", "Betel leaves",
    "Cloves", "Pappaya"
]

with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:
        district = st.selectbox(
            "📍 Select District",
            districts
        )

        crop = st.selectbox(
            "🌾 Select Crop",
            crops
        )

    with col2:
        year = st.number_input(
            "📅 Agriculture Year",
            min_value=2001,
            max_value=2030,
            value=2024
        )

        area = st.number_input(
            "🌱 Cultivated Area (Hectare)",
            min_value=0.01,
            value=10.0,
            step=1.0
        )

    predict_button = st.button(
        "🌿 Predict Productivity",
        type="primary",
        use_container_width=True
    )

# --------------------------------
# PREDICTION
# --------------------------------

if predict_button:

    previous_data = history_data[
        (history_data["Year"] == int(year)) &
        (history_data["District"] == district) &
        (history_data["Crop"] == crop)
    ]

    if previous_data.empty:

        st.warning(
            "Previous year productivity data is not available "
            "for this District and Crop combination."
        )

    else:

        previous_productivity = previous_data[
            "Previous_Year_Productivity"
        ].iloc[0]

        input_data = pd.DataFrame({
            "District": [district],
            "Crop": [crop],
            "Year": [int(year)],
            "Area": [area],
            "Previous_Year_Productivity": [
                previous_productivity
            ]
        })

        processed_data = preprocessor.transform(input_data)

        prediction = model.predict(processed_data)[0]

        # --------------------------------
        # RESULT
        # --------------------------------

        st.divider()
        st.subheader("🌾 Prediction Results")

        st.markdown(f"""
        <div class="result-box">
            <h2>Predicted Crop Productivity</h2>
            <div class="result-value">
                {prediction:,.2f} Kg/Hectare
            </div>
            <p>Machine Learning Prediction Result</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        col1, col2 = st.columns(2)

        col1.metric(
            "Previous Year Productivity",
            f"{previous_productivity:,.2f} Kg/Hectare"
        )

        col2.metric(
            "Predicted Productivity",
            f"{prediction:,.2f} Kg/Hectare",
            delta=f"{prediction - previous_productivity:,.2f}"
        )

        # --------------------------------
        # INPUT SUMMARY
        # --------------------------------

        st.divider()
        st.subheader("📋 Agricultural Input Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("District", district)
        c2.metric("Crop", crop)
        c3.metric("Year", int(year))
        c4.metric("Cultivated Area", f"{area} Ha")

        # --------------------------------
        # PRODUCTIVITY COMPARISON
        # --------------------------------

        st.divider()
        st.subheader("📊 Productivity Comparison")

        comparison_df = pd.DataFrame({
            "Productivity Type": [
                "Previous Year",
                "Predicted"
            ],
            "Productivity": [
                previous_productivity,
                prediction
            ]
        })

        st.bar_chart(
            comparison_df.set_index("Productivity Type")
        )

        difference = prediction - previous_productivity

        if difference > 0:
            st.success(
                f"Predicted productivity is higher by "
                f"{difference:,.2f} Kg/Hectare."
            )
        elif difference < 0:
            st.warning(
                f"Predicted productivity is lower by "
                f"{abs(difference):,.2f} Kg/Hectare."
            )
        else:
            st.info("Predicted productivity is unchanged.")

        st.caption(
            "Note: This is an ML-based estimate, "
            "not a guaranteed agricultural outcome."
        )
