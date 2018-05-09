import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import os, sys
from PIL import Image
import ClassMessageBox

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r') as f:
    config = json.load(f)


class PersonGroup:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host
        # '''
        # basepath = os.path.dirname(os.path.realpath(__file__))
        # with open(basepath + '/FacePI-Config.json', 'r') as f:
        #     config = json.load(f)
        # self.api_key = config["api_key"]
        # self.host = config["host"]
        # self.personGroupId = config['personGroupId']
        # '''

    def list_persons_in_group(self, personGroupId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            #'start': '{string}',
            #'top': '1000',
        })

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                         "/persons?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            # print('persons=', str(data, 'UTF-8'))
            persons = json.loads(str(data, 'UTF-8'))
            conn.close()
            return persons
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def ListPersonGroups(self):
        #print('列出所有的 person Groups')
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            #'start': '{string}',
            'top': '1000',
        })

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups?%s" % params,
                         "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            personGroups = json.loads(str(data, 'UTF-8'))
            conn.close()
            #print('共', len(personGroups), '個 =', personGroups)
            return personGroups
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def getPersonGroup(self, personGroupId):
        print('搜尋 personGroupid =', personGroupId)
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "GET",
                "/face/v1.0/persongroups/" + personGroupId + "?%s" % params,
                "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            personGroup = json.loads(str(data, 'UTF-8'))
            conn.close()
            print(personGroup)
            return personGroup
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def createPersonGroup(self, personGroupId, groupname, groupdata):
        print("createPersonGroup: 建立一個 personGroupid = " + personGroupId)
        headers = {
            # Request headers.
            'Content-Type': 'application/json',

            # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        # Replace 'examplegroupid' with an ID you haven't used for creating a group before.
        # The valid characters for the ID include numbers, English letters in lower case, '-' and '_'.
        # The maximum length of the ID is 64.
        #personGroupId = 'examplegroupid'
        #personGroupId = 'jiangsir_groupid2'

        # The userData field is optional. The size limit for it is 16KB.
        #personGroupId = personGroupId.encode(encoding='utf-8')
        #params = urllib.parse.urlencode(personGroupId)
        body = "{ 'name':'" + groupname + "', 'userData':'" + groupdata + "' }"

        try:
            # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
            #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
            #   URL below with "westus".
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "PUT",
                "/face/v1.0/persongroups/{}".format(personGroupId),
                body.encode(encoding='utf-8'),
                headers)
            response = conn.getresponse()

            # 'OK' indicates success. 'Conflict' means a group with this ID already exists.
            # If you get 'Conflict', change the value of personGroupId above and try again.
            # If you get 'Access Denied', verify the validity of the subscription key above and try again.
            print(response.reason)

            conn.close()
            return personGroupId
        except Exception as e:
            print(e.args)

    def train_personGroup(self, personGroupId):
        print("train_personGroup: 開始訓練一個 personGroup personGroupId=" +
              personGroupId + "。")

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({'personGroupId': personGroupId})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/persongroups/" + personGroupId +
                         "/train?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def personGroup_status(self, personGroupId):
        print("personGroup_status: 查看一個 personGroup 的狀態，也就是看看訓練是否成功！")
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({'personGroupId': personGroupId})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                         "/training?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            status = json.loads(str(data, 'UTF-8'))
            conn.close()
            print('status=', status)
            if 'error' in status:
                ClassMessageBox.FaceAPIErrorGUI('def personGroup_status',
                                                status['error']['code'],
                                                status['error']['message'])
                return []
            return status
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def deletePersonGroup(self, personGroupId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "DELETE",
                "/face/v1.0/persongroups/" + personGroupId + "?%s" % params,
                "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


class Person:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host

    def add_a_person_face(self, imagepath, personId, personGroupId):
        print("'add_a_person_face': 用一個圖片放入一個 person 當中 personId=" + personId,
              'imagepath=', imagepath)
        #display(Image(url=imagepath))

        headers = {
            # Request headers
            #        'Content-Type': 'application/json',
            'Content-Type': 'application/octet-stream',  #上傳圖檔
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'personGroupId': personGroupId,
            #'personId': '03cb1134-ad35-4b80-8bf2-3200f44eef31',
            'personId': personId,
            #'userData': '{string}',
            #'targetFace': '{string}',
        })
        #"https://lh3.googleusercontent.com/AuJtzSdWCTZ6pWW9pMxec86gVZEjP00O7qvl8RNbzYfmJvsiUfDL-BXfel5Sw2jgPNUy7rcIVQ-HFDxDEFuIZxp56NpKwOjYncgMjL_dt0-FnoBIYyUpplx4LlE5ShN2hJ3-URLwOA4=w597-h796-no"

        #    requestbody = '{"url": "'+imageurl+'"}'
        requestbody = open(imagepath, "rb").read()

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request(
                "POST", "/face/v1.0/persongroups/" + personGroupId +
                "/persons/" + personId + "/persistedFaces?%s" % params,
                requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            jsondata = json.loads(str(data, 'UTF-8'))
            conn.close()
            if 'error' in jsondata.keys():
                print("EXCEPTION: 這個圖片中沒有偵測到臉部。:",
                      jsondata['error']['message'])
            # if 'error' in jsondata:
            #     ClassMessageBox.FaceAPIErrorGUI(
            #         'def add_a_person_face',
            #         '這個圖片中沒有偵測到臉部。' + jsondata['error']['code'],
            #         jsondata['error']['message'])
            #     return []

        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def create_a_person(self, personGroupId, name, descript):
        print("'create_a_person': 在 personGroupid=" + personGroupId +
              " 裡 建立一個 person name=" + name)
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({'personGroupId': personGroupId})
        requestbody = '{"name":"' + name + '","userData":"' + descript + '"}'

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/persongroups/" +
                         personGroupId + "/persons?%s" % params,
                         requestbody.encode('UTF-8'), headers)
            response = conn.getresponse()
            data = response.read()
            create_a_person_json = json.loads(str(data, 'UTF-8'))
            conn.close()
            if 'error' in create_a_person_json:
                print(data)
                ClassMessageBox.FaceAPIErrorGUI(
                    'def create_a_person',
                    create_a_person_json['error']['code'],
                    create_a_person_json['error']['message'])
                return []

            return create_a_person_json['personId']
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def list_persons_in_group(self, personGroupId):
        print("'list_persons_in_group'")
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            #'start': '{string}',
            #'top': '1000',
        })

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                         "/persons?%s" % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            #print(data)
            persons = json.loads(str(data, 'UTF-8'))
            conn.close()
            if 'error' in persons:
                ClassMessageBox.FaceAPIErrorGUI('def list_persons_in_group',
                                                persons['error']['code'],
                                                persons['error']['message'])
                return []

            return persons
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def deletePerson(self, personGroupId, personId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("DELETE", "/face/v1.0/persongroups/" + personGroupId +
                         "/persons/" + personId + "?%s" % params, "{body}",
                         headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def get_a_person(self, personId, personGroupId):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                         "/persons/" + personId + "?%s" % params, "{body}",
                         headers)
            response = conn.getresponse()
            data = response.read()
            personjson = json.loads(str(data, 'UTF-8'))
            conn.close()
            print("get_a_person = " + str(personjson))
            return personjson
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def getPersonByName(self, personGroupId, personname):
        persons = self.list_persons_in_group(personGroupId)
        thisperson = None
        for person in persons:
            if person['name'] == personname:
                thisperson = person
                break
        return thisperson

    # 找出所有 指定 personname 的 person. personname 是可以重複的。
    def getPersonsByName(self, personGroupId, personname):
        persons = self.list_persons_in_group(personGroupId)
        returnpersons = []
        for person in persons:
            if person['name'] == personname:
                returnpersons.append(person)
        return returnpersons


class Face:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host

    def identify(self, faceidkeys, personGroupId):
        print("def Face.identify 開始辨識。faceidkeys=", faceidkeys)
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        requestbody = '''{
            "personGroupId": "''' + personGroupId + '''",
            "faceIds":''' + str(faceidkeys) + ''',
            "maxNumOfCandidatesReturned":1,
            "confidenceThreshold": '''+str(config['confidence'])+'''
        }'''
        print('requestbody=', requestbody)
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/identify?%s" % params,
                         requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            #print(data)
            identifyfaces = json.loads(str(data, 'UTF-8'))
            #print(facejson)
            conn.close()
            # if 'error' in facejson:
            #     ClassMessageBox.FaceAPIErrorGUI('def identify',
            #                                     facejson['error']['code'],
            #                                     facejson['error']['message'])
            #     return []

            return identifyfaces
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            sys.exit()

    # 用網路上的圖片進行偵測。
    def detectURLImages(self, imageurls):
        headers = {
            # Request headers
            'Content-Type': 'application/json',  # 
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId':
            'true',
            'returnFaceLandmarks':
            'false',
            'returnFaceAttributes':
            'age,gender,emotion'
        })
        #'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure'
        print('imageurls=', imageurls)
        requestbody = '{"url": "' + imageurls[0] + '"}'
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody,
                         headers)
            response = conn.getresponse()
            data = response.read()
            detectfaces = json.loads(str(data, 'UTF-8'))
            print("detecURLImage.faces 偵測到 faces 長度=", len(detectfaces))
            for index, face in enumerate(detectfaces):
                print('face[' + str(index) + ']=', face)
            conn.close()
            if 'error' in detectfaces:
                ClassMessageBox.FaceAPIErrorGUI(
                    'def detectURLImage', detectfaces['error']['code'],
                    detectfaces['error']['message'])
                return []
            return detectfaces
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return []

    # 用本地端的圖檔進行辨識。
    def detectLocalImage(self, imagepath):
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',  # 用本地圖檔辨識
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId':
            'true',
            'returnFaceLandmarks':
            'false',
            'returnFaceAttributes':
            'age,gender,emotion'
        })
        #'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure'
        print('imagepath=', imagepath)
        requestbody = open(imagepath, "rb").read()
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody,
                         headers)
            response = conn.getresponse()
            data = response.read()
            print('data=', data)
            detectfaces = json.loads(str(data, 'UTF-8'))
            print("detectLocalImage.faces=", detectfaces)
            #print(parsed[0]['faceId'])
            #faceids.append(parsed[0]['faceId'])
            conn.close()
            if 'error' in detectfaces:
                ClassMessageBox.FaceAPIErrorGUI(
                    'def detectLocalImage', detectfaces['error']['code'],
                    detectfaces['error']['message'])
                return []

            # if('error' in faces):
            #     print("讀取 faces 發生錯誤！！ message="+faces['error']['message'])
            #     return []

            print("detectLocalImage:",
                  imagepath + "偵測到 {0} 個人".format(len(detectfaces)))
            #display(Image(filename=imagepath))
            for detectface in detectfaces:
                #print("face = ", face)
                print("faceRectangle = ", detectface['faceRectangle'])
                print("faceId = ", detectface['faceId'])
                left = detectface['faceRectangle']['left']
                top = detectface['faceRectangle']['top']
                height = detectface['faceRectangle']['height']
                width = detectface['faceRectangle']['width']

                img = Image.open(imagepath)
                #faceRectangle =  {'top': 141, 'height': 261, 'width': 261, 'left': 664}
                onlyface = img.crop((left, top, left + width, top + height))

                savejpgimage = basepath + "/tmp/faceId_" + detectface['faceId'] + ".jpg"
                if not os.path.exists(os.path.dirname(savejpgimage)):
                    os.makedirs(os.path.dirname(savejpgimage))
                onlyface.save(savejpgimage, 'JPEG')
                #display(img2)
                #area = (left, top, left+width, top+height)
                #cropped_img = img.crop(area)
                #cropped_img.show()

            return detectfaces
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            return []


class FaceList:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host

    def listFacelists(self):
        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/face/v1.0/facelists?%s" % params, "{body}",
                         headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
