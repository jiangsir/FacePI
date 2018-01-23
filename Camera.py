import os, time

basepath = os.path.dirname(os.path.realpath(__file__))


def takePicture(personGroupId, delay):
    # delay in ms 3000ms = 3s
    imagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(imagepath)):
        os.makedirs(os.path.dirname(imagepath))
    os.system("raspistill -t "+delay+" -o " + imagepath)
    return imagepath
