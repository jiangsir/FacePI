import tkinter as tk
from tkinter import font
from tkinter import Text
import os, sys, json, time, csv
import FaceAPI, Camera
from PIL import Image

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

id_names = {}
with open(basepath + "/data/id_name.csv", "rt") as infile:
    reader = csv.reader(infile)
    headers = next(reader)[0:]
    for row in reader:
        id_names[row[0]] = {key: value for key, value in zip(headers, row[0:])}


def close_window(top):
    top.destroy()
    sys.exit()


def train(top, e, imagepath):
    newpersonname = e.get()
    print(newpersonname)
    personapi = FaceAPI.Person(api_key, host)
    personGroupapi = FaceAPI.PersonGroup(api_key, host)
    personid = personapi.create_a_person(personGroupId, newpersonname, 'unknown descript')
    personapi.add_a_person_face(imagepath, personid, personGroupId)
    print('FROM train()')
    personGroupapi.train_personGroup(personGroupId)

    top.destroy()
    #sys.exit()

def trainNewPersonGUI(text, gifimagepath):
    # 當辨識不到人的時候，跳這個畫面。以便用這個圖片去訓練新人。
    #top = tk.Tk()
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title(text)
    print("訓練新人: imagepath=" + imagepath)
    # 把圖片轉成 gif
    #img = Image.open(imagepath)
    #faceRectangle =  {'top': 141, 'height': 261, 'width': 261, 'left': 664}
    #img2 = img.crop((left, top, left + width, top + height))

    #saveimage = basepath + "/tmp/" + face['faceId'] + ".gif"
    #if not os.path.exists(os.path.dirname(saveimage)):
    #    os.makedirs(os.path.dirname(saveimage))
    #img2.save(saveimage, 'GIF')

    #img = Image.open(imagepath)
    #img.save(imagepath+".gif", 'GIF')

    imagefile = tk.PhotoImage(file=imagepath)
    maxwidth = 160
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)
    print('h=', imagefile.height() , 'w=', imagefile.width())
    canvas = tk.Canvas(top, height=imagefile.height(), width=imagefile.width())

    image = canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    label = tk.Label(top, text=text, font=('Arial', 20))
    label.pack()

    #frame = tkinter.Frame(master=top).grid(row=1, column=2)
    label1 = tk.Label(top, text='請輸入學號：', font=('Arial', 18))
    label1.pack()
    e = tk.Entry(top, font=("Calibri", 24), width=10, show="")
    e.pack()
    e.insert(0, "在此輸入學號")

    b1 = tk.Button(
        top,
        text='進行 5 連拍並記住我！',
        width=15,
        height=4,
        command=lambda: train(top, e, imagepath))
    b1.pack()

    b2 = tk.Button(
        top, text='下一位！', width=15, height=4, command=top.destroy)
    b2.pack()

    # Code to add widgets will go here...
    top.mainloop()


def showGUI(text, imagepath):
    #top = tk.Tk() # 直接 Tk() 會出現 pyimage2 not found 的問題，改成 tk.Toplevel()
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title(text)
    ###image = ImageTk.PhotoImage(Image.open("./tmp/"+face['faceId']+".jpg"))
    #image = tkinter.PhotoImage(file=("./tmp/"+face['faceId']+".jpg"))
    ###labelimage = tkinter.Label(top, image=image)
    ###labelimage.pack()
    print('showGUI imagepath=', imagepath)
    img = Image.open(imagepath)
    img.save(imagepath + ".gif", 'GIF')

    imagefile = tk.PhotoImage(file=imagepath + ".gif")
    maxwidth = 200
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)

    print('imagefile=', imagefile)
    canvas = tk.Canvas(top, height=imagefile.height(), width=imagefile.width())
    
    image = canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    label = tk.Label(top, text=text, font=('Arial', 20))
    label.pack()

    b1 = tk.Button(
        top, text='下一位！', width=15, height=2, command=top.destroy)
    b1.pack()

    # Code to add widgets will go here...
    top.mainloop()
    #win=tk.Tk()     #建立視窗容器物件
    #win.title("Tk GUI")
    #label=tk.Label(win, text=text)   #建立標籤物件
    #label.pack()       #顯示元件
    #button=tk.Button(win, text="OK")
    #button.pack()     #顯示元件
    #win.mainloop()


