import sys, os, json, time
from PIL import Image
import ClassFaceAPI as FaceAPI
import ClassCamera as Camera
import ClassGTTS
from pypinyin import lazy_pinyin


#import ClassGPIO


# 加入一個人的眾多圖片，但不訓練
def add_personimages(personGroupId, personname, imagepaths):
    print("personname=", personname, "圖檔:", imagepaths)
    personAPI = FaceAPI.Person(api_key, host)
    person = personAPI.getPersonByName(personGroupId, personname)
    if person == None:
        print('call create_a_person')
        personid = personAPI.create_a_person(personGroupId, personname,
                                             personname + ' 說明。')
        for imagepath in imagepaths:
            personAPI.add_a_person_face(imagepath, personid, personGroupId)
    else:
        print('call add_a_person_face, personId=', person['personId'])
        for imagepath in imagepaths:
            personAPI.add_a_person_face(imagepath, person['personId'],
                                        personGroupId)


# 加入一個人的眾多圖片，並訓練
def train_personimages(personGroupId, personname, imagepaths):
    add_personimages(personGroupId, personname, imagepaths)

    personGroupapi = FaceAPI.PersonGroup(api_key, host)
    personGroupapi.train_personGroup(personGroupId)


# 將整個 traindatas 的圖片全部送上去訓練
def train_traindatas(personGroupId):
    traindataPath = basepath + '/traindatas/'
    trainfiles = os.listdir(traindataPath)
    print('目前 traindatas/ 內的圖檔如下：')

    for personname in trainfiles:
        #print("file="+ os.path.join(traindataPath, trainfile))
        personpath = os.path.join(traindataPath, personname)
        if os.path.isdir(personpath):
            print("person name=", personname)
            personImagePaths = []
            for personImagePath in os.listdir(personpath):
                personImagePaths.append(
                    os.path.join(personpath, personImagePath))
            print(personGroupId, personname, personImagePaths)
            add_personimages(personGroupId, personname, personImagePaths)
            time.sleep(6)

    personGroupapi = FaceAPI.PersonGroup(api_key, host)
    personGroupapi.train_personGroup(personGroupId)


options = {
    0: '結束程式',
    1: '訓練新人 3 連拍',
    2: '列出所有的 PersonGroups',
    3: '列出「人群」裡有哪些 Person',
    4: '刪除某個 PersonGroups',
    5: '刪除某個 PersonGroups 裡的 Person',
    #6: '列出所有的 facelists',
    7: '觀察 PersonGroup status',
    8: '訓練 PersonGroup',
    9: '建立一個 PersonGroup',
    10: '列出 Config.json 設定。',
    11: '訓練 /traindatas 裡的圖檔，同時訓練一群事先準備好的人與照片',
    12: '搜尋 PersonGroup 裡的 personName',
    13: '設定繼電器',
    14: '用網路 URL 圖片進行辨識。',
    15: '三連拍建立圖片資料庫 trainsdata（不進行訓練）'
}

if len(sys.argv) != 2:
    print("使用方式:", sys.argv[0], "<選項>")
    print("如: python3 FacePI/" + sys.argv[0], "1")
    print("選項:")
    for key in sorted(options.keys()):
        print(str(key) + '.', options[key])
    sys.exit(0)

basepath = os.path.dirname(os.path.realpath(__file__))

#api_key = "f3e388f66ee146d3b6e96f6ca2ac25d3"
#host = "eastasia.api.cognitive.microsoft.com"
#personGroupId = "junior"
#title = "高師大附中 刷臉簽到系統"
with open(basepath + '/Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']
PersonGroup = FaceAPI.PersonGroup(api_key, host)
personApi = FaceAPI.Person(api_key, host)
faceApi = FaceAPI.Face(api_key, host)

print('============================================')
# for key in config.keys():
#     print(key + ": ", config[key])

index = int(sys.argv[1])
print(str(index) + '.', options[index])
if index == 0:
    sys.exit()
elif index == 1:
    personname = input('進行 3 連拍，請輸入要訓練的對象姓名：')
    traindatasPath = basepath + '/traindatas/'

    jpgimagepaths = []
    for i in range(3):
        jpgimagepath = Camera.takePicture(personGroupId, 2000)
        #time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
        jpgimagepaths.append(jpgimagepath)

    train_personimages(personGroupId, personname, jpgimagepaths)

elif index == 2:
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
elif index == 3:
    print('personGroupId = ' + personGroupId)
    persons = PersonGroup.list_persons_in_group(personGroupId)
    if len(persons) == 0:
        print('本 personGroupId 內沒有任何一個 person')
        sys.exit()
    for person in persons:
        print('name=' + person['name'] + ':', 'personId=' + person['personId'],
              'persistedFaceIds=', len(person['persistedFaceIds']))
elif index == 4:
    PersonGroup.deletePersonGroup(input('請輸入要刪除的 personGroupId:'))
