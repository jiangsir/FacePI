#!/usr/bin/env python

import sys, os, json, time, fire
from PIL import Image
import ClassFaceAPI as FaceAPI
import ClassCamera as Camera
import ClassUtils as Utils
from pypinyin import lazy_pinyin
import MyException, ClassTK, ClassCV

basepath = os.path.dirname(os.path.realpath(__file__))
config = Utils.loadConfig()
personGroupId = config['personGroupId']
api_key = config['api_key']
host = config['host']


class FacePI:
    ''' FacePI 文字介面
    搭配參數如下：
    createGroup: 建立一個 PersonGroup
    deleteGroup: 刪除一個 PersonGroup
    deletePerson: 刪除 PersonGroup 裡的一個 Person
    listGroups: 列出所有的 PersonGroups
    listPersons: 列出「人群」裡有哪些 Person
    relay: 設定繼電器,
    status: 觀察 PersonGroup status
    search: 搜尋一個personName,
    traindatas: '訓練 /traindatas 裡的圖檔，同時訓練一群事先準備好的人與照片',

    Config: 列出 Config.json 設定。
    Signin: 進行簽到！
    Identify: 用網路 URL 或本地圖片進行辨識。,
    Train: 用 3 連拍訓練一個新人
    '''

    # def __add_personimages(self, personGroupId, personname, userData,
    #                        imagepaths):
    #     ''' # 加入一個人的一張或多張圖片，但不訓練 '''
    #     print("personname=", personname, "圖檔:", imagepaths)
    #     personAPI = FaceAPI.Person(api_key, host)
    #     person = personAPI.getPersonByName(personGroupId, personname)
    #     if person == None:
    #         print('call create_a_person')
    #         personid = personAPI.create_a_person(personGroupId, personname,
    #                                              userData)
    #         for imagepath in imagepaths:
    #             personAPI.add_a_person_face(imagepath, personid, personGroupId)
    #     else:
    #         print('call add_a_person_face, personId=', person['personId'])
    #         for imagepath in imagepaths:
    #             personAPI.add_a_person_face(imagepath, person['personId'],
    #                                         personGroupId)

    # 將整個 traindatas 的圖片全部送上去訓練
    def traindatas(self, traindatasPath):
        ''' 請輸入 traindatasPath 的絕對路徑。
        請提供資料路徑如： /xxx/xxx/traindatas/
        該路徑內的資料夾結構必須為 [userData/姓名/xxxx.jpg]
        '''
        #traindataPath = basepath + '/traindatas/'
        #traindataPath = os.path.join(basepath, 'traindatas')
        Utils.makedirsPath(traindatasPath)
        train_userDataPaths = os.listdir(traindatasPath)
        print('目前 traindatas/ 內的圖檔如下：')

        for userDataPath in train_userDataPaths:
            userDataPath = os.path.join(traindatasPath, userDataPath)
            if os.path.basename(userDataPath).startswith('.') or os.path.isdir(
                    userDataPath) == False:
                print(userDataPath)
                print('continue')
                continue

            for personnamePath in os.listdir(userDataPath):
                #print("file="+ os.path.join(traindataPath, trainfile))
                personname = os.path.basename(personnamePath)
                personpath = os.path.join(traindatasPath, userDataPath,
                                          personname)
                if os.path.isdir(personpath):
                    print("person name=", personname)
                    personImagePaths = []
                    for personImagePath in os.listdir(personpath):
                        personImagePaths.append(
                            os.path.join(personpath, personImagePath))
                    print(personGroupId, personname, personImagePaths)

                    personAPI = FaceAPI.Person(api_key, host)
                    personAPI.add_personimages(personGroupId, personname,
                                               os.path.basename(userDataPath),
                                               personImagePaths)
                    #time.sleep(6)

        personGroupapi = FaceAPI.PersonGroup(api_key, host)
        personGroupapi.train_personGroup(personGroupId)

    def listGroups(self):
        ''' 2: '列出所有的 PersonGroups' '''
        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        persongroups = PersonGroup.ListPersonGroups()
        if persongroups == None:
            print("讀取 PersonGroup 發生錯誤！: ", persongroups)
            sys.exit()
        if 'error' in persongroups:
            print("讀取 PersonGroup 發生錯誤！: ", persongroups['error']['message'])
            sys.exit()
        print('總共有 ', len(persongroups), '個「人群」')
        for persongroup in persongroups:
            print('personGroupId=' + persongroup['personGroupId'])
            print(persongroup)

    def listPersons(self, personGroupId=personGroupId):
        ''' 3: 列出「人群」裡有哪些 Person '''
        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        try:
            persons = PersonGroup.list_persons_in_group(personGroupId)
            if len(persons) == 0:
                print('本 personGroup(' + personGroupId + ') 內沒有任何一個 person')
                sys.exit()
            for person in persons:
                s = 'name=' + person['name'] + '(' + person['userData'] + '):'
                try:
                    print(s, 'personId=' + person['personId'],
                          'persistedFaceIds=', len(person['persistedFaceIds']))
                except UnicodeEncodeError as e:
                    print('name=姓名編碼有誤！', 'personId=' + person['personId'],
                          'persistedFaceIds=', len(person['persistedFaceIds']))
        except MyException.responseError as e:
            print(e.message)

    def deleteGroup(self):
        ''' 4: '刪除某個 PersonGroups','''
        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        PersonGroup.deletePersonGroup(input('請輸入要刪除的 personGroupId:'))

    def deletePerson(self, personid):
        ''' 5: 給定一個 personId 刪除一個 Person '''
        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        personApi = FaceAPI.Person(api_key, host)

        # persons = PersonGroup.list_persons_in_group(personGroupId)
        # for person in persons:
        #     print('name=' + person['name'] + ':', person)
        personApi.deletePerson(personGroupId, personid)
        PersonGroup.train_personGroup(personGroupId)

    def status(self, personGroupId=personGroupId):
        ''' 7: 觀察 PersonGroup status '''
        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        status = PersonGroup.personGroup_status(personGroupId)
        print('PersonGroup(' + personGroupId + ')狀態:', status['status'])
        print(status)

    def trainGroup(self, personGroupId=personGroupId):
        ''' 8: 訓練 PersonGroup '''
        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        PersonGroup.train_personGroup(personGroupId)

    def createGroup(self, personGroupName):
        ''' 9: 建立一個 PersonGroup, 請給定一個名稱 _英數字 '''
        # personGroupName = input('請輸入 personGroup name(可用中文): ')
        personGroupId = '_'.join(lazy_pinyin(personGroupName))

        PersonGroup = FaceAPI.PersonGroup(api_key, host)
        PersonGroup.createPersonGroup(personGroupId, personGroupName,
                                      'group userdata')

    def Config(self):
        ''' 10: 列出 Config.json 設定。 '''
        api_key = input('請輸入有效的 API KEY[' + config['api_key'] + ']:')
        if api_key != '':
            config['api_key'] = api_key
        host = input("驗證主機[" + config['host'] + "]: ")
        if host != '':
            config['host'] = host
        title = input("自訂標題[" + config['title'] + "]：")
        if title != '':
            config['title'] = title
        personGroupId = input(
            "預設 personGroupId(必須為小寫字母及-_) [" + config['personGroupId'] + "]：")
        if personGroupId != '':
            config['personGroupId'] = personGroupId
        confidence = input("預設信心指數 [" + str(config['confidence']) + "]：")
        if confidence != '':
            config['confidence'] = float(confidence)
        landmark = input("臉部特徵 [" + str(config['landmark']) + "]：")
        if landmark != '':
            config['landmark'] = int(landmark)

        with open(basepath + '/Config.json', 'w', encoding='utf-8') as outfile:
            json.dump(config, outfile, ensure_ascii=False)

    def setAPIKEY(self, api_key):
        ''' 快速設定 API_KEY '''
        config['api_key'] = api_key
        with open(basepath + '/Config.json', 'w', encoding='utf-8') as outfile:
            json.dump(config, outfile, ensure_ascii=False)

    def search(self, personname):
        ''' 12: 搜尋 PersonGroup 裡的 personName '''
        #personname = input('請輸入要找尋的 personname: ')
        personApi = FaceAPI.Person(api_key, host)
        persons = personApi.getPersonsByName(personGroupId, personname)
        for person in persons:
            try:
                print("person: ", person)
            except UnicodeEncodeError as e:
                print("person=", '此人姓名編碼錯誤，無法顯示', e)

    def relay(self):
        ''' 13: '設定繼電器 '''
        #ClassGPIO.RelayExchange()
        print('call ClassGPIO.RelayExchange()')

    def Identify(self, pictureurl):
        ''' 14: 進行「辨識」，使用 image URL or 檔案路徑 '''
        start = int(round(time.time() * 1000))
        print('開始計時 identify')
        faceApi = FaceAPI.Face(api_key, host)
        personApi = FaceAPI.Person(api_key, host)
        print('載入 class', int(round(time.time() * 1000) - start), 'ms')
        #imageurl = input('請輸入準備要辨識的 image URL or 檔案路徑:')
        if pictureurl.startswith('http'):
            detectfaces = faceApi.detectURLImages(pictureurl)
        else:
            pictureurl = pictureurl.strip()
            statinfo = os.stat(pictureurl)
            print('檔案大小：', statinfo.st_size, 'Bytes')
            if statinfo.st_size < 1024:
                print('圖檔太小 不可小於 1KB')
                sys.exit(1)
            elif statinfo.st_size > 4 * 1024 * 1024:
                print('圖檔太大 不可大於 4MB')
                im = Image.open(pictureurl)
                out = im.resize((128, 128))
                im.save(pictureurl, "JPEG")
                print('out=', type(out))
            detectfaces = faceApi.detectLocalImage(pictureurl)

        # if len(detectfaces) == 0:
        #     print('相片中找不到人！')
        #     sys.exit(1)

        faceids = []
        for detectface in detectfaces:
            print('所偵測到的 faceId=', detectface['faceId'])
            faceids.append(detectface['faceId'])

        print('Identify.detectfaces=', detectfaces)

        try:
            identifiedfaces = faceApi.identify(faceids[:10], personGroupId)
            print('在所提供的相片中偵測到 identifyfaces 共 ', len(identifiedfaces), '個')
        except MyException.PersonGroupNotTrainedError as e:
            print('接到例外！MyException.PersonGroupNotTrainedError as e')
            print('Identify.detectedFaces=', detectfaces)
            ClassCV.cv_Identifyfaces(detectfaces, pictureurl)
            #ClassTK.tk_UnknownPerson('texttest....', pictureurl, pictureurl)

            return
        print('在所提供的相片中偵測到 identifyfaces 共 ', len(identifiedfaces), '個')

        # successes = []
        for identifiedface in identifiedfaces:
            for candidate in identifiedface['candidates']:
                personId = candidate["personId"]
                person = personApi.get_a_person(personId, personGroupId)
                identifiedface['person'] = person
                identifiedface['confidence'] = candidate["confidence"]
                identifiedface['personId'] = candidate["personId"]

        Utils.SigninIdentifyfaces(identifiedfaces, pictureurl)

    def buildTraindatas(self, personname):
        ''' 15: '快速 3 連拍建立圖片資料庫不進行訓練） '''
        personname = input('進行 3 連拍，請輸入姓名(儲存不訓練)：')

        #traindatasPath = '~/traindatas/' + personname + "/"
        home = os.path.expanduser("~")
        traindatasPath = os.path.join(home, 'traindatas', personname)

        if not os.path.exists(os.path.dirname(traindatasPath)):
            os.makedirs(os.path.dirname(traindatasPath))

        jpgimagepaths = []
        for i in range(3):
            jpgimagepath = Camera.takePicture(
                personGroupId, 2000, size='large')
            #index = jpgimagepath.rfind('/')
            filename = os.path.basename(jpgimagepath)
            os.rename(jpgimagepath, traindatasPath + filename)
            #time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
            # jpgimagepaths.append(jpgimagepath)

    def Train(self, userData, personname):
        ''' 1. 用 3 連拍訓練一個新人 '''
        #personname = input('進行 3 連拍，請輸入要訓練的對象姓名：')
        #traindatasPath = basepath + '/traindatas/'
        #traindatasPath = os.path.join(basepath, 'traindatas')
        jpgimagepaths = []
        for i in range(3):
            jpgimagepath = Camera.takePicture(
                personGroupId, 2000, 'Train', size='large')
            #time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
            #filename = jpgimagepath[jpgimagepath.rfind('/'):]
            filename = os.path.basename(jpgimagepath)

            #jpgtraindata = '/home/pi/traindatas/' + personname + filename
            home = os.path.expanduser("~")
            jpgtraindata = os.path.join(home, 'traindatas', userData,
                                        personname, filename)

            if not os.path.exists(os.path.dirname(jpgtraindata)):
                os.makedirs(os.path.dirname(jpgtraindata))
            os.rename(jpgimagepath, jpgtraindata)
            jpgimagepaths.append(jpgtraindata)

        personAPI = FaceAPI.Person(api_key, host)
        personAPI.add_personimages(personGroupId, personname, userData,
                                   jpgimagepaths)
        personGroupapi = FaceAPI.PersonGroup(api_key, host)
        personGroupapi.train_personGroup(personGroupId)

    def Signin(self):
        ''' 簽到！ '''
        while True:
            jpgimagepath = Camera.takePicture(personGroupId, 2000)
            self.Identify(jpgimagepath)


if __name__ == '__main__':
    fire.Fire(FacePI)
