import tkinter as tk
from tkinter import font
import os, sys, json

basepath = os.path.dirname(os.path.realpath(__file__))

with open(basepath + '/FacePI-Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']


def identity():
    os.system('python3 ' + basepath + '/FacePI-Identity.py ' +
              personGroupId)


top = tk.Tk()
font_helv36 = font.Font(family='Helvetica', size=36, weight='bold')

width = top.winfo_width()
height = top.winfo_height()
x = (top.winfo_screenwidth() // 2) - (width // 2)
y = (top.winfo_screenheight() // 2) - (height // 2)
#top.geometry('{}x{}'.format(width, height))
top.geometry('600x600')

title = config['title']
top.title(title + " for " + personGroupId)
label = tk.Label(top, text=title, font=font_helv36)
label.pack()
b2 = tk.Button(
    top, text='簽到', font=font_helv36, width=10, height=5, command=identity)
b2.pack()

# Code to add widgets will go here...
top.mainloop()
