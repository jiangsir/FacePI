import os, time, sys, json, platform
import subprocess
import ClassUtils, MyException, ClassCV
from PIL import Image, ImageDraw, ImageFont, ImageTk
import ClassFaceAPI as FaceAPI

# basepath = os.path.dirname(os.path.realpath(__file__))
# with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
#     config = json.load(f)
basepath = ClassUtils.getBasepath()
config = ClassUtils.loadConfig()


api_key = config['api_key']
host = config['host']
personGroupId = config['personGroupId']
 
def takePicture(personGroupId, delay, type='Identify', size='small'):
    sysstr = platform.system()
    print('os=', sysstr, platform.release())

    if ClassUtils.isLinux():
        return takePicture_CSI(personGroupId, delay, size)
    else:
        return takePicture_opencv(personGroupId, delay, type)

    # cameras = config['camera'].split(',')
    # for camera in cameras:
    #     if camera == '*opencv':
    #         return takePicture_opencv(personGroupId, delay, type)
    #     elif camera == '*CSIcamera':
    #         return takePicture_CSI(personGroupId, delay, size)
    # return takePicture_CSI(personGroupId, delay, size)


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


# def cv_Success(successes):
#     ''' 運用 cv2 技術顯示的 Success '''
#     import cv2
#     import numpy as np
#     print('successes=', successes)
#     if len(successes) == 0:
#         cv_ImageText('無人簽到成功', '請按「ENTER」繼續')
#         return
#     for success in successes:
#         # print(success['person']['name'], '簽到成功!')
#         faceimagepath = ClassUtils.getFaceImagepath(success['faceId'])

#         cv_ImageText(
#             ClassUtils.protectPersonName(success['person']['name']) + '簽到成功!',
#             '按 ENTER 繼續')


def takePicture_opencv(personGroupId, delay, typee):
    if (ClassUtils.isWindows() or ClassUtils.isDarwin()):
        picturepath = ClassCV.show_opencv(typee, mirror=True)
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