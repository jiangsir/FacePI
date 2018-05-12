import sys, os, platform
from gtts import gTTS
import pygame as pygame
from pypinyin import lazy_pinyin

basepath = os.path.dirname(os.path.realpath(__file__)) + '/mp3/'
if not os.path.exists(os.path.dirname(basepath)):
    os.makedirs(os.path.dirname(basepath))


def play_gTTS(text):
    tts = gTTS(text=text, lang='zh-tw')
    #text = '_'.join(lazy_pinyin(text))
    mp3path = basepath + text + ".mp3"
    print('gTTS:', text, 'mp3path:', mp3path)
    if os.path.exists(mp3path) == False:
        tts.save(mp3path)

    sysstr = platform.system()
    if (sysstr == "Windows"):
        print("Call Windows tasks")
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
    elif (sysstr == "Darwin"):
        print("Call macOS tasks")
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
    elif (sysstr == "Linux"):
        os.system('omxplayer ' + mp3path)
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
