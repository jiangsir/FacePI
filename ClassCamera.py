import os, time, sys, json
import subprocess
import ClassMessageBox

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r') as f:
    config = json.load(f)

def takePicture(personGroupId, delay):
    cameras = config['camera'].split(',')
    for camera in cameras:
        if camera[0] == '*' and camera == '*webcam':
            return takePicture_fswebcam(personGroupId, delay)
        elif camera[0] == '*' and camera == '*CSIcamera':
            return takePicture_CSI(personGroupId, delay)
    return takePicture_CSI(personGroupId, delay)


def takePicture_CSI(personGroupId, delay):
    # delay in ms 3000ms = 3s
    jpgimagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(jpgimagepath)):
        os.makedirs(os.path.dirname(jpgimagepath))
    try:
        subprocess.call(['raspistill', '-t', str(delay), '-o', jpgimagepath])
    except OSError:
        ClassMessageBox.FaceAPIErrorGUI('def takePicture_CSI',
                                        'CSI 攝影機無法啟動！',
                                        'OSError: raspistill 無法執行或不存在！！')        
        #print('EXCEPTION: raspistill 無法執行或不存在！！', file=sys.stderr)
        jpgimagepath = None

    #os.system("raspistill -t " + str(delay) + " -o " + imagepath)
    return jpgimagepath


def takePicture_fswebcam(personGroupId, delay):
    jpgimagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
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