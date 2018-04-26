import tkinter as tk
from tkinter import font
from tkinter import Text
import os, sys, json, time, csv
from PIL import Image

import ClassFaceAPI as FaceAPI
import ClassCamera as Camera
import ClassGPIO


basepath = os.path.dirname(os.path.realpath(__file__))

with open(basepath + '/Config.json', 'r') as f:
    config = json.load(f)
print(config)

api_key = config['api_key']
host = config['host']
#api_key = "90dd6135652e45ba8ad9d222b4643545" # 透過 github 帳戶獲得的 api key
#host = "westcentralus.api.cognitive.microsoft.com"

#api_key = "f3e388f66ee146d3b6e96f6ca2ac25d3"
#host = "eastasia.api.cognitive.microsoft.com"
#personGroupId = "junior"
#title = "高師大附中 刷臉簽到系統"
personGroupId = config['personGroupId']
title = config['title']

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
    print('imagepath=', imagepath)
    newpersonname = e.get()
    print("newpersonname=",newpersonname)
    personapi = FaceAPI.Person(api_key, host)
    person = personapi.getPersonByName(personGroupId, newpersonname)
    print('getPersonByName: person=',person)
    personGroupapi = FaceAPI.PersonGroup(api_key, host)
    if person == None:
        print('call create_a_person')
        personid = personapi.create_a_person(personGroupId, newpersonname, 'unknown descript')
        personapi.add_a_person_face(imagepath, personid, personGroupId)
    else:
        print('call add_a_person_face, personId=', person['personId'])
        personapi.add_a_person_face(imagepath, person['personId'], personGroupId)
    print('FROM train()')
    personGroupapi.train_personGroup(personGroupId)
    top.destroy()
    #sys.exit()

def YesMe(top, personname, gifimagepath):
    personapi = FaceAPI.Person(api_key, host)
    person = personapi.getPersonByName(personGroupId, personname)
    personapi.add_a_person_face(gifimagepath, person['personId'], personGroupId)
    top.destroy()

def trainNewPersonGUI(text, gifimagepath):
    # 當辨識不到人的時候，跳這個畫面。以便用這個圖片去訓練新人。
    #top = tk.Tk()
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title(text)
    print("訓練新人: gifimagepath=" + gifimagepath)
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

    imagefile = tk.PhotoImage(file=gifimagepath)
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
        text='記住我！',
        width=15,
        height=3,
        command=lambda: train(top, e, gifimagepath))
    b1.pack()

    b2 = tk.Button(
        top, text='下一位！', width=15, height=2, command=top.destroy)
    b2.pack()

    # Code to add widgets will go here...
    top.mainloop()



def NotMeGUI(top, gifimagepath):
    # 辨識出來，但是不是正確的人。
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title('')
    print("不是我！: gifimagepath=" + gifimagepath)

    imagefile = tk.PhotoImage(file=gifimagepath)
    maxwidth = 160
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)
    print('h=', imagefile.height() , 'w=', imagefile.width())
    canvas = tk.Canvas(top, height=imagefile.height(), width=imagefile.width())

    image = canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    label = tk.Label(top, text='', font=('Arial', 20))
    label.pack()

    #frame = tkinter.Frame(master=top).grid(row=1, column=2)
    label1 = tk.Label(top, text='請輸入學號(目前僅接受英數文字)：', font=('Arial', 18))
    label1.pack()
    e = tk.Entry(top, font=("Calibri", 24), width=10, show="")
    e.pack()
    e.insert(0, "")

    b1 = tk.Button(
        top,
        text='記住我！',
        width=15,
        height=4,
        command=lambda: train(top, e, gifimagepath))
    b1.pack()

    b2 = tk.Button(
        top, text='下一位！', width=15, height=4, command=top.destroy)
    b2.pack()

    # Code to add widgets will go here...
    top.mainloop()


