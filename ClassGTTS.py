import sys, os, platform, time
from gtts import gTTS
#import pygame as pygamee
from pypinyin import lazy_pinyin
import ClassUtils

mp3base = os.path.join(ClassUtils.getBasepath(), 'mp3')
if not os.path.exists(os.path.dirname(mp3base)):
    os.makedirs(os.path.dirname(mp3base))

def play_gTTS(name, text):
    start = int(round(time.time() * 1000))
    print('開始計時 play_gTTS 0 ms: ', name, text)

    #text = '_'.join(lazy_pinyin(text))
    name = ClassUtils.protectPersonName(name)

    mp3path = os.path.join(mp3base, name + text + ".mp3")
    #print('gTTS:', str(name + text).encode("utf8"), 'mp3path:', mp3path, os.path.isfile(mp3path))
    print('SPEED: play_gTTS mp3path', int(round(time.time() * 1000) - start),
          'ms')

    if os.path.isfile(mp3path) == False:
        tts = gTTS(
            text=ClassUtils.protectPersonNameForTTS(name) + text, lang='zh-tw')
        tts.save(mp3path)
        print('SPEED: play_gTTS savemp3',
              int(round(time.time() * 1000) - start), 'ms')

    sysstr = platform.system()
    #print('system='+sysstr)
    # print('SPEED: pygame play 前', int(round(time.time() * 1000) - start), 'ms')
    # if (sysstr == "Windows"):
    #     print("Call Windows tasks")
    #     pygamee.mixer.init()
    #     pygamee.mixer.music.load(mp3path)
    #     pygamee.mixer.music.play()
    #     while pygamee.mixer.music.get_busy():
    #         pygamee.time.Clock().tick(10)
    # elif (sysstr == "Darwin"):
    #     print("Call macOS tasks")
    #     pygamee.mixer.init()
    #     pygamee.mixer.music.load(mp3path)
    #     pygamee.mixer.music.play()
    #     while pygamee.mixer.music.get_busy():
    #         pygamee.time.Clock().tick(10)
    # elif (sysstr == "Linux"):
    #     #os.system('omxplayer ' + mp3path +" > /dev/null 2>&1")
    #     pygamee.mixer.init()
    #     pygamee.mixer.music.load(mp3path)
    #     pygamee.mixer.music.play()
    #     while pygamee.mixer.music.get_busy() == True:
    #         continue
    # else:
    #     print("Call Other OS tasks")
    #     pygamee.mixer.init()
    #     pygamee.mixer.music.load(mp3path)
    #     pygamee.mixer.music.play()
    #     while pygamee.mixer.music.get_busy():
    #         pygamee.time.Clock().tick(5)
    print('SPEED: pygame play 後', int(round(time.time() * 1000) - start), 'ms')
