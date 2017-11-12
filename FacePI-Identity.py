import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import os, sys, time, csv
import tkinter
from tkinter import Text

#from IPython.display import Image
#from IPython.display import display
from PIL import Image

basepath = os.path.dirname(os.path.realpath(__file__))

with open(basepath + '/FacePI-Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']

imagepaths = []
if len(sys.argv) < 2:
    print(sys.argv[0] + " <personGroupid> 即時拍照辨識")
    print(sys.argv[0] + " <personGroupid> <imagepath>... 直接指定圖片進行辨識")
    sys.exit()


def takePicture():
    imagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(imagepath)):
        os.makedirs(os.path.dirname(imagepath))
    os.system("raspistill -t 3000 -o " + imagepath)
    return imagepath


personGroupId = sys.argv[1]
if len(sys.argv) == 2:
    imagepaths.append(takePicture())
if len(sys.argv) == 3:
    imagepaths = sys.argv[2:]


def identify(faceids, personGroupId):
    print("開始辨識。")
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({})

    requestbody = '''{
        "personGroupId": "''' + personGroupId + '''",
        "faceIds":''' + str(faceids) + ''',
        "maxNumOfCandidatesReturned":1,
        "confidenceThreshold": 0.5
    }'''

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", "/face/v1.0/identify?%s" % params, requestbody,
                     headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        facejson = json.loads(str(data, 'UTF-8'))
        #print(facejson)
        conn.close()
        return facejson
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        sys.exit()


def get_a_person(personGroupId, personId):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                     "/persons/" + personId + "?%s" % params, "{body}",
                     headers)
        response = conn.getresponse()
        data = response.read()
        personjson = json.loads(str(data, 'UTF-8'))
        conn.close()
        print("get_a_person = " + str(personjson))
        return personjson
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def list_persons_in_group(personGroupId):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        #'start': '{string}',
        #'top': '1000',
    })

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                     "/persons?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        persons = json.loads(str(data, 'UTF-8'))
        conn.close()
        return persons
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def DetectingLocal(imagepath):
    headers = {
        # Request headers
        #'Content-Type': 'application/json',
        'Content-Type': 'application/octet-stream',  # 用本地圖檔辨識
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId':
        'true',
        'returnFaceLandmarks':
        'false',
        'returnFaceAttributes':
        'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure',
    })

    #requestbody = '{"url":"'+imageurl+'"}'
    #requestbody = open('face1.JPG', "rb").read()
    requestbody = open(imagepath, "rb").read()

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody,
                     headers)
        response = conn.getresponse()
        data = response.read()
        #print(data)
        faces = json.loads(str(data, 'UTF-8'))
        #print(parsed[0]['faceId'])
        #faceids.append(parsed[0]['faceId'])
        conn.close()

        print(imagepath + "偵測到 {0} 個人".format(len(faces)))
        #display(Image(filename=imagepath))
        for face in faces:
            #print("face = ", face)
            print("faceRectangle = ", face['faceRectangle'])
            print("faceId = ", face['faceId'])
            left = face['faceRectangle']['left']
            top = face['faceRectangle']['top']
            height = face['faceRectangle']['height']
            width = face['faceRectangle']['width']

            img = Image.open(imagepath)
            #faceRectangle =  {'top': 141, 'height': 261, 'width': 261, 'left': 664}
            img2 = img.crop((left, top, left + width, top + height))

            saveimage = basepath + "/tmp/" + face['faceId'] + ".gif"
            if not os.path.exists(os.path.dirname(saveimage)):
                os.makedirs(os.path.dirname(saveimage))
            img2.save(saveimage, 'GIF')
            #display(img2)
            #area = (left, top, left+width, top+height)
            #cropped_img = img.crop(area)
            #cropped_img.show()
        return faces
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


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
    top = tkinter.Tk()
    top.geometry('400x400')
    top.title(text)
    #img = Image.open(imagepath)
    #img.save(imagepath+".gif", 'GIF')
    print("訓練新人: imagepath=" + imagepath)

    imagefile = tkinter.PhotoImage(file=imagepath)
    maxwidth = 160
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)
    canvas = tkinter.Canvas(
        top, height=imagefile.height(), width=imagefile.width())

    image = canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    label = tkinter.Label(top, text=text, font=('Arial', 20))
    label.pack()

    #frame = tkinter.Frame(master=top).grid(row=1, column=2)
    label1 = tkinter.Label(top, text='請輸入學號：', font=('Arial', 18))
    label1.pack()
    e = tkinter.Entry(top, font=("Calibri", 24), width=10, show="")
    e.pack()
    e.insert(0, "在此輸入學號")

    b1 = tkinter.Button(
        top,
        text='記住我！',
        width=15,
        height=4,
        command=lambda: train(top, e, imagepath))
    b1.pack()

    b2 = tkinter.Button(
        top, text='下一位！', width=15, height=4, command=top.destroy)
    b2.pack()

    # Code to add widgets will go here...
    top.mainloop()


