import tkinter as tk
from tkinter import *
from tkinter import Text
from tkinter import WORD, INSERT
from tkinter.font import Font
from PIL import Image
import threading, time

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

def countdown(b):
    count = 2000
    while count>0:
        count = count - 100
        b.set(count)
        time.sleep(0.1)

def SuccessGUI(title, text, imagepath):
    #top = tk.Toplevel()
    top = tk.Tk()
    top.geometry('400x400')
    top.title(title)

    img = Image.open(imagepath)
    img.save(imagepath + ".gif", 'GIF')

    imagefile = tk.PhotoImage(file=imagepath+".gif")
    maxwidth = 200
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)

    print('imagefile=', imagefile)
    canvas = tk.Canvas(top, height=imagefile.height(), width=imagefile.width())

    image = canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    # count = 5000
    # btn_text = tk.StringVar()
    # btn_text.set("!!!!"+str(count))
    # #button = tk.Button(top, textvariable=btn_text, fg="red", command=countdown, argv=[btn_text])
    # button = tk.Button(top, textvariable=btn_text, fg="red", command=lambda: countdown(btn_text))
    # # t = threading.Thread(target=countdown, args=[button])
    # # t.start()
    
    # button.pack()

    # def counter_label(label):
    #     #counter = 0
    #     def count():
    #         global counter
    #         counter -= 100
    #         label.config(text='倒數 {:.1f} 秒關閉'.format(counter/1000))
    #         label.after(100, count)
    #     count()
    
    label = tk.Label(top, fg="dark green")
    labelFont = Font(family="Times New Roman", size=18)
    label.configure(font=labelFont)
    label.configure(anchor="center")
    label.pack()

    closecounter = 3000
    counter = closecounter
    while counter>0:
        counter -= 100
        label.config(text='倒數 {:.1f} 秒關閉'.format(counter/1000))
        time.sleep(0.1)
        #label.after(100, count)
    
    #counter_label(label)

    # myFont = Font(family="Times New Roman", size=28)
    # text1 = tk.Text(top, wrap=WORD)
    # text1.configure(font=myFont)
    # text1.insert(INSERT, text)
    # text1.pack()

    label2 = tk.Label(top, fg="dark green")
    label2Font = Font(family="Times New Roman", size=28)
    label2.configure(font=label2Font)
    label2.configure(anchor="center")
    label2.config(text=text)
    label2.pack()
    

    top.after(closecounter, lambda: top.destroy())
    top.lift()
    top.call('wm', 'attributes', '.', '-topmost', '1')
    top.mainloop()