import os
import warnings
import time
import pandas as pd
from PIL import Image
from transformers import BlipProcessor as Bp
from transformers import BlipForConditionalGeneration as BConGen
from tqdm import tqdm


def suppress_warnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            return func(*args, **kwargs)
    return wrapper


@suppress_warnings
def obtain_df_with_text(data_path, verbose=False) -> pd.DataFrame:
    
    warnings.simplefilter(action='ignore', category=FutureWarning)
    processor = Bp.from_pretrained("Salesforce/blip-image-captioning-large")
    # Add .to("cuda") to run in GPU
    model = BConGen.from_pretrained("Salesforce/blip-image-captioning-large")
    # We use this text to condition the image text generation
    seed1 = "a photography of"
    # We store here the images and their descriptions
    imtx = pd.DataFrame(columns = ["Filename", "Description"])
    
    for img in tqdm(os.listdir(data_path), disable=not verbose):

        if img.endswith(".png"):
            img_path = os.path.join(data_path, img)
            raw_image = Image.open(img_path).convert('RGB')
            # Add .to("cuda") to run in GPU
            inputs = processor(raw_image, seed1, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=20)
            capt = processor.decode(out[0], skip_special_tokens=True)
            imtx.loc[len(imtx.index)] = [img_path, capt]
            
    return imtx 

def main():
    
    fname = "newset.csv"
    data_path = "./Data/PngRealSet"
    ini = time.time()
    df = obtain_df_with_text(data_path, verbose=True)
    df.to_csv(fname, mode="w", header=False, index=False)
    fin = time.time()
    extime = fin - ini
    print("Time:", extime, "s")

if __name__=="__main__":
    main()
