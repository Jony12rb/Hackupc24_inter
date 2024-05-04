import streamlit as st
from manager import generate_videoclip

st.title("Personal Gallery videoclip generator")

query = st.text_input("Put here your text")

if st.button("Generate videoclip"):
    if query:
        videoclip = generate_videoclip(query)
        st.video(videoclip)
    else: 
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

