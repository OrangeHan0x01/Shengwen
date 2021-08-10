# coding=utf-8
import sys
import json
import time
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
import configparser as ConfigParser

def getConfig(section, key):
	config = ConfigParser.ConfigParser()
	pathforconfig = './general_config.conf'
	config.read(pathforconfig)
	return config[section][key]
#可以使用一个class来做这些工作
class BaiduSR:
	def __init__(self):
		self.API_KEY = getConfig('BaiduSR_api','API_KEY')#输入appkey
		self.SECRET_KEY = getConfig('BaiduSR_api','SECRET_KEY')#填写网页上申请的APP SECRET
		if(self.API_KEY==''):
			print('初始化失败：没有在config文件中设置API_KEY!请设置API与密钥后再使用百度语音识别')
			exit()
		self.CUID = '123456PYTHON'
		self.RATE = 16000
		self.DEV_PID = 1537;  # 1537 表示识别普通话，使用输入法模型。根据文档填写PID，选择语言及识别模型
		self.ASR_URL = 'http://vop.baidu.com/server_api'
		self.SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选，非常旧的应用可能没有
		self.TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
	def fetch_token(self):
		params = {'grant_type': 'client_credentials','client_id': self.API_KEY,'client_secret': self.SECRET_KEY}
		post_data = urlencode(params)
		post_data = post_data.encode('utf-8')
		req = Request(self.TOKEN_URL, post_data)
		try:
			f = urlopen(req)
			result_str = f.read()
		except URLError as err:
			print('token http response http code : ' + str(err.code))
			result_str = err.read()
		result_str = result_str.decode()
		result = json.loads(result_str)
		if ('access_token' in result.keys() and 'scope' in result.keys()):
			if self.SCOPE and (not self.SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
				print('scope is not correct')
			return result['access_token']
		else:
			print('出错，可能是api key填写不正确?')

	def rec(self,file='./out.wav',outf=''):#outf为''空值时不输出文件，否则输出到一个文件中，可以用文本文件
		self.AUDIO_FILE = file  # 只支持 pcm/wav/amr 格式，极速版额外支持m4a 格式
		self.FORMAT = self.AUDIO_FILE[-3:]
		token = self.fetch_token()
		speech_data = []
		with open(self.AUDIO_FILE, 'rb') as speech_file:
			speech_data = speech_file.read()
		length = len(speech_data)
		if length == 0:
			raise DemoError('file %s length read 0 bytes' % self.AUDIO_FILE)
		params = {'cuid': self.CUID, 'token': token, 'dev_pid': self.DEV_PID}
		params_query = urlencode(params);
		self.headers = {'Content-Type': 'audio/' + self.FORMAT + '; rate=' + str(self.RATE),'Content-Length': length}
		url = self.ASR_URL + "?" + params_query
		req = Request(self.ASR_URL + "?" + params_query, speech_data, self.headers)
		try:
			f = urlopen(req)
			result_str = f.read()
		except  URLError as err:
			result_str = err.read()
		result_str = str(result_str, 'utf-8')
		print(result_str)
		if(outf):
			with open(outf, "w") as of:#这种识别方式有依赖于网络环境的延迟
				of.write(result_str)
		return result_str#返回值是json格式的