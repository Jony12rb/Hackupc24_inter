from gradio_client import Client
import urllib3
import replicate

def generate_song(song_prompt : str,
               client : str="https://347770e37084a2c7e3.gradio.live/",
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
    
    
    return result[1]
  
def generate_song_replicated(song_prompt : str,
                             audio_path : str,
                             duration : int=10,
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
                             ):

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
  with open(audio_path,'wb') as out:
    out.write(mp3file.data)

if __name__ == '__main__':
  generate_song("A song about the ocean",
                client="https://347770e37084a2c7e3.gradio.live/",
                model="facebook/musicgen-small",
                melody=None,
                duration=10,
                topk=250,
                topp=0,
                temperature=1,
                cfg_coef=3,
                api_name="/predict_full")



