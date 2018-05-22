import tkinter as tk
from tkinter import *
from tkinter import Text
from tkinter import WORD, INSERT
from tkinter.font import Font

# FaceAPI 相關的錯誤。有些可能是如：RateLimit Exceed 用量超過
# API Key 有錯要更新之類的問題。
def FaceAPIErrorGUI(title, errorcode, errormessage):
    print('ERROR title:', title)
    print('ERROR code:', errorcode)
    print('ERROR message:', errormessage)
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title(title)
    label = tk.Label(
        top,
        text=errorcode,
        font=('Arial', 18),
        #bg='yellow',
        #width=40,
        #height=5,
        wraplength=350,
        justify='center')
    label.pack()

    #frame = tkinter.Frame(master=top).grid(row=1, column=2)
    label1 = tk.Label(
        top,
        text=errormessage,
        font=('Arial', 16),
        bg='yellow',
        #width=40,
        #height=5,
        wraplength=350,
        justify='left')
    label1.pack()
    # e = tk.Entry(top, font=("Calibri", 24), width=10, show="")
    # e.pack()
    # e.insert(0, "message: " + title)

    # b2 = tk.Button(top, text='關閉', width=15, height=3, command=top.destroy)
    # b2.pack()

    # Code to add widgets will go here...
    top.mainloop()


def MessageGUI(title, text):
    #top = tk.Toplevel()
    top = tk.Tk()
    top.geometry('400x400')
    top.title(title)
    # T = Text(top, height=2, width=30)
    # T.pack()
    # T.insert(END, "Just a text Widget\nin two lines\n")
    myFont = Font(family="Times New Roman", size=28)
    text1 = Text(top, wrap=WORD)
    text1.configure(font=myFont)
    text1.insert(INSERT, text)
    text1.pack()
    label1 = tk.Label(top, text=text, font=('Arial', 28))
    label1.pack()

    top.lift()
    top.call('wm', 'attributes', '.', '-topmost', '1')
    top.mainloop()