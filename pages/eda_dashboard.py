
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="EDA Dashboard | AgroPredict AI",
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
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #438b50;
}

div[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

.stPlotlyChart, div[data-testid="stImage"] {
    border-radius: 12px;
}

hr {
    border-color: #c9ddc4;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("🌾 Exploratory Data Analysis")

st.markdown("""
Explore Kerala's agricultural dataset through visualizations
and understand crop distribution, productivity, and production patterns.
""")

# ---------------- LOAD DATASET ----------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "kerala_earas_dataset.csv")

df = pd.read_csv(DATA_PATH)

# ---------------- DATASET OVERVIEW ----------------

st.subheader("📋 Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Records", f"{len(df):,}")
col2.metric("Total Districts", df["District"].nunique())
col3.metric("Total Crops", df["Crop"].nunique())

st.divider()

# ---------------- DATASET PREVIEW ----------------

st.subheader("📑 Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)

# ---------------- MISSING VALUES ----------------

st.subheader("🔍 Missing Values Analysis")

missing = df.isnull().sum().reset_index()
missing.columns = ["Column", "Missing Values"]

st.dataframe(
    missing,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- CROP DISTRIBUTION ----------------

st.subheader("🌾 Crop Distribution")

crop_counts = df["Crop"].value_counts().head(15)

fig, ax = plt.subplots(figsize=(10, 5))

crop_counts.plot(
    kind="bar",
    ax=ax,
    color="#438b50"
)

ax.set_xlabel("Crop")
ax.set_ylabel("Number of Records")
ax.set_title("Top 15 Crops by Record Count")
ax.tick_params(axis="x", rotation=45)

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------- YEAR-WISE PRODUCTIVITY TREND ----------------

st.divider()

st.subheader("📈 Year-wise Average Productivity Trend")

year_col = "Agriculture Year"

year_df = df.copy()

year_df["Year"] = pd.to_numeric(
    year_df[year_col].astype(str).str.extract(r"^(\d{4})")[0],
    errors="coerce"
)

year_df["Productivity"] = pd.to_numeric(
    year_df["Productivity"],
    errors="coerce"
)

year_trend = (
    year_df.dropna(subset=["Year", "Productivity"])
    .groupby("Year")["Productivity"]
    .mean()
    .reset_index()
)

st.line_chart(
    year_trend.set_index("Year")["Productivity"],
    color="#2e7d32"
)

# ---------------- DISTRICT-WISE PRODUCTIVITY ----------------

st.divider()

st.subheader("📍 District-wise Average Productivity")

district_avg = (
    df.groupby("District")["Productivity"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(
    district_avg,
    color="#438b50"
)

# ---------------- AREA VS PRODUCTION ----------------

st.divider()

st.subheader("📊 Area vs Production")

scatter_df = df[["Area", "Production"]].dropna()

fig, ax = plt.subplots(figsize=(10, 5))

ax.scatter(
    scatter_df["Area"],
    scatter_df["Production"],
    alpha=0.5,
    color="#438b50"
)

ax.set_xlabel("Area (Hectare)")
ax.set_ylabel("Production")
ax.set_title("Area vs Production")

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------- CORRELATION HEATMAP ----------------

st.divider()

st.subheader("🔥 Correlation Heatmap")

correlation_df = df[
    ["Area", "Production", "Productivity"]
].apply(pd.to_numeric, errors="coerce")

correlation = correlation_df.corr()

fig, ax = plt.subplots(figsize=(8, 5))

sns.heatmap(
    correlation,
    annot=True,
    cmap="Greens",
    fmt=".2f",
    ax=ax
)

ax.set_title("Agricultural Data Correlation")

fig.tight_layout()

st.pyplot(fig)
plt.close(fig)

# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center; color:#52745a; padding:15px;">
    🌱 AgroPredict AI | Kerala Agricultural Data Analysis
</div>
""", unsafe_allow_html=True)