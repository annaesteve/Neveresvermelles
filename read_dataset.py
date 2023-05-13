import pandas as pd
import numpy as np
import os;
from PIL import Image
import requests
from io import BytesIO

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

file_path = "./hackupc2023_restbai__dataset/hackupc2023_restbai__dataset_sample.json"
dataset = pd.read_json(file_path).transpose()


url = dataset['images'].astype(str).iloc[0].replace("['",'').replace("']",'')
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img = crop_center(img, 256, 256)
img = img.convert("RGBA")
img.save('test1.png')




