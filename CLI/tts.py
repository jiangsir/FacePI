import sys
from gtts import gTTS
from pygame import mixer

s = sys.argv[1]

tts=gTTS(text=s, lang='zh-tw')
tts.save("tts.mp3")

mixer.init()
mixer.music.load('tts.mp3')
mixer.music.play()

