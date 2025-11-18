
import streamlit as st

def load_default_palette():
    return {
        "joy":(255,200,60),"love":(255,95,150),
        "anger":(245,60,60),"sadness":(70,120,255),
        "curiosity":(200,220,255),"calm":(120,200,255),
        "neutral":(200,200,200)
    }

def build_active_palette(default, custom, use_csv_only):
    if use_csv_only:
        return custom.copy()
    p=default.copy()
    p.update(custom)
    return p

def palette_ui(panel, default_palette):
    panel.subheader("Palette")
    st.session_state.setdefault("custom_palette",{})
    use_csv_only=panel.checkbox("Use CSV only", False)
    with panel.expander("Add Custom Emotion"):
        name=panel.text_input("Name")
        r=panel.number_input("R",0,255,100)
        g=panel.number_input("G",0,255,100)
        b=panel.number_input("B",0,255,100)
        if panel.button("Add Color"):
            st.session_state.custom_palette[name]=(r,g,b)
    return build_active_palette(default_palette,
                                st.session_state.custom_palette,
                                use_csv_only)
