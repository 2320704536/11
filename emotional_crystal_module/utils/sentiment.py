
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

analyzer = SentimentIntensityAnalyzer()

def fetch_news(keyword):
    url = "https://newsapi.org/v2/everything"
    params = {"q":keyword,"sortBy":"publishedAt","language":"en"}
    # API key will come from st.secrets in app
    import streamlit as st
    params["apiKey"] = st.secrets["NEWS_API_KEY"]
    r = requests.get(url,params=params).json()
    rows=[]
    for a in r.get("articles",[]):
        txt=(a.get("title","") or "")+" "+(a.get("description","") or "")
        rows.append({
            "timestamp":a.get("publishedAt",""),
            "text":txt,
            "source":a.get("source",{}).get("name","")
        })
    return pd.DataFrame(rows)

def classify(row):
    c=row['compound']
    if c>0.6: return "joy"
    if c>0.3: return "love"
    if c>0: return "calm"
    if c<-0.5: return "anger"
    if c<0: return "sadness"
    return "neutral"

def analyze_dataframe(df):
    if df.empty: return df
    s=df['text'].apply(analyzer.polarity_scores).tolist()
    df[['neg','neu','pos','compound']] = pd.DataFrame(s)
    df['emotion']=df.apply(classify,axis=1)
    return df
