import sys
sys.path.insert(1, 'modules')

import streamlit as st
from manager import generate_videoclip
from iris_db import IrisDB
from openai import OpenAI
import os
import getpass

if not os.environ.get("OPENAI_API_KEY"): 
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
DB = IrisDB(Openai_client = openai_client)

st.title("Personal Gallery videoclip generator")

query = st.text_input("Put here your prompt")
amount_images = st.slider("Amount of images", 1, 30, 10)
duration = st.slider("Duration (seconds)", 5, 60, 20)
video_path = st.text_input("Video path", 'SampleData/output.mp4')

if st.button("Generate videoclip"):
    if query:
        videoclip = generate_videoclip(openai_client=openai_client, DB=DB, 
                                       query=query, duration=duration, video_path=video_path, amount_images=amount_images)
        st.video(video_path)
    else: 
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

