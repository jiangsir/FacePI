import sys, os, platform, time
from gtts import gTTS
import pygame as pygame
from pypinyin import lazy_pinyin
import ClassUtils as Utils

basepath = os.path.dirname(os.path.realpath(__file__)) + '/mp3/'
if not os.path.exists(os.path.dirname(basepath)):
    os.makedirs(os.path.dirname(basepath))


def play_gTTS(name, text):
    start = int(round(time.time() * 1000))
    print('開始計時 play_gTTS 0 ms')

    #text = '_'.join(lazy_pinyin(text))
    name = Utils.protectPersonName(name)

    mp3path = basepath + name + text + ".mp3"
    print('gTTS:', name + text, 'mp3path:', mp3path, os.path.isfile(mp3path))
    print('SPEED: play_gTTS mp3path', int(round(time.time() * 1000) - start),
          'ms')

    if os.path.isfile(mp3path) == False:
        tts = gTTS(
            text=Utils.protectPersonNameForTTS(name) + text, lang='zh-tw')
        tts.save(mp3path)
        print('SPEED: play_gTTS savemp3',
              int(round(time.time() * 1000) - start), 'ms')

    sysstr = platform.system()
    #print('system='+sysstr)
    print('SPEED: pygame play 前', int(round(time.time() * 1000) - start), 'ms')
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
    elif (sysstr == "Linux"):
        #os.system('omxplayer ' + mp3path +" > /dev/null 2>&1")
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    else:
        print("Call Other OS tasks")
        pygame.mixer.init()
        pygame.mixer.music.load(mp3path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
    print('SPEED: pygame play 後', int(round(time.time() * 1000) - start), 'ms')
