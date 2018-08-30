from PIL import Image, ImageDraw, ImageFont, ImageTk
import os, json
import ClassFaceAPI as FaceAPI
import ClassUtils

basepath = os.path.dirname(os.path.realpath(__file__))
# with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
#     config = json.load(f)

config = ClassUtils.loadConfig()

api_key = config['api_key']
host = config['host']
personGroupId = config['personGroupId']
traindataspath = os.path.join(basepath , 'traindatas')


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
    save_traindatas(personname, imagepath)
    top.destroy()

def save_traindatas(personname, imagepath):
    ''' 在 oneshot 視窗輸入姓名的人, 順便紀錄到 traindatas 內以便未來整體移植 '''
    
    traindatas_personname = os.path.join(traindataspath, personGroupId, personname, os.path.basename(imagepath))
    if not os.path.exists(os.path.dirname(traindatas_personname)):
        os.makedirs(os.path.dirname(traindatas_personname))
    
    os.rename(imagepath, traindatas_personname)


def tk_UnknownPerson(text, facepath, picture, personname=None):
    ''' # 當不認識的時候，跳這個畫面。以便用這個圖片去訓練新人。 '''
    import tkinter as tk

    top = tk.Tk()
    top.attributes("-topmost", True)


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
    e.focus()
    if personname==None:
        personname = ""
    e.insert(0, personname)

    b1 = tk.Button(
        top,
        text='記住我！',
        width=15,
        height=3,
        command=lambda: train_oneShot(top, e, e.get(), 'oneshot', picture))
    b1.bind("<Return>", lambda x: train_oneShot(top, e, e.get(), 'oneshot', picture))
    b1.pack()

    b2 = tk.Button(top, text='下一位！', width=15, height=2, command=top.destroy)
    b2.bind("<Return>", lambda x:top.destroy())
    b2.pack()
    #top.bind('<Return>', lambda x: top.destroy())
    top.bind('<Escape>', lambda x:top.destroy())
    
    #top.call('wm', 'attributes', '.', '-topmost', '1')
    # top.lift()

    # Code to add widgets will go here...
    top.mainloop()
