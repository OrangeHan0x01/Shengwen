# -*- coding: utf-8 -*-
import pyttsx3
def tts(str,out='test.mp3',rate=150,volume=1):#rate每分钟读字，volume改变音量，范围（0-2）
	eng = pyttsx3.init()
	try:
		eng.setProperty('voice','zh')
		eng.setProperty('rate', rate)
		eng.setProperty('volume', volume)
		eng.save_to_file(str , out)
		eng.runAndWait()
	except:
		eng.setProperty('rate', rate)
		eng.setProperty('volume', volume)
		eng.save_to_file(str , out)
		eng.runAndWait()
def tts_say(txt='测试'):
	eng = pyttsx3.init()
	try:
		eng.setProperty('voice','zh')
		eng.say(txt)
		eng.runAndWait()
	except:
		eng.say(txt)
		eng.runAndWait()
