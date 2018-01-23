import FaceAPI, Camera, sys
from PIL import Image

api_key = "f3e388f66ee146d3b6e96f6ca2ac25d3"
host = "eastasia.api.cognitive.microsoft.com"
personGroupId = "junior"
title = "高師大附中 刷臉簽到系統"
PersonGroup = FaceAPI.PersonGroup(api_key, host)
personApi = FaceAPI.Person(api_key, host)

while True:
    print('0. 結束程式！')
    print('1. 列出所有的 PersonGroups')
    print('2. 列出某個「人群」裡有哪些 Person')
    print('3. 刪除某個 PersonGroups')
    print('4. 刪除某個 PersonGroups 裡的 Person')
    print('5. 鏡頭對焦')
    index = input('選擇功能？ ')
    if index == '0':
        sys.exit()
    elif index == '1':
        persongroups = PersonGroup.ListPersonGroups()
        print('總共有 ', len(persongroups), '個「人群」')
        for persongroup in persongroups:
            print('personGroupId=', persongroup)
    elif index == '2':
        persons = PersonGroup.list_persons_in_group(input('請輸入 personGroupId: '))
        if len(persons)==0:
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
