import os, time, sys
import subprocess

basepath = os.path.dirname(os.path.realpath(__file__))


def takePicture(personGroupId, delay):
    # delay in ms 3000ms = 3s
    imagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(imagepath)):
        os.makedirs(os.path.dirname(imagepath))
    try:
        subprocess.call(['raspistill', '-t', str(delay), '-o', imagepath])
    except OSError:
        print('EXCEPTION: raspistill 無法執行或不存在！！', file=sys.stderr)
        imagepath = None

    #os.system("raspistill -t " + str(delay) + " -o " + imagepath)
    return imagepath

def takePicture_WebCam():
    return "webcam"