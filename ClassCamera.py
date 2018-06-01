import os, time, sys, json, platform
import subprocess
import ClassUtils, MyException
from PIL import Image, ImageDraw, ImageFont, ImageTk
import ClassFaceAPI as FaceAPI

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
api_key = config['api_key']
host = config['host']
personGroupId = config['personGroupId']


def takePicture(personGroupId, delay, type='Identify', size='small'):
    cameras = config['camera'].split(',')
    for camera in cameras:
        if camera == '*opencv':
            return takePicture_opencv(personGroupId, delay, type)
        elif camera == '*CSIcamera':
            return takePicture_CSI(personGroupId, delay, size)
    return takePicture_CSI(personGroupId, delay, size)


def takePicture_CSI(personGroupId, delay, size='small'):
    # delay in ms 3000ms = 3s
    # jpgimagepath = os.path.join(basepath, 'takepictures', personGroupId + "_" + time.strftime(
    #     "%Y%m%d_%H%M%S", time.localtime()) + ".jpg")
    picturepath = ClassUtils.getTakePicturePath(personGroupId)
    if not os.path.exists(os.path.dirname(picturepath)):
        os.makedirs(os.path.dirname(picturepath))
    try:
        # small for 辨識，加快速度。
        if size == 'small':
            subprocess.call([
                'raspistill', '-hf', '-w', '800', '-h', '450', '-t',
                str(delay), '-o', picturepath
            ])
        else:  # for 訓練。訓練用圖片可以比較大
            subprocess.call([
                'raspistill', '-hf', '-w', '1600', '-h', '900', '-t',
                str(delay), '-o', picturepath
            ])

    except OSError:
        # ClassMessageBox.FaceAPIErrorGUI('def takePicture_CSI', 'CSI 攝影機無法啟動！',
        #                                 'OSError: raspistill 無法執行或不存在！！')
        print('def takePicture_CSI', 'CSI 攝影機無法啟動！',
              'OSError: raspistill 無法執行或不存在！！')
        return None

    #os.system("raspistill -t " + str(delay) + " -o " + imagepath)
    return picturepath


def show_opencv(type, mirror=False):
    ''' 顯示主畫面 '''
    import cv2
    import numpy as np

    cam = cv2.VideoCapture(0)
    cam.set(3, 1280)  # 修改解析度 寬
    cam.set(4, 1280 // 16 * 9)  # 修改解析度 高
    print('WIDTH', cam.get(3), 'HEIGHT', cam.get(4))  # 顯示預設的解析度
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        H, W = img.shape[:2]
        #imS = cv2.resize(img, (W, H))

        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
        pil_im = Image.fromarray(cv2_im)
        draw = ImageDraw.Draw(pil_im)  # 括号中为需要打印的canvas，这里就是在图片上直接打印

        ttf = ClassUtils.getSystemFont()

        font = ImageFont.truetype(ttf, 40, encoding="utf-8")
        hintfont = ImageFont.truetype(ttf, 24, encoding="utf-8")

        title = config['title'] + ""
        w, h = draw.textsize(title, font=font)
        draw.rectangle(
            ((W / 2 - w / 2 - 5, 0), (W / 2 + w / 2 + 5, h + 20)),
            fill="black")
        titlelocation = (W / 2 - w / 2, 5)
        #textlocation = (0,0)
        draw.text(
            titlelocation, title, (0, 255, 255),
            font=font)  # 第一个参数为打印的坐标，第二个为打印的文本，第三个为字体颜色，第四个为字体

        if type == 'Identify':
            hint = "請按「ENTER」進行簽到"
        elif type == 'Train':
            hint = "請按「ENTER」進行三連拍"
        else:
            hint = "請按「ENTER」繼續"
        w, h = draw.textsize(hint, font=hintfont)
        draw.rectangle(
            ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="red")
        hintlocation = (W / 2 - w / 2, H - h)
        #textlocation = (0,0)
        draw.text(
            hintlocation, hint, (0, 255, 255),
            font=hintfont)  # 第一个参数为打印的坐标，第二个为打印的文本，第三个为字体颜色，第四个为字体

        cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)

        if ClassUtils.isWindows():
            cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN,
                                  cv2.WINDOW_FULLSCREEN)

        cv2.imshow("window", cv2_text_im)
        #cv2.imshow("window", img)

        key = cv2.waitKey(1)
        if key == ord(' ') or key == 3 or key == 13:  # space or enter
            picturepath = ClassUtils.getTakePicturePath(config['personGroupId'])
            cv2.imwrite(picturepath, img)
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            return picturepath
        elif key == 27:  # esc to quit
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            raise MyException.esc_opencv("偵測到 esc 結束鏡頭")
        else:
            if key != -1:
                print('key=', key)


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


