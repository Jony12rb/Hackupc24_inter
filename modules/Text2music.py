from gradio_client import Client
from moviepy.editor import AudioFileClip


def text2music(text,
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
    
    client = Client("https://bd4d529137a742d156.gradio.live/")
    result = client.predict(
		model=model,
        model_path = model_path,
		decoder=decoder,
		text=text,
		melody=melody,
		duration=duration,
		topk=topk,
		topp=topp,
		temperature=temperature,
		cfg_coef=cfg_coef,
		api_name=api_name
    )
    
    return AudioFileClip(result[1])


if __name__ == "__main__":
    # Measuring the time taken to convert text to music
    import time
    start = time.time() 
    text2music("Summer trip").preview()
    end = time.time()
    print(f"Time taken to convert text to music: {end - start} seconds")