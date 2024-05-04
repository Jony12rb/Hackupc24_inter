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

    lat = img['lat']
    long = img['long']
    if lat is not None and long is not None:
        lat = str(conv(lat))
        long = str(conv(long))
        coord = lat + ", " + long
        location = geolocator.reverse(coord, exactly_one=True, language="en-GB")
        address = location.raw['address']
        return address.get('city', ''), address.get('country', '')

    else:
        return None, None


def extract_metadata(data_path):
    
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
                metadata_dict[img_path] = {"time": time, "lat": lat, "long": long}
            else:
                # Si no se encuentra el valor XMP, se asignan None a los metadatos
                metadata_dict[img_path] = {"time": None, "lat": None, "long": None}


    return metadata_dict


def save_metadata_to_csv(metadata_dict, fname):
    with open(fname, 'w', newline='') as csvfile:
        fieldnames = ['Image', 'Time', 'Latitude', 'Longitude', 'Season', 'City', 'Country']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for img, data in metadata_dict.items():
            writer.writerow({'Image': img,
                             'Time': data['time'],
                             'Latitude': data['lat'],
                             'Longitude': data['long'], 
                             'Season': data['season'], 
                             'City': data['city'],
                             'Country': data['country']})


def get_season(img):

    if img["time"] is not None:
        month = img["time"].month 
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

        
def derivate_metadata(metadata_dict):
    
    for img in metadata_dict:
        # First data derivation relative to location
        city, country = city_state_country(metadata_dict[img])
        # Now we get the season
        season = get_season(metadata_dict[img])

        metadata_dict[img]["city"] = city
        metadata_dict[img]["country"] = country
        metadata_dict[img]["season"] = season
    



def generate_metadata(data_path, fname):

    metadata_dict = extract_metadata(data_path)
    derivate_metadata(metadata_dict)
    save_metadata_to_csv(metadata_dict, fname)


def main():

    fname = "metadata1.csv"
    data_path = "/Users/gonzalomf_12/Documents/HackUPC/Hackupc24_inter/Data/PngRealSet"
    ini = time.time()
    generate_metadata(data_path, fname)
    fin = time.time()
    extime = fin - ini
    print("Time:", extime, "s")


main()