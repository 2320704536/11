
import streamlit as st
from utils.sentiment import fetch_news, analyze_dataframe
from utils.crystal_engine import render_crystal
from utils.cinematic import apply_cinematic_pipeline
from utils.palette import load_default_palette, build_active_palette, palette_ui
import pandas as pd
import io

st.set_page_config(page_title="Emotional Crystal — Pro", layout="wide")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame()
if 'palette' not in st.session_state:
    st.session_state.palette = load_default_palette()

st.sidebar.title("Data Source")
mode = st.sidebar.radio("Mode", ["NewsAPI", "Random Crystal"])

if mode == "NewsAPI":
    kw = st.sidebar.text_input("Keyword")
    if st.sidebar.button("Fetch News"):
        df = fetch_news(kw)
        df = analyze_dataframe(df)
        st.session_state.df = df
else:
    if st.sidebar.button("Random Generate"):
        df = pd.DataFrame({"emotion": ["joy","love","anger","curiosity"]*20})
        st.session_state.df = df

df = st.session_state.df
palette = palette_ui(st.sidebar, st.session_state.palette)

st.sidebar.subheader("Crystal Engine")
layers = st.sidebar.slider("Layers",1,20,10)
shapes = st.sidebar.slider("Shapes per emotion",5,40,20)

st.sidebar.subheader("Cinematic")
contrast = st.sidebar.slider("Contrast",-0.5,1.0,0.2)

img = render_crystal(df, palette, layers=layers, shapes_per_emotion=shapes)
img = apply_cinematic_pipeline(img, contrast=contrast)

col1,col2 = st.columns([2,1])
with col1:
    st.image(img)
    buf=io.BytesIO()
    img.save(buf,format="PNG")
    st.download_button("Download",buf.getvalue(),file_name="crystal.png")

with col2:
    st.dataframe(df, height=600)
