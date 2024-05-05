from iris_db import IrisDB
from song_prompt_creator import create_song_prompt
from song_generator import generate_song_replicated
from ImgsMus2Video import make_video_experimental
from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

def generate_videoclip(
        openai_client : OpenAI,
        DB: IrisDB,
        query: str,
        duration : int = 20,
        video_path : str = 'SampleData/output.mp4',
        amount_images : int = 10
    ):
    """
    Given a query, generates a video clip with images and a song.
    """
    if not os.environ.get("REPLICATE_API_TOKEN"):
        raise Exception("Please set the REPLICATE_API_TOKEN environment variable.")
    
    db_output_df  = DB.description_search(query=query, top_n=amount_images)
    image_paths = db_output_df['path'].tolist()
    image_paths = [path for path in image_paths if os.path.exists(path)]
    image_descriptions = db_output_df['description'].tolist()
    song_prompt = create_song_prompt(query, image_descriptions, openai_client)
    #song = generate_song(song_prompt, duration=duration, model="facebook/musicgen-medium")
    song = generate_song_replicated(song_prompt, duration=duration)
    make_video_experimental(image_paths, song, duration, video_path)


if __name__ == '__main__':
    Openai_client = OpenAI()
    DB = IrisDB(Openai_client = Openai_client)
    if not DB.table_exists():
        df = pd.read_csv('Data/version2.csv')
        df.columns = ['image_path', 'description']

        DB.init_table()
        DB.insert_df_to_table(df)

    query = 'Cool chairs'
    generate_videoclip(Openai_client, DB, query, duration=10, video_path='Data/ExampleData/output.mp4', amount_images=6)
