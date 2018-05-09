import sys, os
from gtts import gTTS
from pygame import mixer


s = sys.argv[1]

basepath = '/home/pi/mp3/'
if not os.path.exists(os.path.dirname(basepath)):
    os.makedirs(os.path.dirname(basepath))

tts=gTTS(text=s, lang='zh-tw')
mp3path = basepath+s+".mp3"
tts.save(mp3path)

mixer.init()
mixer.music.load(mp3path)
mixer.music.play()

