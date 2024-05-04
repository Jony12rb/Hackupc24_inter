import streamlit as st
import random 
import glob
import os
from datetime import datetime
from PIL import Image

import sys
sys.path.insert(1, 'utils')

from image_adder import add_images

if not os.environ.get("OPENAI_API_KEY"): 
    os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")

openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

st.title("Image uploader")

uploaded_images=st.file_uploader("Upload your images. Only png files are supported.", type=['png'], accept_multiple_files=True)
if uploaded_images:
    if not st.button("Confirm selection and upload"):
        for img in uploaded_images:
            st.image(img)
    else: 
        newpath = f"Data/UploadedData/{datetime.today().strftime('%Y_%m_%d_%H_%M_%S')}"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        for img in uploaded_images:
            imgpath = f"{newpath}/{datetime.today().strftime('%H_%M_%S_%f')}.png"
            pilimg = Image.open(img)
            pilimg.save(imgpath, format='PNG')
            pilimg.close()
        add_images(openai_client, newpath)

        
        add_images(uploaded_images)
    
        
    
else:
    for i in range(3):
        st.image(random.choice(glob.glob("Data/PngRealSet/*.png")))