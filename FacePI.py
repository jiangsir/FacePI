import FaceAPI
import Camera
import sys
import os
import json

basepath = os.path.dirname(os.path.realpath(__file__))

#api_key = "f3e388f66ee146d3b6e96f6ca2ac25d3"
#host = "eastasia.api.cognitive.microsoft.com"
#personGroupId = "junior"
#title = "高師大附中 刷臉簽到系統"
with open(basepath + '/Config.json', 'r') as f:
    config = json.load(f)
print(config)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']
PersonGroup = FaceAPI.PersonGroup(api_key, host)
personApi = FaceAPI.Person(api_key, host)

while True:
    print('============================================')
    print('當前設定檔內容：')
    for key in config.keys():
        print(key+": ", config[key])
    print('0. 結束程式！')
    print('1. 列出所有的 PersonGroups')
    print('2. 列出某個「人群」裡有哪些 Person')
    print('3. 刪除某個 PersonGroups')
    print('4. 刪除某個 PersonGroups 裡的 Person')
    print('5. 鏡頭對焦')
    print('6. 列出所有的 facelists ')
    print('7. 觀察 PersonGroup status ')
    print('8. 訓練 PersonGroup ')
    print('9. 建立一個 PersonGroup ')
    print('10. 檢測 Config 設定。ApiKey ')
    index = input('選擇功能？ ')
    if index == '0':
        sys.exit()
    elif index == '1':
        persongroups = PersonGroup.ListPersonGroups()
        if 'error' in persongroups:
            print("讀取 PersonGroup 發生錯誤！: ", persongroups['error']['message'])
            continue
        print('總共有 ', len(persongroups), '個「人群」')
        for persongroup in persongroups:
            print('personGroupId=', persongroup)
    elif index == '2':
        persons = PersonGroup.list_persons_in_group(
            input('請輸入 personGroupId: '))
        if len(persons) == 0:
            print('本 personGroupId 內沒有任何一個 person')
        for person in persons:
            print('person:', person)
    elif index == '3':
        PersonGroup.deletePersonGroup(input('請輸入要刪除的 personGroupId:'))
    elif index == '4':
        persongroups = PersonGroup.ListPersonGroups()
        print('總共有 ', len(persongroups), '個「人群」')
        for persongroup in persongroups:
            print('personGroupId=', persongroup)
        personGroupId = input('請輸入 personGroupId: ')
        persons = PersonGroup.list_persons_in_group(personGroupId)
        for person in persons:
            print('person:', person)
        personid = input('請輸入 personid: ')
        personApi.deleteAPerson(personGroupId, personid)
    elif index == '5':
        Camera.takePicture('test camera', 10000)
    elif index == '6':
        faceList = FaceAPI.FaceList(api_key, host)
        faceList.listFacelists()
    elif index == '7':
        personGroupId = input('請輸入 personGroupId: ')
        PersonGroup.personGroup_status(personGroupId)
    elif index == '8':
        personGroupId = input('請輸入 personGroupId: ')
        PersonGroup.train_personGroup(personGroupId)
    elif index == '9':
        personGroupId = input('建立一個 personGroupId: ')
        PersonGroup.createPersonGroup(
            personGroupId, 'group namename', 'group datadata')
    elif index == '10':
        api_key = input('請輸入有效的 API KEY['+config['api_key']+']:')
        if api_key != '':
            config['api_key'] = api_key
        host = input("驗證主機["+config['host']+"]: ")
        if host != '':
            config['host'] = host
        #personGroupId = input("現有一個預設的 person: ")
        title = input("自訂標題["+config['title']+"]：")
        if title != '':
            config['title'] = title
        with open(basepath + '/Config.json', 'w') as outfile:
            json.dump(config, outfile, ensure_ascii=False)
