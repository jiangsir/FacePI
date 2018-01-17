import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import os, sys


class PersonGroup:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host
        '''
        basepath = os.path.dirname(os.path.realpath(__file__))
        with open(basepath + '/FacePI-Config.json', 'r') as f:
            config = json.load(f)
        self.api_key = config["api_key"]
        self.host = config["host"]
        self.personGroupId = config['personGroupId']
        '''

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
            #print(data)
            persons = json.loads(str(data, 'UTF-8'))
            conn.close()
            return persons
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def ListPersonGroups(self):
        print('列出所有的 person Groups')
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
            print('共', len(personGroups), '個 =', personGroups)
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
        print("建立一個 personGroupid = " + personGroupId)
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
        body = "{ 'name':'" + groupname + "', 'userData':'" + groupdata + "' }"

        try:
            # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
            #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the
            #   URL below with "westus".
            conn = http.client.HTTPSConnection(self.host)
            conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId,
                         body, headers)
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
            print("開始訓練一個 personGroup personGroupId=" + personGroupId + "。")

            headers = {
                # Request headers
                'Ocp-Apim-Subscription-Key': self.api_key,
            }

            params = urllib.parse.urlencode({'personGroupId': personGroupId})

            try:
                conn = http.client.HTTPSConnection(self.host)
                conn.request("POST", "/face/v1.0/persongroups/" +
                             personGroupId + "/train?%s" % params, "{body}",
                             headers)
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
                conn.request("GET", "/face/v1.0/persongroups/" +
                             personGroupId + "/training?%s" % params, "{body}",
                             headers)
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
        print("用一個圖片放入一個 person 當中 personId=" + personId)
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
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

        def create_a_person(self, personGroupId, name, descript):
            print("在 personGroupid=" + personGroupId + " 裡 建立一個 person name=" +
                  name)
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
                             requestbody, headers)
                response = conn.getresponse()
                data = response.read()
                #print(data)
                create_a_person_json = json.loads(str(data, 'UTF-8'))

                conn.close()
                return create_a_person_json['personId']
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))

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
                conn.request("GET", "/face/v1.0/persongroups/" +
                             personGroupId + "/persons?%s" % params, "{body}",
                             headers)
                response = conn.getresponse()
                data = response.read()
                #print(data)
                persons = json.loads(str(data, 'UTF-8'))
                conn.close()
                return persons
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))


class Face:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host

    def identify(self, faceids, personGroupId):
        print("開始辨識。faceids=", faceids, " , personGroupId=", personGroupId)
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.api_key,
        }

        params = urllib.parse.urlencode({})

        requestbody = '''{
            "personGroupId": "''' + personGroupId + '''",
            "faceIds":''' + str(faceids) + ''',
            "maxNumOfCandidatesReturned":1,
            "confidenceThreshold": 0.5
        }'''
        print('requestbody=', requestbody)
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/identify?%s" % params,
                         requestbody, headers)
            response = conn.getresponse()
            data = response.read()
            #print(data)
            facejson = json.loads(str(data, 'UTF-8'))
            #print(facejson)
            conn.close()
            return facejson
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
            sys.exit()

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
            'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure'
        })
        print('imagepath=', imagepath)
        requestbody = open(imagepath, "rb").read()
        try:
            conn = http.client.HTTPSConnection(self.host)
            conn.request("POST", "/face/v1.0/detect?%s" % params, requestbody,
                         headers)
            response = conn.getresponse()
            data = response.read()
            faces = json.loads(str(data, 'UTF-8'))
            #print(parsed[0]['faceId'])
            #faceids.append(parsed[0]['faceId'])
            conn.close()
            return faces
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


class FaceList:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host
