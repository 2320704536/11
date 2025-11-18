# ============================================================
# sentiment.py — Emotional Crystal Pro (FINAL FIXED VERSION)
# ============================================================
from __future__ import annotations   # ← 关键：让类型注解惰性解析，避免 NameError

import streamlit as st
import requests
import pandas as pd
import numpy as np
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

_analyzer = SentimentIntensityAnalyzer()


# ============================================================
# Fetch NewsAPI  (NO type annotations)
# ============================================================

def fetch_news_data(keyword):
    if "NEWS_API_KEY" not in st.secrets:
        st.error("Missing NEWS_API_KEY in Streamlit Secrets.")
        return pd.DataFrame([])

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": st.secrets["NEWS_API_KEY"],
    }

    res = requests.get(url, params=params).json()
    articles = res.get("articles", [])

    rows = []
    for a in articles:
        title = (a.get("title") or "")
        desc  = (a.get("description") or "")
        text = f"{title}. {desc}".strip()

        rows.append({
            "timestamp": a.get("publishedAt", ""),
            "text": text,
            "source": a.get("source", {}).get("name", ""),
        })

    return pd.DataFrame(rows)


# ============================================================
# VADER
# ============================================================

def vader_scores(text):
    return _analyzer.polarity_scores(str(text))


# ============================================================
# 20+ emotion classifier
# ============================================================

def classify_emotion_expanded(row):
    c = row["compound"]
    pos = row["pos"]
    neg = row["neg"]
    neu = row["neu"]

    if c >= 0.75 and pos > 0.60: return "joy"
    if c >= 0.55 and pos > 0.45: return "love"
    if 0.45 <= c < 0.75 and pos > 0.35: return "pride"
    if 0.35 <= c < 0.55 and pos > 0.30: return "hope"

    if 0.15 <= c < 0.35 and neu > 0.35: return "calm"
    if 0.05 <= c < 0.25 and (neu > 0.30 or pos > 0.20): return "curiosity"
    if pos > 0.25 and abs(c) < 0.20: return "surprise"
    if 0.10 <= c < 0.35 and pos > 0.25: return "trust"
    if c >= 0.20 and (pos > 0.20 and neu > 0.20): return "awe"
    if neu >= 0.40 and (0 <= c < 0.20) and pos > 0.10: return "nostalgia"

    if c <= -0.60 and neg > 0.40: return "anger"
    if -0.60 < c <= -0.25 and neg > 0.30: return "fear"
    if -0.40 < c <= -0.05 and neu > 0.30: return "sadness"
    if -0.15 <= c <= 0.05 and neg > 0.20 and neu < 0.50: return "anxiety"
    if neg > 0.35 and c < -0.10: return "disgust"

    if abs(c) < 0.05 and neu > 0.50: return "neutral"
    if neu > 0.45 and 0.05 <= abs(c) <= 0.15: return "boredom"

    return "mixed"


# ============================================================
# Apply sentiment + emotion  (NO type annotations)
# ============================================================

def analyze_sentiment_dataframe(df):
    if df.empty:
        return df

    scores = df["text"].apply(vader_scores).apply(pd.Series)
    df = pd.concat([df.reset_index(drop=True), scores], axis=1)
    df["emotion"] = df.apply(classify_emotion_expanded, axis=1)
    return df
