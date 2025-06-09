from gtts import gTTS
import os

def say(text):
  tts = gTTS(text=text, lang='en')
  tts.save("geeks.mp3")

  os.system("mpg321 geeks.mp3")
  
say("Hello, Geeks for Geeks!")
