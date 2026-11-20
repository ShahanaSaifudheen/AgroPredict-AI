
import streamlit as st
import pandas as pd
import os

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="Crop Comparison | AgroPredict AI",
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
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #d5e5d2;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

st.title("🌾 Crop Productivity Comparison")

st.markdown("""
Compare historical crop productivity across Kerala districts
and explore differences between selected agricultural crops.
""")

st.divider()

# --------------------------------
# LOAD DATA
# --------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "historical_productivity.csv")

df = pd.read_csv(DATA_PATH)

# --------------------------------
# FILTER SECTION
# --------------------------------

st.subheader("🔍 Select Comparison Parameters")

with st.container(border=True):

    col1, col2 = st.columns(2)

    with col1:
        selected_district = st.selectbox(
            "📍 Select District",
            sorted(df["District"].dropna().unique())
        )

    with col2:
        crop_options = sorted(df["Crop"].dropna().unique())

        selected_crops = st.multiselect(
            "🌱 Select Crops to Compare",
            crop_options,
            default=crop_options[:3]
        )

# --------------------------------
# FILTER DATA
# --------------------------------

filtered_df = df[
    (df["District"] == selected_district) &
    (df["Crop"].isin(selected_crops))
]

if not selected_crops:

    st.warning("Please select at least one crop.")

elif filtered_df.empty:

    st.warning("No historical data available for this selection.")

else:

    # --------------------------------
    # COMPARISON CALCULATION
    # --------------------------------

    comparison = (
        filtered_df.groupby("Crop")["Previous_Year_Productivity"]
        .mean()
        .reset_index()
        .rename(columns={
            "Previous_Year_Productivity": "Average Productivity"
        })
        .sort_values(
            "Average Productivity",
            ascending=False
        )
    )

    st.divider()

    st.subheader(f"🌿 Crop Analysis – {selected_district}")

    # --------------------------------
    # METRIC CARDS
    # --------------------------------

    highest_crop = comparison.iloc[0]
    lowest_crop = comparison.iloc[-1]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Crops Compared",
        len(comparison)
    )

    col2.metric(
        "Highest Productivity",
        highest_crop["Crop"],
        f'{highest_crop["Average Productivity"]:,.2f} Kg/Ha'
    )

    col3.metric(
        "Lowest Productivity",
        lowest_crop["Crop"],
        f'{lowest_crop["Average Productivity"]:,.2f} Kg/Ha'
    )

    # --------------------------------
    # BAR CHART
    # --------------------------------

    st.divider()

    st.subheader("📊 Average Productivity Comparison")

    st.bar_chart(
        comparison.set_index("Crop")[
            "Average Productivity"
        ]
    )

    # --------------------------------
    # COMPARISON TABLE
    # --------------------------------

    st.divider()

    st.subheader("📋 Detailed Comparison")

    st.dataframe(
        comparison.style.format({
            "Average Productivity": "{:,.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # INSIGHT
    # --------------------------------

    st.divider()

    st.subheader("💡 Agricultural Insight")

    st.success(
        f'{highest_crop["Crop"]} has the highest average '
        f'previous-year productivity among the selected crops '
        f'in {selected_district}.'
    )

    st.caption(
        "Note: Values represent average previous-year productivity "
        "from the historical lookup dataset, not future predictions."
    )