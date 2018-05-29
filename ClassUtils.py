import os, json, time, platform
import MyException


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
                                         "faceId_" + faceid + ".png")

    if not os.path.exists(os.path.dirname(detectedFaceImagepath)):
        os.makedirs(os.path.dirname(detectedFaceImagepath))
    return detectedFaceImagepath


def getTakePicturePath(personGroupId):
    ''' 取得拍照後要存檔的路徑。 ''' 
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


# def SigninSuccess(person, faceid):
#     #ClassGTTS.play_gTTS(person['name'], '簽到成功')
#     text = person['name'], '簽到成功'
#     print(person['name'], '簽到成功')
#     print(person)
#     print(getFaceImagepath(faceid))
#     ClassMessageBox.SuccessGUI('簽到成功', text, getFaceImagepath(faceid))


def SigninSuccesses(successes):
    if isLinux():
        if len(successes)==0:
            print('沒有人簽到')
            return

        for success in successes:
            name = protectPersonName(success['person']['name'])
            if isDarwin():
                #import ClassGTTS
                #ClassGTTS.play_gTTS(name, '簽到成功!')
                print(name, '簽到成功!')
            else:
                print(name, '簽到成功!')
    elif isWindows() or isDarwin():
        import ClassCamera
        #ClassMessageBox.SuccessesGUI(successes)
        ClassCamera.cv_Success(successes)

def SigninIdentifyfaces(identifyfaces):
    if isLinux():
        if len(identifyfaces)==0:
            print('照片裡沒有人！')
            return

        for identifyface in identifyfaces:
            if 'person' in identifyface:
                name = protectPersonName(identifyface['person']['name'])
                print(name, '簽到成功!')
            else:
                print('你哪位？', identifyface)
    elif isWindows() or isDarwin():
        import ClassCamera
        ClassCamera.cv_Identifyfaces(identifyfaces)

def isLinux():
    return 'Linux' == platform.system()

def isDarwin():
    return 'Darwin' == platform.system()

def isWindows():
    return 'Windows' == platform.system()
