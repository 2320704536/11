# ============================================================
# Emotional Crystal — Full Professional Version (Performance Optimized)
# app.py — Main Streamlit Application
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import io
import random
from datetime import datetime

# Utils modules
from utils.sentiment import fetch_news_data, analyze_sentiment_dataframe
from utils.palette import (
    load_default_palette,
    palette_ui_section,
    get_active_palette
)
from utils.crystal_engine import (
    render_crystalmix
)
from utils.cinematic import (
    apply_cinematic_pipeline
)

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Emotional Crystal — Final Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# INITIAL SESSION STATE
# ============================================================
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

if "palette_custom" not in st.session_state:
    st.session_state.palette_custom = {}

if "use_csv_only" not in st.session_state:
    st.session_state.use_csv_only = False

if "random_mode" not in st.session_state:
    st.session_state.random_mode = False

# ============================================================
# TITLE
# ============================================================
st.title("❄ Emotional Crystal — Final Pro (Performance Optimized Version)")
st.caption("Generate cinematic emotional crystal art from text emotions, news articles, or random mode.")


# ============================================================
# SIDEBAR — SECTION 1: DATA SOURCE
# ============================================================
st.sidebar.header("📡 Data Source")

source_mode = st.sidebar.radio(
    "Choose Mode:",
    ["NewsAPI Text Mode", "Random Crystal Mode"],
)

# ============================================================
# NEWS MODE
# ============================================================
if source_mode == "NewsAPI Text Mode":
    st.session_state.random_mode = False

    keyword = st.sidebar.text_input("Keyword for NewsAPI (English only)", "")
    fetch_btn = st.sidebar.button("🔍 Fetch News")

    if fetch_btn and keyword.strip():
        with st.spinner("Fetching news from NewsAPI..."):
            df = fetch_news_data(keyword)
            if not df.empty:
                df = analyze_sentiment_dataframe(df)
                st.session_state.df = df

# ============================================================
# RANDOM MODE
# ============================================================
else:
    st.session_state.random_mode = True
    if st.sidebar.button("✨ Random Generate (Crystal Mode)"):
        # Randomly generate a DataFrame with random emotions only
        df = pd.DataFrame({
            "emotion": np.random.choice(
                list(load_default_palette().keys()),
                size=100,
                replace=True
            )
        })
        df["compound"] = 0.0
        st.session_state.df = df


# ============================================================
# GET CURRENT DATAFRAME
# ============================================================
df = st.session_state.df