def __tk_UnknownPerson(text, facepath, picture):
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
    pil_image = pil_image.resize((maxwidth, int(height * maxwidth / width) ),
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

    b2 = tk.Button(
        top, text='下一位！', width=15, height=2, command=top.destroy)
    b2.pack()
    #top.bind('<Return>', lambda x: top.destroy())

    top.lift()
    top.call('wm', 'attributes', '.', '-topmost', '1')
    # Code to add widgets will go here...
    top.mainloop()


def __cv_ImageText(title, hint, facepath=None, picture=None, identifyfaces=None):
    ''' 標準 cv 視窗'''
    import cv2
    import numpy as np
    if facepath == None:
        img = np.zeros((400, 400, 3), np.uint8)
        img.fill(90)
    else:
        img = cv2.imread(facepath)
        print('__cv_ImageText.imagepath=', facepath)
        H, W = img.shape[:2]
        img = cv2.resize(img, (400, int(H / W * 400)))

    windowname = facepath
    H, W = img.shape[:2]

    #img = cv2.resize(img, (400,int(H/W*400)))

    ttf = ClassUtils.getSystemFont()

    cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # cv2和PIL中颜色的hex码的储存顺序不同
    pil_im = Image.fromarray(cv2_im)
    draw = ImageDraw.Draw(pil_im)  # 括号中为需要打印的canvas，这里就是在图片上直接打印
    titlefont = ImageFont.truetype(ttf, 24, encoding="utf-8")
    hintfont = ImageFont.truetype(ttf, 18, encoding="utf-8")

    w, h = draw.textsize(title, font=titlefont)
    draw.rectangle(
        ((W / 2 - w / 2 - 5, 0), (W / 2 + w / 2 + 5, h + 20)), fill="black")
    titlelocation = (W / 2 - w / 2, 5)
    w, h = draw.textsize(hint, font=hintfont)
    draw.rectangle(
        ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="red")
    hintlocation = (W / 2 - w / 2, H - h)
    draw.text(
        titlelocation, title, (0, 255, 255),
        font=titlefont)  # 第一个参数为打印的坐标，第二个为打印的文本，第三个为字体颜色，第四个为字体
    draw.text(
        hintlocation, hint, (0, 255, 255),
        font=hintfont)  # 第一个参数为打印的坐标，第二个为打印的文本，第三个为字体颜色，第四个为字体

    cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    cv2.imshow(windowname, cv2_text_im)
    key = cv2.waitKey(10000)
    if key == ord(' ') or key == 3 or key == 13:  # space or enter
        cv2.destroyWindow(windowname)
    elif key == ord('a') and len(identifyfaces)==1:  # 鍵盤 a 代表要新增 oneshot
        cv2.destroyWindow(windowname)
        __tk_UnknownPerson('您哪位？', facepath, picture)


def cv_Identifyfaces(identifyfaces, picture=None):
    ''' 運用 cv2 技術顯示的 Identifyfaces '''
    import cv2
    import numpy as np
    # print('identifyfaces=',identifyfaces)
    if len(identifyfaces) == 0:
        __cv_ImageText('沒有偵測到任何人！', '請按「ENTER」繼續')
        return
    for identifyface in identifyfaces:
        faceimagepath = ClassUtils.getFaceImagepath(identifyface['faceId'])
        if 'person' not in identifyface:
            print('identifyface=', identifyface)
            __cv_ImageText('你哪位？請先訓練。', '按 ENTER 繼續', faceimagepath, picture, identifyfaces)
        else:
            try:
                print(
                    ClassUtils.protectPersonName(
                        identifyface['person']['name']), '簽到成功!')
            except UnicodeEncodeError as e:
                print('姓名編碼錯誤!', '簽到成功!')

            #print('cv_Identifyfaces.identifyface=', identifyface)
            __cv_ImageText(
                ClassUtils.protectPersonName(identifyface['person']['name']) +
                '簽到成功!', '按 ENTER 繼續', faceimagepath, picture, identifyfaces)


def cv_Success(successes):
    ''' 運用 cv2 技術顯示的 Success '''
    import cv2
    import numpy as np
    print('successes=', successes)
    if len(successes) == 0:
        __cv_ImageText('無人簽到成功', '請按「ENTER」繼續')
        return
    for success in successes:
        # print(success['person']['name'], '簽到成功!')
        faceimagepath = ClassUtils.getFaceImagepath(success['faceId'])

        __cv_ImageText(
            ClassUtils.protectPersonName(success['person']['name']) + '簽到成功!',
            '按 ENTER 繼續')


def takePicture_opencv(personGroupId, delay, type):
    sysstr = platform.system()
    print('os=', sysstr, platform.release())
    if (ClassUtils.isWindows() or ClassUtils.isDarwin()):
        picturepath = show_opencv(type, mirror=True)
        return picturepath
    else:
        print('若系統為樹莓派，則需設定 camera 為 CSIcamera 無法以 webcam 作為影像來源。')
        return None


'''
def takePicture_Picamera(personGroupId, delay):
    # 安裝 sudo apt-get install python3-picamera
    # 預設解析度1280x800
    imagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(imagepath)):
        os.makedirs(os.path.dirname(imagepath))
    
    with picamera.PiCamera() as camera:
        camera.start_preview()
        sleep(delay)
        camera.capture(imagepath)
        return imagepath
'''