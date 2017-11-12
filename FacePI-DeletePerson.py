import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

basepath = os.path.dirname(os.path.realpath(__file__))

with open(basepath + '/FacePI-Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']

personId = 'bb8400b5-3a78-4ba0-8168-dbe48453a4d6'
personIds = [
    'bb8400b5-3a78-4ba0-8168-dbe48453a4d6',
    '020a3ca7-8b45-4972-8057-b4e078e98367',
    '19b093d9-1699-45ea-b12c-d8efacfb18f8',
    '263c960e-ae72-4e44-ac29-a314e0ed434f',
    '5409c1b8-4a7c-48b3-8e37-35c76dccf076',
    '5a3df061-9f19-4d1e-a4a1-a64e58ea282d',
    '6f5cb711-6aeb-476f-8548-f6fe77c70dd1',
    '74555c60-1d1a-4282-8a5c-9c84d63ce9d8',
    'e8e690ab-f2d2-4f7e-aed0-10290276b0ee',
    '9ca21460-e6a0-4500-ae82-b33c96d4eab5'
]
headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': api_key,
}


def deletePersonId(personGroupId, personId):
    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("DELETE", "/face/v1.0/persongroups/" + personGroupId +
                     "/persons/" + personId + "?%s" % params, "{body}",
                     headers)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


for personId in personIds:
    deletePersonId(personGroupId, personId)
