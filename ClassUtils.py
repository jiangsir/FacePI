import os, json, time
import MyException, ClassMessageBox
# from matplotlib.font_manager import FontProperties


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
    detectedFaceImagepath = os.path.join(basepath, 'tmp',
                                         "faceId_" + faceid + ".jpg")

    if not os.path.exists(os.path.dirname(detectedFaceImagepath)):
        os.makedirs(os.path.dirname(detectedFaceImagepath))
    return detectedFaceImagepath


def getTakePicturePath(personGroupId):
    basepath = getBasepath()
    jpgimagepath = os.path.join(
        basepath, 'takepictures', personGroupId + "_" +
        time.strftime("%Y%m%d_%H%M%S", time.localtime()) + ".jpg")
    return jpgimagepath


def makedirsPath(path):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))


def isFaceAPIError(faceapijson):
    if 'error' in faceapijson:
        if faceapijson['error']['code'] == 'RateLimitExceeded':
            raise MyException.RateLimitExceededError(
                faceapijson['error']['code'])
        elif faceapijson['error']['code'] == 'PersonGroupNotFound':
            raise MyException.PersonGroupNotFoundError(
                faceapijson['error']['code'])
        elif faceapijson['error']['code'] == 'Unspecified':
            raise MyException.UnspecifiedError(faceapijson['error']['code'])
        else:
            print('CODE:', faceapijson['error']['code'])
            print('MESSAGE:', faceapijson['error']['message'])
        return True
    return False


def SigninSuccess(person, faceid):
    #ClassGTTS.play_gTTS(person['name'], '簽到成功')
    text = person['name'], '簽到成功'
    print(person['name'], '簽到成功')
    print(person)
    print(getFaceImagepath(faceid))
    ClassMessageBox.SuccessGUI('簽到成功', text, getFaceImagepath(faceid))

def SigninSuccesses(successes):
    for success in successes:
        print(success['person']['name'], '簽到成功!')
    ClassMessageBox.SuccessesGUI(successes)
    
def getChineseFont():  
    pass
    #return FontProperties(fname='/System/Library/Fonts/PingFang.ttc',size=15)
