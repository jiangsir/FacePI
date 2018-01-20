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
    newpersonid = e.get()
    print(newpersonid)
    if newpersonid != None and newpersonid.strip() != '':
        os.system('python3 ' + basepath + '/FacePI-Train.py ' + personGroupId +
                  ' ' + newpersonid + ' ' + imagepath)
    top.destroy()
    sys.exit()

def trainNewPerson(text, imagepath):
    # 當辨識不到人的時候，跳這個畫面。以便用這個圖片去訓練新人。
    top = tk.Tk()
    top.geometry('400x400')
    top.title(text)
    #img = Image.open(imagepath)
    #img.save(imagepath+".gif", 'GIF')
    print("訓練新人: imagepath=" + imagepath)

    imagefile = tk.PhotoImage(file=imagepath)
    maxwidth = 160
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)
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
        text='記住我！',
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
    imagepath = Camera.takePicture(personGroupId)
    faces = faceapi.detectLocalImage(imagepath)
    print('faces[',len(faces),'] = ', faces)
    faceids = {}
    for face in faces:
        faceids[face['faceId']] = imagepath
    print('faceids =', faceids)
    facejsons = faceapi.identify(list(faceids.keys()), personGroupId)
    print("facejsons=", facejsons, type(facejsons))
    if 'error' in facejsons and 'not trained' in facejsons['error']['message']:
        persongroupapi.train_personGroup(personGroupId)
        persongroupapi.personGroup_status(personGroupId)
        facejsons = faceapi.identify(list(faceids.keys()), personGroupId)
    
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
            personjson = persongroupapi.get_a_person(personGroupId,
                                    facejson["candidates"][0]["personId"])
            text = ""
            if 'error' in personjson.keys():
                text = "查無此人！"
                imagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
                trainNewPerson(text, imagepath)
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
            imagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
            trainNewPerson(text, imagepath)


b2 = tk.Button(
    top, text='簽到', font=font_helv36, width=10, height=5, command=Signin)
b2.pack()

# Code to add widgets will go here...
top.mainloop()
