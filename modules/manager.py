from iris_db import IrisDB
from song_prompt_creator import create_song_prompt
from song_generator import generate_song
from ImgsMus2Video import make_video
from openai import OpenAI
import pandas as pd

GRADIO_CLIENT = "https://05af30f78f5cf150b7.gradio.live/"

def generate_videoclip(openai_client : OpenAI, DB: IrisDB, 
                       query: str, duration : int = 20, video_path : str = 'SampleData/output.mp4', amount_images : int = 10):
    db_output_df  = DB.description_search(query=query, top_n=amount_images)
    image_paths = db_output_df['path'].tolist()
    image_descriptions = db_output_df['description'].tolist()
    song_prompt = create_song_prompt(query, image_descriptions, openai_client)
    song = generate_song(song_prompt, duration=duration, client=GRADIO_CLIENT)
    print(song)
    make_video(image_paths, song, duration, video_path)


if __name__ == '__main__':
    OPENAI_API_KEY = open('OPENAI_API_KEY.txt').read().strip()
    Openai_client = OpenAI(api_key=OPENAI_API_KEY)
    DB = IrisDB(Openai_client = Openai_client)
    if not DB.table_exists():
        df = pd.read_csv('Data/version2.csv')
        df.columns = ['image_path', 'description']

        DB.init_table()
        DB.insert_df_to_table(df)

    query = 'a cool chair'
    generate_videoclip(Openai_client, DB, query, duration=20, video_path='SampleData/output.mp4', amount_images=10)
