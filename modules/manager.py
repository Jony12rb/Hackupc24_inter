from text_embedder import generate_text_embedding
from db_info_retriever import retrieve_images
from song_prompt_creator import create_song_prompt
from song_generator import generate_song
from ImgsMus2Video import make_video

def generate_videoclip(query: str):
    query_embedding = generate_text_embedding(query)
    images, image_descriptions = retrieve_images(query_embedding)
    song_prompt = create_song_prompt(query, image_descriptions)
    song = generate_song(song_prompt)
    make_video(images, song)
