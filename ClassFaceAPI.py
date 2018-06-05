import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import os, sys, time
from PIL import Image, ImageDraw
import ClassUtils
import MyException
from urllib import request
import ClassFaceAPI as FaceAPI

basepath = os.path.dirname(os.path.realpath(__file__))
with open(basepath + '/Config.json', 'r', encoding='utf-8') as f:
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
            persons = json.loads(str(data, 'UTF-8'))
            conn.close()

            try:
                if ClassUtils.isFaceAPIError(persons):
                    pass
            except MyException.RateLimitExceededError as e:
                time.sleep(10)
                return self.list_persons_in_group(personGroupId)
            except MyException.PersonGroupNotFoundError as e:
                self.createPersonGroup(config['personGroupId'],
                                    config['personGroupName'], 'group userdata')
                return self.list_persons_in_group(config['personGroupId'])

            if 'error' in persons:
                message = '取得 persons 出錯！\n'
                message += '錯誤編號 = ' + persons['error']['code'] + '\n'
                message += '錯誤訊息 = ' + persons['error']['message']
                raise MyException.responseError(message)
            return persons
            
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))


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
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
        try:
            if ClassUtils.isFaceAPIError(personGroups):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.ListPersonGroups()
        except MyException.UnspecifiedError as e:
            return

        return personGroups

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
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

        try:
            if ClassUtils.isFaceAPIError(personGroup):
                pass
            return personGroup
        except MyException.UnspecifiedError as e:
            return

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
            self.train_personGroup(personGroupId)
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
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

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
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
        try:
            if ClassUtils.isFaceAPIError(status):
                return None
            return status
        except MyException.UnspecifiedError as e:
            return

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
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))


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
            # if 'error' in jsondata:
            #     if 'RateLimitExceeded' == jsondata['error']['code']:
            #         time.sleep(10)
            #     else:
            #         print("EXCEPTION: ", jsondata['error']['code'] + ":",
            #               jsondata['error']['message'])

        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

        try:
            if ClassUtils.isFaceAPIError(jsondata):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.add_a_person_face(imagepath, personId, personGroupId)
        except MyException.UnspecifiedError as e:
            return

    def create_a_person(self, personGroupId, name, userData):
        print("'create_a_person': 在 personGroupid=" + personGroupId +
              " 裡 建立一個 person name=" + name)
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({'personGroupId': personGroupId})
        requestbody = '{"name":"' + name + '","userData":"' + userData + '"}'

        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/persongroups/" +
                         personGroupId + "/persons?%s" % params,
                         requestbody.encode('UTF-8'), headers)
            response = conn.getresponse()
            data = response.read()
            create_a_person_json = json.loads(str(data, 'UTF-8'))
            conn.close()
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

        try:
            if ClassUtils.isFaceAPIError(create_a_person_json):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.create_a_person(personGroupId, name, userData)
        except MyException.PersonGroupNotFoundError as e:
            personGroupApi = PersonGroup(self.api_key, self.host)
            personGroupApi.createPersonGroup(config['personGroupId'],
                                             config['personGroupName'],
                                             'group userdata')
            return self.create_a_person(personGroupId, name, userData)
        except MyException.UnspecifiedError as e:
            return

        return create_a_person_json['personId']

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
            persons = json.loads(str(data, 'UTF-8'))
            #print('def list_persons_in_group:', persons)
            conn.close()
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
            return []

        try:
            if ClassUtils.isFaceAPIError(persons):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.list_persons_in_group(personGroupId)
        except MyException.PersonGroupNotFoundError as e:
            personGroupAPI = PersonGroup(self.api_key, self.host)
            personGroupAPI.createPersonGroup(config['personGroupId'],
                                             config['personGroupName'],
                                             'group userdata')
            return self.list_persons_in_group(personGroupId)
        except MyException.UnspecifiedError as e:
            return

        return persons

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
            #datajson = json.loads(str(data, 'UTF-8'))
            print('deletePerson:', data)
            conn.close()
            # if ClassUtils.isFaceAPIError(datajson):
            #     pass
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

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

            try:
                if ClassUtils.isFaceAPIError(personjson):
                    return None
            except MyException.RateLimitExceededError as e:
                time.sleep(10)
                return self.get_a_person(personId, personGroupId)
            except MyException.UnspecifiedError as e:
                return
            except MyException.PersonGroupNotTrainedError as e:
                print('ERROR: get_a_person.PersonGroupNotTrainedError')
                return
            return personjson
            
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))

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

    def add_personimages(self, personGroupId, personname, userData,
                           imagepaths):
        ''' # 加入一個人的一張或多張圖片，但不訓練 '''
        print("personname=", personname, "圖檔:", imagepaths)
        personAPI = FaceAPI.Person(self.api_key, self.host)
        person = self.getPersonByName(personGroupId, personname)
        if person == None:
            print('call create_a_person')
            personid = self.create_a_person(personGroupId, personname,
                                                 userData)
            for imagepath in imagepaths:
                self.add_a_person_face(imagepath, personid, personGroupId)
        else:
            print('call add_a_person_face, personId=', person['personId'])
            for imagepath in imagepaths:
                self.add_a_person_face(imagepath, person['personId'],
                                            personGroupId)


