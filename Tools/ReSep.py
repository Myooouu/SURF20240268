import shutil
import os
# 首先，读取分类文件并创建一个字典来存储分类信息
categories = {}
with open('train.txt', 'r') as f:
    for line in f:
        Temp = line.split(" ", 5)
        filename, category = Temp[2]+".flac",Temp[4]+Temp[5]
        #The txt file should be the one which can be downloaded from challenge
        #Supposed to be formatted as "kiritan CtrSVDD_0059 CtrSVDD_0059_D_0000006 - - bonafide"
        category = category.strip("\n")
        categories[filename] = category
for filename, category in categories.items():
    # 创建类别文件夹（如果不存在）
    os.makedirs(category, exist_ok=True)
    # 移动文件
    shutil.copy(filename, os.path.join(category, filename))
