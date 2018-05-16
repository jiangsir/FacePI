import sys, os, platform
from gtts import gTTS
import pygame as pygame
from pypinyin import lazy_pinyin
import ClassUtils as Utils

basepath = os.path.dirname(os.path.realpath(__file__)) + '/mp3/'
if not os.path.exists(os.path.dirname(basepath)):
    os.makedirs(os.path.dirname(basepath))


def play_gTTS(name, text):
    tts = gTTS(text=Utils.protectPersonNameForTTS(name) + text, lang='zh-tw')
    #text = '_'.join(lazy_pinyin(text))
    name = Utils.protectPersonName(name)
    text = name + text
    mp3path = basepath + text + ".mp3"
    print('gTTS:', text, 'mp3path:', mp3path)
    if os.path.exists(mp3path) == False:
        tts.save(mp3path)

    sysstr = platform.system()
    print('system='+sysstr)
    if (sysstr == "Windows"):
        print("Call Windows tasks")
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    elif (sysstr == "Darwin"):
        print("Call macOS tasks")
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    #elif (sysstr == "Linux"):
    #    os.system('omxplayer ' + mp3path)
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
