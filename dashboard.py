"""
Health Insurance Claims Cost Analyser — Interactive Dashboard
Author: Hillary Onah | DHIN Finance & Data Science Analyst
Project: Starter Portfolio Project — Health Finance Analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Health Insurance Claims Analyser",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        text-align: center;
    }
    .metric-label { font-size: 13px; color: #6c757d; margin-bottom: 4px; }
    .metric-value { font-size: 26px; font-weight: 600; color: #212529; }
    .metric-delta { font-size: 12px; color: #28a745; }
    .section-header {
        font-size: 16px;
        font-weight: 600;
        color: #212529;
        border-left: 4px solid #0d6efd;
        padding-left: 10px;
        margin: 1.5rem 0 1rem;
    }
    .insight-box {
        background: #e8f4fd;
        border-left: 4px solid #0d6efd;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        font-size: 14px;
        color: #0a4a8a;
        margin: 0.75rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/dsrscientist/dataset1/master/medical_cost.csv"
    try:
        df = pd.read_csv(url)
    except Exception:
        df = pd.read_csv("medical_cost.csv")

    df = df.drop_duplicates().dropna()
    df["age_group"] = pd.cut(
        df["age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=["Under 25", "25–34", "35–44", "45–54", "55+"]
    )
    df["cost_tier"] = pd.cut(
        df["charges"],
        bins=[0, 5000, 15000, 30000, df["charges"].max() + 1],
        labels=["Low (<$5k)", "Medium ($5k–15k)", "High ($15k–30k)", "Very High (>$30k)"]
    )
    return df

df = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/hospital.png", width=60)
    st.title("Claims Analyser")
    st.caption("Health Insurance Cost Analytics | DHIN")
    st.divider()

    st.subheader("🔍 Filters")

    age_range = st.slider(
        "Age range",
        int(df["age"].min()), int(df["age"].max()),
        (18, 65)
    )

    selected_sex = st.multiselect(
        "Sex", options=df["sex"].unique().tolist(),
        default=df["sex"].unique().tolist()
    )

    selected_smoker = st.multiselect(
        "Smoker status", options=df["smoker"].unique().tolist(),
        default=df["smoker"].unique().tolist()
    )

    selected_region = st.multiselect(
        "Region", options=df["region"].unique().tolist(),
        default=df["region"].unique().tolist()
    )

    st.divider()
    st.caption("📊 Built with Python · Streamlit · Plotly")
    st.caption("👤 Hillary Onah | Finance | Data Scientist")

# ── Apply filters ──────────────────────────────────────────────────────────────
filtered = df[
    (df["age"] >= age_range[0]) &
    (df["age"] <= age_range[1]) &
    (df["sex"].isin(selected_sex)) &
    (df["smoker"].isin(selected_smoker)) &
    (df["region"].isin(selected_region))
]

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🏥 Health Insurance Claims Cost Analyser")
st.caption("Exploratory analysis of insurance claim cost patterns · Dataset: US Medical Insurance Costs")
st.divider()

# ── KPI row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

with k1:
    st.metric("Total claims", f"{len(filtered):,}")
with k2:
    st.metric("Avg claim cost", f"${filtered['charges'].mean():,.0f}")
with k3:
    st.metric("Median claim", f"${filtered['charges'].median():,.0f}")
with k4:
    st.metric("Highest claim", f"${filtered['charges'].max():,.0f}")
with k5:
    smoker_pct = (filtered["smoker"] == "yes").mean() * 100
    st.metric("Smoker rate", f"{smoker_pct:.1f}%")

st.divider()

# ── Row 1: Distribution + Age group ───────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-header">Cost Distribution</div>', unsafe_allow_html=True)
    fig1 = px.histogram(
        filtered, x="charges", nbins=50,
        labels={"charges": "Claim Cost (USD)", "count": "Number of Claims"},
        color_discrete_sequence=["#4472C4"]
    )
    fig1.update_layout(
        showlegend=False, margin=dict(t=10, b=10),
        height=320, plot_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown(
        '<div class="insight-box"> Right-skewed: most claims are low-cost, '
        'but a small high-cost tail drives disproportionate spend.</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown('<div class="section-header">Average Cost by Age Group</div>', unsafe_allow_html=True)
    age_cost = (
        filtered.groupby("age_group", observed=True)["charges"]
        .mean().reset_index()
    )
    fig2 = px.bar(
        age_cost, x="age_group", y="charges",
        labels={"age_group": "Age Group", "charges": "Avg Claim (USD)"},
        color="charges",
        color_continuous_scale="Blues"
    )
    fig2.update_layout(
        showlegend=False, margin=dict(t=10, b=10),
        height=320, plot_bgcolor="white",
        coloraxis_showscale=False,
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig2, use_container_width=True)
    if len(age_cost) >= 2:
        youngest = age_cost.iloc[0]["charges"]
        oldest = age_cost.iloc[-1]["charges"]
        multiplier = oldest / youngest if youngest > 0 else 0
        st.markdown(
            f'<div class="insight-box"> The 55+ group costs {multiplier:.1f}x '
            f'more than under-25s — justifying age-banded premium pricing.</div>',
            unsafe_allow_html=True
        )

# ── Row 2: Smoker vs non + Region ─────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Smoking Status — Cost Impact</div>', unsafe_allow_html=True)
    smoker_cost = filtered.groupby("smoker")["charges"].mean().reset_index()
    smoker_cost["smoker_label"] = smoker_cost["smoker"].map({"yes": "Smoker", "no": "Non-smoker"})
    fig3 = px.bar(
        smoker_cost, x="smoker_label", y="charges",
        labels={"smoker_label": "", "charges": "Avg Claim (USD)"},
        color="smoker_label",
        color_discrete_map={"Smoker": "#E74C3C", "Non-smoker": "#2ECC71"}
    )
    fig3.update_layout(
        showlegend=False, margin=dict(t=10, b=10),
        height=300, plot_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig3, use_container_width=True)

    if len(smoker_cost) == 2:
        smoker_avg = smoker_cost[smoker_cost["smoker"] == "yes"]["charges"].values
        nonsmoker_avg = smoker_cost[smoker_cost["smoker"] == "no"]["charges"].values
        if len(smoker_avg) > 0 and len(nonsmoker_avg) > 0 and nonsmoker_avg[0] > 0:
            ratio = smoker_avg[0] / nonsmoker_avg[0]
            st.markdown(
                f'<div class="insight-box">💡 Smokers generate claims {ratio:.1f}x higher — '
                f'the strongest single cost predictor in the dataset.</div>',
                unsafe_allow_html=True
            )

with col4:
    st.markdown('<div class="section-header">Cost by Region</div>', unsafe_allow_html=True)
    region_cost = (
        filtered.groupby("region")["charges"]
        .mean().reset_index()
        .sort_values("charges", ascending=False)
    )
    fig4 = px.bar(
        region_cost, x="region", y="charges",
        labels={"region": "Region", "charges": "Avg Claim (USD)"},
        color_discrete_sequence=["#4472C4"]
    )
    fig4.update_layout(
        showlegend=False, margin=dict(t=10, b=10),
        height=300, plot_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown(
        '<div class="insight-box"> Regional variation is relatively narrow (~$2k spread), '
        'suggesting lifestyle factors outweigh geography in cost prediction.</div>',
        unsafe_allow_html=True
    )

# ── Row 3: Scatter + Cost tier breakdown ──────────────────────────────────────
st.divider()
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="section-header">Age vs Claim Cost (by Smoker Status)</div>', unsafe_allow_html=True)
    fig5 = px.scatter(
        filtered, x="age", y="charges",
        color="smoker",
        color_discrete_map={"yes": "#E74C3C", "no": "#4472C4"},
        labels={"age": "Age", "charges": "Claim Cost (USD)", "smoker": "Smoker"},
        opacity=0.6
    )
    fig5.update_layout(
        margin=dict(t=10, b=10), height=320,
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown(
        '<div class="insight-box"> Two distinct cost bands visible — smokers form a '
        'consistently elevated cluster across all ages.</div>',
        unsafe_allow_html=True
    )

with col6:
    st.markdown('<div class="section-header">Cost Tier Breakdown</div>', unsafe_allow_html=True)
    tier_counts = filtered["cost_tier"].value_counts().reset_index()
    tier_counts.columns = ["tier", "count"]
    fig6 = px.pie(
        tier_counts, values="count", names="tier",
        color_discrete_sequence=["#2ECC71", "#4472C4", "#F39C12", "#E74C3C"],
        hole=0.45
    )
    fig6.update_layout(margin=dict(t=10, b=10), height=320)
    st.plotly_chart(fig6, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "📁 Data: US Medical Insurance Costs (public dataset) · "
    "Built by Hillary Onah as a portfolio project in health finance analytics · "
    "DHIN | June 2026"
)