def showGUI(personname, imagepath, text):
    #top = tk.Tk() # 直接 Tk() 會出現 pyimage2 not found 的問題，改成 tk.Toplevel()
    top = tk.Toplevel()
    top.geometry('400x400')
    top.title(personname + text)
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

    label = tk.Label(top, text=personname + text, font=('Arial', 20))
    label.pack()
    if personname == '__Nobody':
        b1 = tk.Button(top, text='下一位！', width=15, height=4, command=top.destroy)
        b1.pack()
    else:
        b1 = tk.Button(
            top, text='下一位！', width=15, height=2, command=lambda: YesMe(top, personname, imagepath + ".gif"))
        b1.pack()
        b2 = tk.Button(
            top, text='我不是'+personname+'！', width=15, height=2, command=lambda: NotMeGUI(top, imagepath+".gif"))
        b2.pack()

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
    
    #config
    #imagepath = Camera.takePicture_CSI(personGroupId, 2000)
    imagepath = Camera.takePicture(personGroupId, 2000)

    faces = faceapi.detectLocalImage(imagepath)
    print('本地圖片偵測到 ',len(faces),' 人, faces=', faces)
    if len(faces) == 0:
        showGUI('__Nobody', imagepath, "本圖片沒有偵測到任何人！")

    faceids = {}
    for face in faces:
        faceids[face['faceId']] = imagepath
    print('faceids =', faceids)
    facejsons = faceapi.identify(list(faceids.keys()), personGroupId)
    if 'error' in facejsons:
        status = persongroupapi.personGroup_status(personGroupId)
        if status['status'] == 'failed' and 'no persisted faces of person' in status['message']:
            gifimagepath = basepath + "/tmp/" + list(faceids.keys())[0] + ".gif"
            trainNewPersonGUI('jsjsjs', gifimagepath)

    print("facejsons=", facejsons, type(facejsons))
    
    for facejson in facejsons:
        print("facejson type = ", type(facejson), "  ", facejson == 'error')            
        #if facejson == 'error':
        #    break
        #display(Image(filename="tmp/"+facejson['faceId']+".jpg"))
        text = ""
        if facejson == 'error' and 'PersonGroupNotTrained' in facejsons['error']['code']:
            gifimagepath = basepath + "/tmp/" + list(faceids.keys())[0] + ".gif"
            persongroupapi.train_personGroup(personGroupId)
            trainNewPersonGUI('訓練一個人群', gifimagepath)
            #showGUI(text, imagepath)
        elif facejson != 'error' and len(facejson['candidates']) > 0:
            confidence = facejson["candidates"][0]["confidence"]
            print("personId: " + facejson["candidates"][0]["personId"] + ", 信心指數："
                + str(confidence))
            personjson = personapi.get_a_person(
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
                text = " 報到成功！！！" + str(confidence)
                ClassGPIO.RelayExchange()
                showGUI(name, basepath + "/tmp/" + facejson['faceId'] + ".gif", text)
            elif confidence >= 0.7:
                if personjson['name'] in id_names.keys():
                    name = id_names[personjson['name']]['name']
                else:
                    name = personjson['name']
                text = " 報到成功！！" + str(confidence)
                ClassGPIO.RelayExchange()
                showGUI(name, basepath + "/tmp/" + facejson['faceId'] + ".gif", text)
#            elif confidence >= 0.5:
#                if personjson['name'] in id_names.keys():
#                    name = id_names[personjson['name']]['name']
#                else:
#                    name = personjson['name']
#                text = name + " 報到成功！"
            else:
                gifimagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
                trainNewPersonGUI(text, gifimagepath)
        elif facejson != 'error' and len(facejson['candidates']) == 0:
            text = "哈囉，你哪位？"
            gifimagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
            trainNewPersonGUI(text, gifimagepath)


b2 = tk.Button(
    top, text='簽到', font=font_helv36, width=10, height=5, command=Signin)
b2.pack()

# Code to add widgets will go here...
top.mainloop()
