import http.client, urllib.request, urllib.parse, urllib.error, base64
import json, os, sys

basepath = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) < 2:
    print(sys.argv[0] + " <person name> 要刪除的名字")
    sys.exit()

personname = sys.argv[1]

with open(basepath + '/FacePI-Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': api_key,
}


def list_persons_in_group(personGroupId):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': api_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        #'start': '{string}',
        #'top': '1000',
    })

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", "/face/v1.0/persongroups/" + personGroupId +
                     "/persons?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        persons = json.loads(str(data, 'UTF-8'))
        conn.close()
        return persons
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


def deletePersonId(personGroupId, personId):
    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection(host)
        conn.request("DELETE", "/face/v1.0/persongroups/" + personGroupId +
                     "/persons/" + personId + "?%s" % params, "{body}",
                     headers)
        response = conn.getresponse()
        data = response.read()
        print(str(data, 'UTF-8') + " 成功！")
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


#for personId in personIds:
#    deletePersonId(personGroupId, personId)

persons = list_persons_in_group(personGroupId)

for person in persons:
    if person['name'] == personname:
        print('刪除 ', person['name'], person['personId'])
        deletePersonId(personGroupId, person['personId'])
    else:
        print('', person['name'], person['personId'])