elif index == 5:
    persongroups = PersonGroup.ListPersonGroups()
    print('總共有 ', len(persongroups), '個「人群」')
    for persongroup in persongroups:
        print('personGroupId=', persongroup)
    #personGroupId = input('請輸入 personGroupId: ')
    persons = PersonGroup.list_persons_in_group(personGroupId)
    for person in persons:
        print('name=' + person['name'] + ':', person)
    personid = input('請輸入將要刪除的 personid: ')
    personApi.deletePerson(personGroupId, personid)
# elif index == 6:
#     faceList = FaceAPI.FaceList(api_key, host)
#     faceList.listFacelists()
elif index == 7:
    print('personGroupId = ' + personGroupId)
    PersonGroup.personGroup_status(personGroupId)
elif index == 8:
    print('personGroupId = ' + personGroupId)
    PersonGroup.train_personGroup(personGroupId)
elif index == 9:
    print('建立一個 personGroup')
    # 直接用中文建立：
    # 安裝套件：pip install pypinyin
    #personGroupId = input('請輸入 personGroupId(必須小寫字母與 - _): ')
    personGroupName = input('請輸入 personGroup name(可用中文): ')
    personGroupId = '_'.join(lazy_pinyin(personGroupName))

    PersonGroup.createPersonGroup(personGroupId, personGroupName,
                                  'group userdata')
elif index == 10:
    print(config)
    api_key = input('請輸入有效的 API KEY[' + config['api_key'] + ']:')
    if api_key != '':
        config['api_key'] = api_key
    host = input("驗證主機[" + config['host'] + "]: ")
    if host != '':
        config['host'] = host
    #personGroupId = input("現有一個預設的 person: ")
    title = input("自訂標題[" + config['title'] + "]：")
    if title != '':
        config['title'] = title
    with open(basepath + '/Config.json', 'w') as outfile:
        json.dump(config, outfile, ensure_ascii=False)
elif index == 11:
    train_traindatas(personGroupId)
elif index == 12:
    personname = input('請輸入要找尋的 personname: ')
    persons = personApi.getPersonsByName(personGroupId, personname)
    for person in persons:
        print("person: ", person)
elif index == 13:
    #ClassGPIO.RelayExchange()
    print('call ClassGPIO.RelayExchange()')
elif index == 14:
    imageurl = input('請輸入準備要辨識的 image URL or 檔案路徑:')
    if imageurl.startswith('http'):
        imageurls = []
        imageurls.append(imageurl)
        detectfaces = faceApi.detectURLImages(imageurls)
    else:
        imageurl = imageurl.strip()
        statinfo = os.stat(imageurl)
        print('檔案大小：', statinfo.st_size, 'Bytes')
        if statinfo.st_size < 1024:
            print('圖檔太小 不可小於 1KB')
            sys.exit(1)
        elif statinfo.st_size > 4 * 1024 * 1024:
            print('圖檔太大 不可大於 4MB')
            im = Image.open(imageurl)
            out = im.resize((128, 128))
            im.save(imageurl, "JPEG")
            print('out=', type(out))
        detectfaces = faceApi.detectLocalImage(imageurl)

    if len(detectfaces) == 0:
        print('相片中找不到人！')
        sys.exit(1)

    faceids = []
    for face in detectfaces:
        print('所偵測到的 faceId=', face['faceId'])
        faceids.append(face['faceId'])

    identifyfaces = faceApi.identify(faceids[:10], personGroupId)
    print('在所提供的相片中偵測到 identifyfaces 共 ', len(identifyfaces), '個',
          identifyfaces)
    for identifyface in identifyfaces:
        # print('candidateface 的[\'candidates\'] 其中有 ',
        #       len(candidateface['candidates']), '個在辨認資料庫內')
        for candidate in identifyface['candidates']:
            personId = candidate["personId"]
            confidence = candidate["confidence"]
            # print('辨認候選人 candidate: personId=', personId, confidence,
            #       candidate)
            person = personApi.get_a_person(personId, personGroupId)
            print(person['name'],
                  '簽到成功（' + str(confidence) + '）！', person['personId'],
                  len(person['persistedFaceIds']), '個 faceid')
            ClassGTTS.play_gTTS(person['name']+'簽到成功')

elif index == 15:
    personname = input('進行 3 連拍，請輸入姓名(儲存不訓練)：')
    # 建檔先暫放 /tmp 以免更新程式被清除。
    traindatasPath = '~/traindatas/' + personname + "/"
    if not os.path.exists(os.path.dirname(traindatasPath)):
        os.makedirs(os.path.dirname(traindatasPath))

    jpgimagepaths = []
    for i in range(3):
        jpgimagepath = Camera.takePicture(personGroupId, 2000)
        index = jpgimagepath.rfind('/')
        os.rename(jpgimagepath, traindatasPath + jpgimagepath[index:])
        #time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime()) + ".jpg"
        # jpgimagepaths.append(jpgimagepath)

else:
    print("使用方式:", sys.argv[0], "<選項>")
    print("如: python3 FacePI/" + sys.argv[0], "1")
    print("選項:")
    for key in sorted(options.keys()):
        print(str(key) + '.', options[key])
    sys.exit(1)