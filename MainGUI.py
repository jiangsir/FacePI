import tkinter as tk
from tkinter import font
import os, sys, json, time
import FaceAPI 

basepath = os.path.dirname(os.path.realpath(__file__))

#with open(basepath + '/FacePI-Config.json', 'r') as f:
#    config = json.load(f)
#api_key = config["api_key"]
#host = config["host"]
#personGroupId = config['personGroupId']
api_key = "f3e388f66ee146d3b6e96f6ca2ac25d3"
host = "eastasia.api.cognitive.microsoft.com"
personGroupId = "junior"
title = "高師大附中 刷臉簽到系統"

top = tk.Tk()
font_helv36 = font.Font(family='Helvetica', size=36, weight='bold')

width = top.winfo_width()
height = top.winfo_height()
x = (top.winfo_screenwidth() // 2) - (width // 2)
y = (top.winfo_screenheight() // 2) - (height // 2)
#top.geometry('{}x{}'.format(width, height))
pad = 3
top.geometry("{0}x{1}+0+0".format(top.winfo_screenwidth() - pad,
                                  top.winfo_screenheight() - pad))

top.title(title + " for " + personGroupId)
label = tk.Label(top, text=title, font=font_helv36)
label.pack()

def takePicture():
    imagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(imagepath)):
        os.makedirs(os.path.dirname(imagepath))
    os.system("raspistill -t 3000 -o " + imagepath)
    return imagepath


def Signin():
    faceapi = FaceAPI.Face(api_key, host)


    #os.system('python3 ' + basepath + '/FacePI-Identity.py ' + personGroupId)


b2 = tk.Button(
    top, text='簽到', font=font_helv36, width=10, height=5, command=Signin)
b2.pack()

# Code to add widgets will go here...
top.mainloop()
