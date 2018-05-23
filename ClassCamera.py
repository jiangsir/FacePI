import os, time, sys, json, platform, cv2
import subprocess
import ClassMessageBox, ClassUtils

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)


def takePicture(personGroupId, delay, size='small'):
    cameras = config['camera'].split(',')
    for camera in cameras:
        if camera[0] == '*' and camera == '*webcam':
            return takePicture_webcam(personGroupId, delay)
        elif camera[0] == '*' and camera == '*CSIcamera':
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
        ClassMessageBox.FaceAPIErrorGUI('def takePicture_CSI', 'CSI 攝影機無法啟動！',
                                        'OSError: raspistill 無法執行或不存在！！')
        #print('EXCEPTION: raspistill 無法執行或不存在！！', file=sys.stderr)
        #jpgimagepath = None

    #os.system("raspistill -t " + str(delay) + " -o " + imagepath)
    return jpgimagepath


def show_webcam(imagepath, mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)

        # font                   = cv2.FONT_HERSHEY_SIMPLEX
        # bottomLeftCornerOfText = (10,10)
        # fontScale              = 5
        # fontColor              = (255,255,255)
        # lineType               = 2
        # cv2.putText(img,'Hello World!', 
        # bottomLeftCornerOfText, 
        # font, 
        # fontScale,
        # fontColor,
        # lineType)

        cv2.putText(img,config['title'],(50,150),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),25)
        cv2.imshow(config['title'], img)

        key = cv2.waitKey(1)
        if key == ord(' '):
            cv2.imwrite(imagepath, img)
            break
        elif key == 27:  # esc to quit
            break
    cv2.destroyAllWindows()
    cv2.VideoCapture(0).release()


def takePicture_webcam(personGroupId, delay):
    sysstr = platform.system()
    print('os=', sysstr)
    if (sysstr == "Windows" or sysstr == "Darwin"):
        # jpgimagepath = os.path.join(basepath, 'takepictures', personGroupId + "_" + time.strftime(
        #     "%Y%m%d_%H%M%S", time.localtime()) + ".jpg")
        jpgimagepath = ClassUtils.getTakePicturePath(personGroupId)
        
        show_webcam(jpgimagepath, mirror=True)
        return jpgimagepath
    else:
        # jpgimagepath = os.path.join(basepath, 'takepictures', personGroupId + "_" + time.strftime(
        #     "%Y%m%d_%H%M%S", time.localtime()) + ".jpg")
        jpgimagepath = ClassUtils.getTakePicturePath(personGroupId)

        if not os.path.exists(os.path.dirname(jpgimagepath)):
            os.makedirs(os.path.dirname(jpgimagepath))
        try:
            subprocess.call(['fswebcam', "--no-banner", jpgimagepath])
        except OSError:
            ClassMessageBox.FaceAPIErrorGUI('def takePicture_fswebcam',
                                            'web cam 無法啟動！',
                                            'OSError: fswebcam 無法執行或不存在！！')
            #print('EXCEPTION: fswebcam 無法執行或不存在！！', file=sys.stderr)
            jpgimagepath = None
        return jpgimagepath


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