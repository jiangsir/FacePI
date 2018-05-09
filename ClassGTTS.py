import sys, os
from gtts import gTTS
from pygame import mixer

basepath = '~/mp3/'
if not os.path.exists(os.path.dirname(basepath)):
    os.makedirs(os.path.dirname(basepath))

def play_gTTS(text):
    tts=gTTS(text=text, lang='zh-tw')
    mp3path = basepath+text+".mp3"
    if  os.path.exists(mp3path)==False:
        tts.save(mp3path)
    os.system('omxplayer '+mp3path)

#mixer.init()
#mixer.music.load(mp3path)
#mixer.music.play()

