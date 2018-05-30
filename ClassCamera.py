import os, time, sys, json, platform
import subprocess
import ClassUtils, MyException
from PIL import Image, ImageDraw, ImageFont

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


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
    jpgimagepath = ClassUtils.getTakePicturePath(personGroupId)
    if not os.path.exists(os.path.dirname(jpgimagepath)):
        os.makedirs(os.path.dirname(jpgimagepath))
    try:
        # small for 辨識，加快速度。
        if size == 'small':
            subprocess.call([
                'raspistill', '-hf', '-w', '800', '-h', '450', '-t',
                str(delay), '-o', jpgimagepath
            ])
        else:  # for 訓練。訓練用圖片可以比較大
            subprocess.call([
                'raspistill', '-hf', '-w', '1600', '-h', '900', '-t',
                str(delay), '-o', jpgimagepath
            ])

    except OSError:
        # ClassMessageBox.FaceAPIErrorGUI('def takePicture_CSI', 'CSI 攝影機無法啟動！',
        #                                 'OSError: raspistill 無法執行或不存在！！')
        print('def takePicture_CSI', 'CSI 攝影機無法啟動！',
              'OSError: raspistill 無法執行或不存在！！')
        return None

    #os.system("raspistill -t " + str(delay) + " -o " + imagepath)
    return jpgimagepath


def show_opencv(type, mirror=False):
    import cv2
    import numpy as np

    cam = cv2.VideoCapture(0)
    cam.set(3,1280) # 修改解析度 寬
    cam.set(4,1280//16*9) # 修改解析度 高
    print('WIDTH',cam.get(3),'HEIGHT',cam.get(4)) # 顯示預設的解析度
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

        if type=='Identify':
            hint = "請按「ENTER」進行簽到"
        elif type=='Train':
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
            imagepath = ClassUtils.getTakePicturePath(config['personGroupId'])
            cv2.imwrite(imagepath, img)
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            return imagepath
        elif key == 27:  # esc to quit
            cv2.destroyAllWindows()
            cv2.VideoCapture(0).release()
            raise MyException.esc_opencv("偵測到 esc 結束鏡頭")
        else:
            if key != -1:
                print('key=', key)

def __cv_ImageText(title, hint, imagepath=None):
    ''' 標準 cv 視窗'''
    import cv2
    import numpy as np
    if imagepath == None:    
        img = np.zeros((400, 400, 3), np.uint8)
        img.fill(90)
    else:
        img = cv2.imread(imagepath)
        print('__cv_ImageText.imagepath=', imagepath)
        H, W = img.shape[:2]
        img = cv2.resize(img, (400,int(H/W*400))) 

    windowname = imagepath
    H, W = img.shape[:2]

    #img = cv2.resize(img, (400,int(H/W*400))) 
    
    # if ClassUtils.isDarwin():
    #     ttf = "/Library/Fonts/Arial Unicode.ttf"
    # elif ClassUtils.isWindows7():
    #     ttf = "simhei.ttf"
    # elif ClassUtils.isWindows10():
    #     ttf = "C:/Windows/Fonts/Arial.ttf"
    # else:
    #     ttf = "simhei.ttf"

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
        ((W / 2 - w / 2 - 5, H-h), (W / 2 + w / 2 + 5, H)), fill="red")
    hintlocation = (W / 2 - w / 2, H-h)
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

''' 運用 cv2 技術顯示的 Identifyfaces '''
def cv_Identifyfaces(identifyfaces):
    import cv2
    import numpy as np
    # print('identifyfaces=',identifyfaces)
    if len(identifyfaces) == 0:
        __cv_ImageText('沒有偵測到任何人！', '請按「ENTER」繼續')
        return
    for identifyface in identifyfaces:
        imagepath = ClassUtils.getFaceImagepath(identifyface['faceId'])
        if 'person' not in identifyface:
            print('identifyface=', identifyface)
            __cv_ImageText('你哪位？請先訓練。', '按 ENTER 繼續', imagepath)
        else:
            #print(identifyface['person']['name'], '簽到成功!')
            #print('cv_Identifyfaces.identifyface=', identifyface)
            __cv_ImageText(ClassUtils.protectPersonName(
                identifyface['person']['name']) + '簽到成功!', '按 ENTER 繼續', imagepath)

''' 運用 cv2 技術顯示的 Success '''
def cv_Success(successes):
    import cv2
    import numpy as np
    print('successes=',successes)
    if len(successes) == 0:
        __cv_ImageText('無人簽到成功', '請按「ENTER」繼續')
        return
    for success in successes:
        print(success['person']['name'], '簽到成功!')
        imagepath = ClassUtils.getFaceImagepath(success['faceId'])

        __cv_ImageText(ClassUtils.protectPersonName(
            success['person']['name']) + '簽到成功!', '按 ENTER 繼續', imagepath)


def takePicture_opencv(personGroupId, delay, type):
    sysstr = platform.system()
    print('os=', sysstr, platform.release, platform.system_alias, platform.version)
    if (ClassUtils.isWindows() or ClassUtils.isDarwin()):
        jpgimagepath = show_opencv(type, mirror=True)
        return jpgimagepath
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