class Face:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host

    def identify(self, faceidkeys, personGroupId):
        print("def Face.identify 開始辨識。faceidkeys=", faceidkeys)
        if len(faceidkeys) == 0:
            return []
        start = int(round(time.time() * 1000))
        print('開始辨識 identify 0 ms')

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
            "confidenceThreshold": ''' + str(config['confidence']) + '''
        }'''
        #print('requestbody=', requestbody)
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/identify?%s" % params,
                         requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            identifyfaces = json.loads(str(data, 'UTF-8'))
            print('Face.Identify.identifyfaces=', identifyfaces)
            conn.close()
            # ClassUtils.tryFaceAPIError(identifyfaces)
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
            sys.exit()

        try:
            if ClassUtils.isFaceAPIError(identifyfaces):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.identify(faceidkeys, personGroupId)
        except MyException.PersonGroupNotFoundError as e:
            personGroupAPI = PersonGroup(self.api_key, self.host)
            personGroupAPI.createPersonGroup(personGroupId,
                                            config['personGroupName'],
                                            'group userdata')
            return self.identify(faceidkeys, personGroupId)
        except MyException.UnspecifiedError as e:
            return []
        except MyException.PersonGroupNotTrainedError as e:
            print('丟出 MyException.PersonGroupNotTrainedError 例外')
            raise
        print('超過 raise')
        # if ClassUtils.isFaceAPIError(identifyfaces):
        #     return []
        return identifyfaces


    def __detectFaces_Save(self, detectFaces, imagepath):
        for detectface in detectFaces:
            print("faceRectangle = ", detectface['faceRectangle'])
            print("faceId = ", detectface['faceId'])
            left = detectface['faceRectangle']['left']
            top = detectface['faceRectangle']['top']
            height = detectface['faceRectangle']['height']
            width = detectface['faceRectangle']['width']

            img = Image.open(imagepath)
            draw = ImageDraw.Draw(img)
            if config['landmark'] > 0:
                print("save facelandmarks=", detectface['faceLandmarks'])
                for faceLandmark in detectface['faceLandmarks']:
                    print('faceLandmark=', faceLandmark)
                    print('faceLandmark=',
                        detectface['faceLandmarks'][faceLandmark])
                    x = int(detectface['faceLandmarks'][faceLandmark]['x'])
                    y = int(detectface['faceLandmarks'][faceLandmark]['y'])
                    draw.ellipse(
                        (x, y, x + config['landmark'], y + config['landmark']),
                        fill=(255, 0, 0))
            #faceRectangle =  {'top': 141, 'height': 261, 'width': 261, 'left': 664}
            faceonly = img.crop((left, top, left + width, top + height))

            saveFaceImagepath = ClassUtils.getFaceImagepath(
                detectface['faceId'])
            faceonly.save(saveFaceImagepath, 'PNG')

    ''' 用網路上的圖片進行偵測。'''

    def detectURLImages(self, imageurl):
        ''' 下載後，用 detectLocalImage 上傳辨識 '''
        jpgimagepath = ClassUtils.getTakePicturePath(config['personGroupId'])
        print('jpgimagepath:', jpgimagepath)
        request.urlretrieve(imageurl, jpgimagepath)
        return self.detectLocalImage(jpgimagepath)

    ''' 不下載直接用 URL 進行辨識 '''

    def detectURLImages_NoDownload(self, imageurl):
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
        print('imageurl=', imageurl)
        requestbody = '{"url": "' + imageurl + '"}'

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
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
            #return []

        try:
            if ClassUtils.isFaceAPIError(detectfaces):
                return []
        except MyException.RateLimitExceededError as e:
            time.sleep(10)
            return self.detectURLImages(imageurl)
        except MyException.UnspecifiedError as e:
            return

        self.__detectFaces_Save(detectfaces, imageurl)
        return detectfaces

    # 用本地端的圖檔進行辨識。
    def detectLocalImage(self, imagepath):
        start = int(round(time.time() * 1000))
        print('開始計時 detectLocalImage 0 ms')

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
            'true',
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
            print('detectLocalImage.data=', data)
            detectfaces = json.loads(str(data, 'UTF-8'))
            print("detectLocalImage.faces=", detectfaces)
            #print(parsed[0]['faceId'])
            #faceids.append(parsed[0]['faceId'])
            conn.close()

            try:
                if ClassUtils.isFaceAPIError(detectfaces):
                    return []
            except MyException.RateLimitExceededError as e:
                time.sleep(10)
                return self.detectLocalImage(imagepath)
            except MyException.PersonGroupNotTrainedError as e:
                print('ERROR: detectLocalImage MyException.PersonGroupNotTrainedError')
                return
            except MyException.UnspecifiedError as e:
                return

            print("detectLocalImage:",
                imagepath + "偵測到 {0} 個人".format(len(detectfaces)))

            self.__detectFaces_Save(detectfaces, imagepath)
            return detectfaces
            
        except Exception as e:
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
            #return []



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
            print("[Errno {0}]連線失敗！請檢查網路設定。 {1}".format(e.errno, e.strerror))
