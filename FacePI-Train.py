import http.client, urllib.request, urllib.parse, urllib.error, base64, json
import sys, os, time
import tkinter



if len(sys.argv)<3:
    print("Train.py <pergonGroupId> <personname> 即時拍照進行訓練")
    print("Train.py <pergonGroupId> <personname> <faceimage1> ...  直接指定圖片進行訓練")
    sys.exit()

personGroupId = sys.argv[1]
personname = sys.argv[2]
trainimages = []

basepath = os.path.dirname(os.path.realpath(__file__))

with open(basepath + '/FacePI-Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']


def takePicture():
    imagepath = personGroupId+"_"+personname+"_"+time.strftime("%Y-%m-%d:%H:%M:%S", time.localtime())+".jpg"
    os.system("raspistill -t 3000 -o " + imagepath)
    print("imagepath = " + imagepath)
    return imagepath

if len(sys.argv)==3:
    trainimages.append(takePicture())
elif len(sys.argv)>3:
    trainimages = sys.argv[3:]
    
print("trains = " + str(trainimages))

def create_personGroup(personGroupId, groupname, groupdata):
    print("建立一個 personGroupid = "+personGroupId)
    headers = {
        # Request headers.
        'Content-Type': 'application/json',

        # NOTE: Replace the "Ocp-Apim-Subscription-Key" value with a valid subscription key.
        'Ocp-Apim-Subscription-Key': api_key,
    }

    # Replace 'examplegroupid' with an ID you haven't used for creating a group before.
    # The valid characters for the ID include numbers, English letters in lower case, '-' and '_'. 
    # The maximum length of the ID is 64.
    #personGroupId = 'examplegroupid'
    #personGroupId = 'jiangsir_groupid2'

    # The userData field is optional. The size limit for it is 16KB.
    body = "{ 'name':'"+groupname+"', 'userData':'"+groupdata+"' }"

    try:

        # NOTE: You must use the same location in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westus, replace "westcentralus" in the 
        #   URL below with "westus".
        conn = http.client.HTTPSConnection(host)
        conn.request("PUT", "/face/v1.0/persongroups/%s" % personGroupId, body, headers)
        response = conn.getresponse()

        # 'OK' indicates success. 'Conflict' means a group with this ID already exists.
        # If you get 'Conflict', change the value of personGroupId above and try again.
        # If you get 'Access Denied', verify the validity of the subscription key above and try again.
        print(response.reason)

        conn.close()
        return personGroupId
    except Exception as e:
        print(e.args)
        
        
        
        



##################################################################################################
### main
##################################################################################################


personGroupId = create_personGroup(personGroupId, "personGroup namenamename", "junior class students")
personId = create_a_person(personGroupId, personname, "juniorclass_userDatauserData")

for trainimage in trainimages:
    add_a_person_face(trainimage, personId, personGroupId)


train_personGroup(personGroupId)
personGroup_status(personGroupId)

