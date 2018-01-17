import os, time

basepath = os.path.dirname(os.path.realpath(__file__))


def takePicture(personGroupId):
    imagepath = basepath + "/takepictures/Identity_" + personGroupId + "_" + time.strftime(
        "%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
    if not os.path.exists(os.path.dirname(imagepath)):
        os.makedirs(os.path.dirname(imagepath))
    os.system("raspistill -t 3000 -o " + imagepath)
    return imagepath
