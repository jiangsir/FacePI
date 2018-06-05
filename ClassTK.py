from PIL import Image, ImageDraw, ImageFont, ImageTk
import os, json
import ClassFaceAPI as FaceAPI

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

api_key = config['api_key']
host = config['host']
personGroupId = config['personGroupId']


def train_oneShot(top, e, personname, userData, imagepath):
    ''' 未經訓練的新人，憑簽到時的一張照片進行訓練。 '''
    jpgimagepaths = []
    jpgimagepaths.append(imagepath)
    personAPI = FaceAPI.Person(api_key, host)
    if personname == '':
        personname = 'unknown_oneshot'
    personAPI.add_personimages(personGroupId, personname, userData,
                               jpgimagepaths)
    personGroupapi = FaceAPI.PersonGroup(api_key, host)
    personGroupapi.train_personGroup(personGroupId)
    top.destroy()


def tk_UnknownPerson(text, facepath, picture):
    ''' # 當不認識的時候，跳這個畫面。以便用這個圖片去訓練新人。 '''
    import tkinter as tk

    top = tk.Tk()
    #top = tk.Toplevel()
    top.geometry('500x500')
    top.title(text)
    print("訓練 oneshot: picture=" + picture)
    pil_image = Image.open(facepath)
    width, height = pil_image.size
    maxwidth = 200
    pil_image = pil_image.resize((maxwidth, int(height * maxwidth / width)),
                                 Image.ANTIALIAS)

    imagefile = ImageTk.PhotoImage(pil_image)
    #imagefile = tk.PhotoImage(file=imagepath)
    h = imagefile.height()
    w = imagefile.width()
    # if w > maxwidth:
    #     imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)

    print('h=', imagefile.height(), 'w=', imagefile.width())
    canvas = tk.Canvas(top, height=imagefile.height(), width=imagefile.width())
    canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    label = tk.Label(top, text=text, font=('Arial', 20))
    label.pack()

    #frame = tkinter.Frame(master=top).grid(row=1, column=2)
    label1 = tk.Label(top, text='請輸入姓名：', font=('Arial', 18))
    label1.pack()
    e = tk.Entry(top, font=("Calibri", 24), width=10, show="")
    e.pack()
    e.insert(0, "")

    b1 = tk.Button(
        top,
        text='記住我！',
        width=15,
        height=3,
        command=lambda: train_oneShot(top, e, e.get(), 'oneshot', picture))
    b1.pack()

    b2 = tk.Button(top, text='下一位！', width=15, height=2, command=top.destroy)
    b2.pack()
    #top.bind('<Return>', lambda x: top.destroy())

    top.lift()
    top.call('wm', 'attributes', '.', '-topmost', '1')
    # Code to add widgets will go here...
    top.mainloop()
