import os, json

def loadConfig():
    basepath = getBasepath()
    with open(basepath + '/Config.json', 'r') as f:
        config = json.load(f)
    return config

def getBasepath():
    basepath = os.path.dirname(os.path.realpath(__file__))
    return basepath

def protectPersonName(name):
    return name[0]+'〇'+name[2:]

def protectPersonNameForTTS(name):
    return name[0]+'圈'+name[2:]