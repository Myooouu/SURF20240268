from PIL import Image
import os
path = "./JPEGImages/"
for file_name in os.listdir(path):
    img =Image.open(path + file_name)
    if img.mode != "RGB" :
        print(file_name)
        img_rgb = img.convert("RGB")
        os.remove(path + file_name)
        img_rgb.save(path + file_name)
# The model only accept RGB files, so if you do not have them to be RGB, you can simply use this file to convert it into RGB