def Signin():
    faceapi = FaceAPI.Face(api_key, host)
    persongroupapi = FaceAPI.PersonGroup(api_key, host)
    personapi = FaceAPI.Person(api_key, host)

    status = persongroupapi.personGroup_status(personGroupId)
    if 'error' in status and status['error']['code'] == 'PersonGroupNotFound':
        persongroupapi.createPersonGroup(personGroupId, 'group name', 'group data')
        persongroupapi.train_personGroup(personGroupId)
    if 'error' in status and status['error']['code'] == 'PersonGroupNotTrained':
        persongroupapi.train_personGroup(personGroupId)
        
    imagepath = Camera.takePicture(personGroupId, 2000)
    faces = faceapi.detectLocalImage(imagepath)
    print('本地圖片偵測到 ',len(faces),' 人, faces=', faces)
    if len(faces) == 0:
        showGUI("本圖片沒有偵測到任何人！", imagepath)

    faceids = {}
    for face in faces:
        faceids[face['faceId']] = imagepath
    print('faceids =', faceids)
    facejsons = faceapi.identify(list(faceids.keys()), personGroupId)
    if 'error' in facejsons:
        status = persongroupapi.personGroup_status(personGroupId)
        if status['status'] == 'failed' and 'no persisted faces of person' in status['message']:
            gifimagepath = basepath + "/tmp/" + faceids.keys()[0] + ".gif"
            trainNewPersonGUI('jsjsjs', gifimagepath)

    print("facejsons=", facejsons, type(facejsons))
    
    for facejson in facejsons:
        print("facejson type = ", type(facejson), "  ", facejson == 'error')            
        #if facejson == 'error':
        #    break
        #display(Image(filename="tmp/"+facejson['faceId']+".jpg"))
        text = "恐怖喔，你確定有人嗎？"
        if facejson == 'error':
            showGUI(text, imagepath)
        elif facejson != 'error' and len(facejson['candidates']) > 0:
            confidence = facejson["candidates"][0]["confidence"]
            print("personId: " + facejson["candidates"][0]["personId"] + ", 信心指數："
                + str(confidence))
            personjson = persongroupapi.get_a_person(
                                    facejson["candidates"][0]["personId"], personGroupId)
            text = ""
            if 'error' in personjson.keys():
                text = "查無此人！"
                print('imagepath2=', imagepath)
                gifimagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
                trainNewPersonGUI(text, gifimagepath)
                sys.exit()
            elif confidence >= 0.9:
                if personjson['name'] in id_names.keys():
                    name = id_names[personjson['name']]['name']
                else:
                    name = personjson['name']
                text = "" + name + " 報到成功！！！"
            elif confidence >= 0.7:
                if personjson['name'] in id_names.keys():
                    name = id_names[personjson['name']]['name']
                else:
                    name = personjson['name']
                text = name + " 報到成功！！"
            elif confidence >= 0.5:
                if personjson['name'] in id_names.keys():
                    name = id_names[personjson['name']]['name']
                else:
                    name = personjson['name']
                text = name + " 報到成功！"

            print(text)
            showGUI(text, basepath + "/tmp/" + facejson['faceId'] + ".gif")
        elif facejson != 'error' and len(facejson['candidates']) == 0:
            text = "哈囉，你哪位？"
            gifimagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
            trainNewPersonGUI(text, gifimagepath)


b2 = tk.Button(
    top, text='簽到', font=font_helv36, width=10, height=5, command=Signin)
b2.pack()

# Code to add widgets will go here...
top.mainloop()
