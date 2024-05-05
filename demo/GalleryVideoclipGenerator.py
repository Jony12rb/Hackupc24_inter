import sys
sys.path.insert(1, 'modules')

import streamlit as st
from manager import generate_videoclip
from iris_db import IrisDB
from openai import OpenAI
import os
import getpass
import pandas as pd

if not os.environ.get("OPENAI_API_KEY"): 
    os.environ["OPENAI_API_KEY"] = open('OPENAI_API_KEY.txt').read().strip()

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
DB = IrisDB(Openai_client = openai_client)
if not DB.table_exists():
    df = pd.read_csv('Data/version2.csv')
    df.columns = ['image_path', 'description']

    DB.init_table()
    DB.insert_df_to_table(df)


st.title("Personal Gallery videoclip generator")

query = st.text_input("Put here your prompt")
amount_images = st.slider("Amount of images", 1, 30, 10)
duration = st.slider("Duration (seconds)", 5, 60, 20)
video_path = st.text_input("Video path", 'Data/ExampleData/test.mp4')

if st.button("Generate videoclip"):
    if query:
        videoclip = generate_videoclip(openai_client=openai_client, DB=DB, 
                                       query=query, duration=duration, video_path=video_path, amount_images=min(amount_images,duration))
        st.video(video_path)
    else: 
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

