import tkinter as tk
from tkinter import font
import os, sys, json
import FaceAPI

basepath = os.path.dirname(os.path.realpath(__file__))

with open(basepath + '/FacePI-Config.json', 'r') as f:
    config = json.load(f)
api_key = config["api_key"]
host = config["host"]
personGroupId = config['personGroupId']

PersonGroup = FaceAPI.PersonGroup(api_key, host)

PersonGroup.ListPersonGroups()

PersonGroup.getPersonGroup('personGroupId')

#personGroup.createPersonGroup('junior', 'jiangsir_juniorclass', 'jiangsir_groupdata')

PersonGroup.ListPersonGroups()

personGroupId = 'junior2'
personGroup = PersonGroup.getPersonGroup(personGroupId)
if ('error' in personGroup):
    PersonGroup.createPersonGroup(personGroupId, personGroupId + '_groupname',
                                  personGroupId + '_groupdata')
    personGroup = PersonGroup.getPersonGroup(personGroupId)

print('id = ', personGroup['personGroupId'])
