import os
import csv
import warnings
import requests
import time
from PIL import Image
from transformers import BlipProcessor as Bp
from transformers import BlipForConditionalGeneration as BConGen


def suppress_warnings(func):
    def wrapper(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=FutureWarning)
            return func(*args, **kwargs)
    return wrapper


@suppress_warnings
def obtain_text(data_path) -> dict[str, str]:
    
    warnings.simplefilter(action='ignore', category=FutureWarning)
    processor = Bp.from_pretrained("Salesforce/blip-image-captioning-large")
    # Add .to("cuda") to run in GPU
    model = BConGen.from_pretrained("Salesforce/blip-image-captioning-large")
    # We use this text to condition the image text generation
    seed1 = "a photography of"
    # We store here the images and their descriptions
    imtx = {}
    
    for img in os.listdir(data_path):

        if img.endswith(".png"):
            img_path = os.path.join(data_path, img)
            raw_image = Image.open(img_path).convert('RGB')
            # Add .to("cuda") to run in GPU
            inputs = processor(raw_image, seed1, return_tensors="pt")
            out = model.generate(**inputs, max_new_tokens=20)
            capt = processor.decode(out[0], skip_special_tokens=True)
            imtx[img_path] = capt
            
    return imtx 


def image2text(data_path: str, fname: str) -> None:

    imtx = obtain_text(data_path)

    with open(fname, "w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerow(["Filename", "Description"])
        
        for image, descr in imtx.items():
            writer.writerow([image, descr])

    print(f"File '{fname}' successfully created.")

def main():
    
    fname = "newset.csv"
    data_path = "/Users/gonzalomf_12/Documents/HackUPC/Hackupc24_inter/Data/PngRealSet"
    ini = time.time()
    image2text(data_path, fname)
    fin = time.time()
    extime = fin - ini
    print("Time:", extime, "s")


main()
