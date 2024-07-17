import os
import shutil
import numpy as np
def get_files():
    NameList = []
    for filepath,dirnames,filenames in os.walk(r'E:\XJTLU\SURFData\Trial\OriHere'):    #Path here
        for filename in filenames:
            temp = os.path.join(filepath,filename)
            NameList.append(f'{temp}')
    return NameList

def get_labels():
    LabelList = []
    fileHandler  =  open("E:\\XJTLU\\SURF20240268\\DataLoad\\dev.txt",  "r")   # Open file        
    while  True:
        # Get next line from file
        line  =  fileHandler.readline()
        LabelList.append(line)
        # If line is empty then end of file reached
        if  not  line  :
            return LabelList
        # Close Close    
    fileHandler.close()

def labelSeperate(Labels):
    x = np.empty(shape=[100000,2],dtype = str)
    for OriLabel in Labels:
        Temp = OriLabel.split(" ", 5)
        np.append(x,[Temp[2],Temp[5]])
    print(x)
        


def seperate(Labels,FilePaths):
    for label in Labels:
        break

Filepaths = get_files()
Labels = get_labels()
labelSeperate(Labels)