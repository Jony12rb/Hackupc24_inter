from iris_db import IrisDB
from song_prompt_creator import create_song_prompt
from song_generator import generate_song
from ImgsMus2Video import make_video
from openai import OpenAI

def generate_videoclip(openai_client : OpenAI, DB: IrisDB, 
                       query: str, duration : int = 20, video_path : str = 'SampleData/output.mp4', amount_images : int = 10):
    db_output_df  = DB.description_search(txt=query, top_n=amount_images)
    image_paths = db_output_df['path'].tolist()
    image_descriptions = db_output_df['description'].tolist()
    song_prompt = create_song_prompt(query, image_descriptions)
    song = generate_song(song_prompt, duration=duration)
    make_video(image_paths, song, duration, video_path)
