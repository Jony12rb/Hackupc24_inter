from gradio_client import Client
from moviepy.editor import AudioFileClip

def generate_song(song_prompt : str,
               client : str="https://99b6f868731deec2c0.gradio.live/",
               model : str="facebook/musicgen-small",
               model_path : str ="",
               decoder : str="Default",
               melody : str=None,
               duration : int=10,
               topk : int=250,
               topp : int=0,
               temperature : int=1,
               cfg_coef : int=3,
               api_name : str="/predict_full"):
    """
    Convert text to music using the musicgen model.
    """
    
    client = Client(client)
    result = client.predict(
		model=model,
        model_path = model_path,
		decoder=decoder,
		text=song_prompt,
		melody=melody,
		duration=duration,
		topk=topk,
		topp=topp,
		temperature=temperature,
		cfg_coef=cfg_coef,
		api_name=api_name
    )
    
    return AudioFileClip(result[1])



