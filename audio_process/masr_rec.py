# -*- coding: utf-8 -*-
#需要安装masr
from masr.models.conv import GatedConv
import configparser as ConfigParser
def getConfig(section, key):
	config = ConfigParser.ConfigParser()
	pathforconfig = './general_config.conf'
	config.read(pathforconfig)
	return config[section][key]

class masr_model:
	def __init__(self,model_path=getConfig('model_path','masr_model')):
		try:
			import audio_process.beamdecode as beamdecode
			if(getConfig('model_path','lm_model')):
				self.state=1
				print('[+]It seems that you are using lm_model now.')
			else:
				self.state=0
		except:
			self.model = GatedConv.load(model_path)
			self.state=0
	def rec(self,input='save_audio/0.wav'):
		if self.state==1:
			return beamdecode.predict(input)
		else:
			return self.model.predict(input)
#实际使用中，可以通过创建的masr_model对象的state属性来判断有没有成功加载语言模型