def showGUI(text, imagepath):
    top = tkinter.Tk()
    top.geometry('400x400')
    top.title(text)
    ###image = ImageTk.PhotoImage(Image.open("./tmp/"+face['faceId']+".jpg"))
    #image = tkinter.PhotoImage(file=("./tmp/"+face['faceId']+".jpg"))
    ###labelimage = tkinter.Label(top, image=image)
    ###labelimage.pack()

    img = Image.open(imagepath)
    img.save(imagepath + ".gif", 'GIF')

    imagefile = tkinter.PhotoImage(file=imagepath + ".gif")
    maxwidth = 200
    h = imagefile.height()
    w = imagefile.width()
    if w > maxwidth:
        imagefile = imagefile.subsample(w // maxwidth, w // maxwidth)

    canvas = tkinter.Canvas(
        top, height=imagefile.height(), width=imagefile.width())

    image = canvas.create_image(10, 10, anchor="nw", image=imagefile)
    canvas.pack()

    label = tkinter.Label(top, text=text, font=('Arial', 20))
    label.pack()

    b1 = tkinter.Button(
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


##################################################################################################
### main
##################################################################################################
id_names = {}
with open(basepath + "/data/id_name.csv", "rt") as infile:
    reader = csv.reader(infile)
    headers = next(reader)[0:]
    for row in reader:
        id_names[row[0]] = {key: value for key, value in zip(headers, row[0:])}

persons = list_persons_in_group(personGroupId)
print("list_persions personGroupId=" + personGroupId)
for person in persons:
    print(person["name"], person["personId"])

faceids = {}

#for imageurl in imageurls:
#    faceids.append(Detecting(imageurl))
for imagepath in imagepaths:
    for face in DetectingLocal(imagepath):
        faceids[face['faceId']] = imagepath

print("faceids=", list(faceids.keys()))

facejsons = identify(list(faceids.keys()), personGroupId)
print("facejsons=", facejsons, type(facejsons))

for facejson in facejsons:
    print("facejson type = ", type(facejson), "  ", facejson == 'error')
    #if facejson == 'error':
    #    break
    #display(Image(filename="tmp/"+facejson['faceId']+".jpg"))
    text = "恐怖喔，你確定有人嗎？"
    if facejson == 'error':
        print(imagepaths)
        showGUI(text, imagepaths[0])
    elif facejson != 'error' and len(facejson['candidates']) > 0:
        confidence = facejson["candidates"][0]["confidence"]
        print("personId: " + facejson["candidates"][0]["personId"] + ", 信心指數："
              + str(confidence))
        personjson = get_a_person(personGroupId,
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
            text = "" + name + " 報到成功！"
        elif confidence >= 0.7:
            if personjson['name'] in id_names.keys():
                name = id_names[personjson['name']]['name']
            else:
                name = personjson['name']
            text = name + " 報到成功！"
        elif confidence >= 0.5:
            if personjson['name'] in id_names.keys():
                name = id_names[personjson['name']]['姓名']
            else:
                name = personjson['name']
            text = name + " 報到成功！"

        print(text)
        showGUI(text, basepath + "/tmp/" + facejson['faceId'] + ".gif")
    elif facejson != 'error' and len(facejson['candidates']) == 0:
        text = "哈囉，你哪位？"
        imagepath = basepath + "/tmp/" + facejson['faceId'] + ".gif"
        trainNewPerson(text, imagepath)
