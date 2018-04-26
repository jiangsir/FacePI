import sys, os, json, time
import ClassFaceAPI as FaceAPI
import ClassCamera as Camera
#import ClassGPIO


def train_image(personGroupId, personname, imagepath):
    print("訓練圖檔路徑:", imagepath)
    print("personname=", personname)
    personapi = FaceAPI.Person(api_key, host)
    person = personapi.getPersonByName(personGroupId, personname)
    print('getPersonByName: person=', person)
    personGroupapi = FaceAPI.PersonGroup(api_key, host)
    if person == None:
        print('call create_a_person')
        personid = personapi.create_a_person(personGroupId, personname,
                                             personname + ' 說明。')
        personapi.add_a_person_face(imagepath, personid, personGroupId)
    else:
        print('call add_a_person_face, personId=', person['personId'])
        personapi.add_a_person_face(imagepath, person['personId'],
                                    personGroupId)
    personGroupapi.train_personGroup(personGroupId)


options = {
    0: '結束程式',
    1: '進行 3 連拍',
    2: '列出所有的 PersonGroups',
    3: '列出「人群」裡有哪些 Person',
    4: '刪除某個 PersonGroups',
    5: '刪除某個 PersonGroups 裡的 Person',
    #6: '列出所有的 facelists',
    7: '觀察 PersonGroup status',
    8: '訓練 PersonGroup',
    9: '建立一個 PersonGroup',
    10: '列出 Config.json 設定。',
    11: '訓練 /traindatas 裡的圖檔',
    12: '搜尋 PersonGroup 裡的 personName',
    13: '設定繼電器',
}

if len(sys.argv) != 2:
    print("使用方式:", sys.argv[0], "<選項>")
    print("如:", sys.argv[0], "1")
    print("選項:")
    for key in sorted(options.keys()):
        print(str(key)+'.', options[key])
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

print('============================================')
# for key in config.keys():
#     print(key + ": ", config[key])

index = int(sys.argv[1])
print(str(index)+'.', options[index])
if index == 0:
    sys.exit()
elif index == 1:
    personname = input('進行 3 連拍，請輸入姓名：')
    for i in range(3):
        jpgimagepath = Camera.takePicture(personGroupId, 2000)
        train_image(personGroupId, personname, jpgimagepath)
elif index == 2:
    persongroups = PersonGroup.ListPersonGroups()
    if 'error' in persongroups:
        print("讀取 PersonGroup 發生錯誤！: ", persongroups['error']['message'])
    print('總共有 ', len(persongroups), '個「人群」')
    for persongroup in persongroups:
        print('personGroupId=' + persongroup['personGroupId'])
        print(persongroup)
elif index == 3:
    print('personGroupId = ' + personGroupId)
    persons = PersonGroup.list_persons_in_group(personGroupId)
    if len(persons) == 0:
        print('本 personGroupId 內沒有任何一個 person')
    for person in persons:
        print('name=' + person['name'] + ':', person)
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
        print('name='+person['name']+':', person)
    personid = input('請輸入將要刪除的 personid: ')
    personApi.deleteAPerson(personGroupId, personid)
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
    personGroupId = input('建立一個 personGroupId: ')
    PersonGroup.createPersonGroup(personGroupId, 'group namename',
                                  'group datadata')
elif index == 10:
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
    filelist = os.listdir(basepath + '/traindatas/')
    print('目前 traindatas/ 內的圖檔如下：')
    for file in filelist:
        time.sleep(10)
        personname = file.split('_')[0]
        train_image(personGroupId, personname,
                    os.path.join(basepath + '/traindatas/', file))
elif index == 12:
    personname = input('請輸入要找尋的 personname: ')
    persons = personApi.getPersonsByName(personGroupId, personname)
    for person in persons:
        print("person: ", person)
elif index == 13:
    #ClassGPIO.RelayExchange()
    print('')
else:
    print("使用方式:", sys.argv[0], "<選項>")
    print("如:", sys.argv[0], "1")
    print("選項:")
    for key in sorted(options.keys()):
        print(str(key)+'.', options[key])
    sys.exit(1)