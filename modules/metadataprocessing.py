import os
import csv
import time
import xml.etree.ElementTree as ET
from PIL import Image
from datetime import datetime
import csv 
import pandas as pd
import numpy as np
import math
from geopy.geocoders import Nominatim

def conv(coord_str):
    
    parts = coord_str.split(",")
    gds = float(parts[0])
    min = float(parts[1][:-1]) # Delete last character ('N' o 'W')
    coord = gds + min / 60

    # If direction is 'S' o 'W', multiply by -1
    if coord_str.endswith("S") or coord_str.endswith("W"):
        coord *= -1

    return coord


def city_state_country(img):
    
    geolocator = Nominatim(user_agent="gonchuuu")

    lat = img['Latitude']
    long = img['Longitude']
    if lat is not None and long is not None:
        lat = str(conv(lat))
        long = str(conv(long))
        coord = lat + ", " + long
        location = geolocator.reverse(coord, exactly_one=True, language="en-GB")
        address = location.raw['address']
        return address.get('city', ''), address.get('country', '')

    else:
        return None, None
    

def get_season(img):

    if img["Time"] is not None:
        month = img["Time"].month 
        if 3 <= month <= 5:
            return "Spring"
        elif 6 <= month <= 8:
            return "Summer"
        elif 9 <= month <= 11:
            return "Autum"
        else:
            return "Winter"
    else:
        return None 

        
def derivate_metadata(df):
    # Now we get the season
    df["Season"] = df.apply(get_season, axis=1)
    # First data derivation relative to location
    df[["City", "Country"]] = df.apply(city_state_country, axis=1).to_list()
    return df        


def extract_metadata(data_path, df):
    
    metadata_dict = {}
    for img in os.listdir(data_path):
        
        if img.endswith(".png"):
            img_path = os.path.join(data_path, img)
            raw_image = Image.open(img_path).convert('RGB')
            metadata = raw_image.info
            valor_xmp = metadata.get("XML:com.adobe.xmp", None)
            
            if valor_xmp:
                root = ET.fromstring(valor_xmp)
                time = None
                lat = None
                long = None

                for child in root.iter():
                    if child.tag.endswith("CreateDate"):
                        time_str = child.text
                        time = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
                    elif child.tag.endswith("GPSLatitude"):
                        lat = child.text          
                    elif child.tag.endswith("GPSLongitude"):
                        long = child.text
                df = df._append({"Image": img, "Time": time, "Latitude": lat, 
                                "Longitude": long}, ignore_index=True)


            else:
                df = df._append({"Image": img, "Time": None, "Latitude": None, 
                                "Longitude": None}, ignore_index=True)
    return df    


def generate_metadata(data_path, fname):

    df = pd.DataFrame(columns=["Image", "Time", "Latitude", "Longitude"])
    df = extract_metadata(data_path, df)
    df = derivate_metadata(df)
    df.to_csv(fname, index=False)


def main():

    fname = "metadata.csv"
    data_path = "/Users/gonzalomf_12/Documents/HackUPC/Hackupc24_inter/Data/PngRealSet"
    ini = time.time()
    generate_metadata(data_path, fname)
    fin = time.time()
    extime = fin - ini
    print("Time:", extime, "s")


main()