import tkinter as tk
from tkinter import font
from tkinter import Text


# FaceAPI 相關的錯誤。有些可能是如：RateLimit Exceed 用量超過
# API Key 有錯要更新之類的問題。
def FaceAPIErrorGUI(text):
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title(text)
    label = tk.Label(
        top,
        text=text,
        font=('Arial', 20),
        bg='yellow',
        width=40,
        height=3,
        wraplength=40,
        justify='left')
    label.pack()

    #frame = tkinter.Frame(master=top).grid(row=1, column=2)
    label1 = tk.Label(top, text='', font=('Arial', 18))
    label1.pack()
    e = tk.Entry(top, font=("Calibri", 24), width=10, show="")
    e.pack()
    e.insert(0, "message: " + text)

    b2 = tk.Button(top, text='關閉', width=15, height=4, command=top.destroy)
    b2.pack()

    # Code to add widgets will go here...
    top.mainloop()
