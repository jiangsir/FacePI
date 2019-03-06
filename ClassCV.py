import time
import ClassUtils
import ClassTK
import MyException
import ClassCSV
import ClassDB
from PIL import Image, ImageDraw, ImageFont, ImageTk


def show_opencv(typee, hint='', mirror=False):
    ''' 顯示主畫面 '''
    import cv2
    import numpy as np
    config = ClassUtils.loadConfig()

    cam = cv2.VideoCapture(config['videoid'])
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
        # FreeAPIKEY: b9160fbd882f47bd821205a4bce64354
        if config['api_key'] == 'b9160fbd882f47bd821205a4bce64354':
            warningfont = ImageFont.truetype(ttf, 24, encoding="utf-8")
            warning = "請注意，您目前是用的是共用的測試 API_KEY 請儘速自行申請一個自用的 KEY"
            w, h = draw.textsize(warning, font=warningfont)
            draw.rectangle(
                ((W / 2 - w / 2 - 5, H - h * 2), (W / 2 + w / 2 + 5, H - h)),
                fill="yellow")
            warninglocation = (W / 2 - w / 2, H - h * 2)
            draw.text(
                warninglocation, warning, (0, 0, 255),
                font=warningfont)  # 第一个参数为打印的坐标，第二个为打印的文本，第三个为字体颜色，第四个为字体

        if typee == 'Identify':
            hints = "請按「ENTER」進行簽到" + hint
        elif typee == 'Train':
            hints = "請按「ENTER」進行三連拍" + hint
        else:
            hints = "請按「ENTER」繼續" + hint
        w, h = draw.textsize(hints, font=hintfont)
        draw.rectangle(
            ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="red")
        hintlocation = (W / 2 - w / 2, H - h)
        #textlocation = (0,0)
        draw.text(
            hintlocation, hints, (0, 255, 255),
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
            picturepath = ClassUtils.getTakePicturePath(
                config['personGroupId'])
            cv2.imwrite(picturepath, img)
            cv2.destroyAllWindows()
            cv2.VideoCapture(config['videoid']).release()
            return picturepath
        elif key == 27:  # esc to quit
            cv2.destroyAllWindows()
            cv2.VideoCapture(config['videoid']).release()
            raise MyException.esc_opencv("偵測到 esc 結束鏡頭")
        else:
            if key != -1:
                print('key=', key)


def cv_ImageText(title, hint, facepath=None, picture=None, identifyfaces=None, personname=None):
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

    if identifyfaces != None and len(identifyfaces) == 1:
        hint = hint + "或按 'a' 新增身份"
    w, h = draw.textsize(hint, font=hintfont)
    draw.rectangle(
        ((W / 2 - w / 2 - 5, H - h), (W / 2 + w / 2 + 5, H)), fill="red")
    hintlocation = (W / 2 - w / 2, H - h)
    draw.text(titlelocation, title, (0, 255, 255), font=titlefont)
    draw.text(hintlocation, hint, (0, 255, 0), font=hintfont)

    cv2_text_im = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
    cv2.imshow(windowname, cv2_text_im)
    key = cv2.waitKey(10000)
    if key == ord(' ') or key == 3 or key == 13:  # space or enter
        cv2.destroyWindow(windowname)
    elif key == ord('a') and len(identifyfaces) == 1:  # 鍵盤 a 代表要新增 oneshot
        cv2.destroyWindow(windowname)
        ClassTK.tk_UnknownPerson('您哪位？', facepath, picture, personname)


def cv_Identifyfaces(identifyfaces, picture=None):
    ''' 運用 cv2 技術顯示的 Identifyfaces '''
    import cv2
    import numpy as np
    # print('identifyfaces=',identifyfaces)
    if len(identifyfaces) == 0:
        cv_ImageText('沒有偵測到任何人！', '請按「ENTER」繼續')
        return
    for identifyface in identifyfaces:
        faceimagepath = ClassUtils.getFaceImagepath(identifyface['faceId'])
        if 'person' not in identifyface:
            print('identifyface=', identifyface)
            cv_ImageText('你哪位？請先訓練。', '按 ENTER 繼續', faceimagepath, picture,
                         identifyfaces)
        else:
            text = ClassUtils.textConfidence(identifyface['person']['name'],
                                             identifyface['confidence'])
            try:
                print(text, identifyface['confidence'])
            except UnicodeEncodeError as e:
                print("UnicodeEncodeERROR!!", identifyface['confidence'])
            #print('cv_Identifyfaces.identifyface=', identifyface)
            # text = ClassUtils.textConfidence(identifyface['person']['name'],
            #                                  identifyface['confidence'])
            cv_ImageText(text, '按 ENTER 繼續', faceimagepath, picture,
                         identifyfaces, identifyface['person']['name'])
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            personId = identifyface['person']['personId']
            name = identifyface['person']['name']
            confidence = identifyface['confidence']
            faceimage = ClassUtils.readFile(faceimagepath)

            config = ClassUtils.loadConfig()
            ClassDB.BaseDB.insert(personId, name, confidence, text, config['api_key'], config['personGroupId'], timestamp,
                                  faceimage)
