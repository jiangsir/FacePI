import os, json

def getBasepath():
    basepath = os.path.dirname(os.path.realpath(__file__))
    return basepath

def loadConfig():
    basepath = getBasepath()
    configpath = os.path.join(basepath, 'Config.json')
    with open(configpath, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def protectPersonName(name):
    return name[0] + '〇' + name[2:]


def protectPersonNameForTTS(name):
    return name[0] + '圈' + name[2:]


def getFaceImagepath(faceid):
    basepath = os.path.dirname(os.path.realpath(__file__))
    #detectedFaceImagepath = basepath + "/tmp/faceId_" + faceid + ".jpg"
    detectedFaceImagepath = os.path.join(basepath, 'tmp', "faceId_" + faceid + ".jpg")

    if not os.path.exists(os.path.dirname(detectedFaceImagepath)):
        os.makedirs(os.path.dirname(detectedFaceImagepath))
    return detectedFaceImagepath
