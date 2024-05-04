from gradio_client import Client
from moviepy.editor import AudioFileClip

def generate_song(song_prompt,
               client="https://bd4d529137a742d156.gradio.live/",
               model="facebook/musicgen-medium",
               model_path="",
               decoder="Default",
               melody=None,
               duration=10,
               topk=250,
               topp=0,
               temperature=1,
               cfg_coef=3,
               api_name="/predict_full"):
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



