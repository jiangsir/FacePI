import tkinter as tk
from tkinter import font
from tkinter import Text


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
