# 假设我们有一个名为classification.txt的文件，其中包含分类信息
# 格式为：filename: category
import shutil
import os
# 首先，读取分类文件并创建一个字典来存储分类信息
categories = {}
with open('dev.txt', 'r') as f:
    for line in f:
        Temp = line.split(" ", 4)
        filename, category = Temp[2]+".flac",Temp[4]
        categories[filename] = category
# 现在，您可以根据分类信息对您的文件进行分类
# 例如，将文件移动到对应类别的文件夹中
for filename, category in categories.items():
    # 创建类别文件夹（如果不存在）
    os.makedirs(category, exist_ok=True)
    # 移动文件
    shutil.copy(filename, os.path.join(category, filename))
