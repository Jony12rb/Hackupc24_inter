from gradio_client import Client
import urllib3
import replicate

def generate_song(
        song_prompt : str,
        client : str="https://5c3c66d4aa962d8f21.gradio.live",
        model : str="facebook/musicgen-small",
        model_path : str ="",
        decoder : str="Default",
        melody : str=None,
        duration : int=10,
        topk : int=250,
        topp : int=0,
        temperature : int=1,
        cfg_coef : int=3,
        api_name : str="/predict_full"
    ):
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
    
    
    return result[1]
  
def generate_song_replicated(song_prompt : str,
                             audio_path : str = "Data/ExampleData/input.mp3",
                             duration : int=2,
                             model_version : str="large",
                             top_k : int=250,
                             top_p : int=0,
                             temperature : int=1,
                             continuation : bool=False,
                             continuation_start : int=0,
                             output_format : str="mp3",
                             multi_band_diffusion : bool=False,
                             normalization_strategy : str="peak",
                             classifier_free_guidance : int=3,
                             ) -> str:
  """
  Generate a song using the musicgen model. This function uses the Replicate API.
  returns the path to the audio file.
  """

  output = replicate.run(
      "meta/musicgen:671ac645ce5e552cc63a54a2bbff63fcf798043055d2dac5fc9e36a837eedcfb",
      input={
          "top_k": top_k,
          "top_p": top_p,
          "prompt": song_prompt,
          "duration": duration,
          "temperature": temperature,
          "continuation": continuation,
          "model_version": model_version,
          "output_format": output_format,
          "continuation_start": continuation_start,
          "multi_band_diffusion": multi_band_diffusion,
          "normalization_strategy": normalization_strategy,
          "classifier_free_guidance": classifier_free_guidance
      }
  )

  mp3file = urllib3.request("GET", output)
  # Save the audio file. Erase the file if it already exists.
  with open(audio_path, 'wb') as f:
    f.write(mp3file.data)
    
  return audio_path

if __name__ == '__main__':
  generate_song_replicated("A song about the ocean")


