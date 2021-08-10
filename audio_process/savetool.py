# -*- coding: utf-8 -*-
#接收识别结果（api/离线模型）并进行保存，还可以输入t_start和t_keep参数来生成字幕文件，但这两个参数最好还是用整数，float也行但应该保留两位小数
#两个t可以通过indexlist来取
import json

class savetool:
	def __init__(self,out_path):
		self.f = open(out_path, 'w',encoding='utf8')
	def close(self):
		self.f.close()
	def api_save(self,input,t_start=0,t_keep=0):
		dict=json.loads(input)
		if(dict['err_msg']=='success.'):
			res=dict['result'][0].strip('& ')#使用& 作为分隔符号，以防万一先去掉结果开头末尾的这个符号
			self.f.write(res)
			if(t_start or t_keep):#两个全输入0或者''，则不写两个t参数，只输入句子
				sn = '& '+str(t_start)+'& '+str(t_keep)+'\n'
				self.f.write(sn)
			else:
				self.f.write('\n')
			return 1
		elif(dict['err_msg']=='speech quality error.'):
			res=' '#使用& 作为分隔符号，以防万一先去掉结果开头末尾的这个符号
			self.f.write(res)
			if(t_start or t_keep):#两个全输入0或者''，则不写两个t参数，只输入句子
				sn = '& '+str(t_start)+'& '+str(t_keep)+'\n'
				self.f.write(sn)
			else:
				self.f.write('\n')
			return 1
		else:
			res=' '#使用& 作为分隔符号，以防万一先去掉结果开头末尾的这个符号
			self.f.write(res)
			if(t_start or t_keep):#两个全输入0或者''，则不写两个t参数，只输入句子
				sn = '& '+str(t_start)+'& '+str(t_keep)+'\n'
				self.f.write(sn)
			else:
				self.f.write('\n')
			return 0
	def str_save(self,input,t_start,t_keep):#离线模型用这个方法，但如果手动loadjson，api也是可以用的，这个方法没有返回值
		self.f.write(input)
		if(t_start or t_keep):
			sn = '& '+str(t_start)+'& '+str(t_keep)+'\n'
			self.f.write(sn)
		else:
			self.f.write('\n')
#格式：文字& t_start& t_keep
class readtool:#用于从index_list文件读取时间并迭代
	def __init__(self,index_path):#index文件也可以自己写，不需要索引顺序一致，因为这里是按照文件名取的，但如果想要减少时间，就可以通过排序和索引方式来读写
		with open(index_path,encoding='utf8') as f:
			self.content = f.readlines()#记得要strip \n，格式为[文件名,t_start,t_keep\n]
	def read(self,pos):#读取出来的是[t_start,t_keep],并且是字符串形式.pos输入需要的文件名，通过文件名的列表同时进行读取和进行识别应当是较方便的算法
		for k in self.content:
			if(pos==k.split(',')[0]):
				ret = [k.split(',')[1],k.split(',')[2].strip('\n')]
		return ret

def changeline(path,replace_index,input_str):#只修改第一个& 之前的数据，即字幕部分，而不修改开始时间、持续时间,参数依次为字幕文件路径，修改行号，新字符串
	f=open(path,'r+',encoding='utf8')
	flist=f.readlines()
	f.close()
	flist[replace_index]=input_str+'& '+flist[replace_index].split('& ')[1]+'& '+flist[replace_index].split('& ')[2]
	f=open(path,'w+',encoding='utf8')
	f.writelines(flist)
	f.close()
