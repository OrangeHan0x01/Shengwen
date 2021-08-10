# -*- coding: utf-8 -*-
#百度语音识别api支持60s以下，故使用时将语音拼接到尽量接近60s，提高利用效率和降低价格
from pydub import AudioSegment
import os
#语音拼接函数
def audio_combine(pth_list,out_path,tl=55):#输入的pth_list是列表，输出out_path则是文件夹，文件夹别忘加/，默认上限55秒，t=0时全部一起输出，离线识别建议tl在5-12秒之间，输出文件名显然是'数字.wav'的格式
#先输入列表，设置参数分别代表pth的数字和输出的路径，循环提取音频长度和计算总值，增加后若>=55则先输出，此外到最后不满55的也要一起输出，还要注意和原本不应该是同一个文件夹
	isExists=os.path.exists(out_path.rstrip('/'))
	if not isExists:
		os.makedirs(out_path)
	time_total=0
	out_count=0
	if(tl!=0):
		for i in range(len(pth_list)):
			nwav=AudioSegment.from_wav(pth_list[i])
			st=nwav.duration_seconds
			if(i==0):#如果是第一个文件
				playlist=nwav
				time_total=st
			elif(i==len(pth_list)-1):#如果是最后一个文件
				test_t=time_total+st
				if(test_t>=tl):#如果是最后一个文件，不管是否到了都输出，但是到了的话需要额外一步判断
					playlist.export(out_path+str(out_count)+'.wav',format='wav')#导出的肯定<=55,除非你第一个文件就>55秒了
					out_count+=1
					playlist=nwav
					time_total=st
					playlist.export(out_path+str(out_count)+'.wav',format='wav')
				else:
					playlist+=nwav
					playlist.export(out_path+str(out_count)+'.wav',format='wav')
			else:#正常情况
				test_t=time_total+st
				if(test_t>=tl):
					playlist.export(out_path+str(out_count)+'.wav',format='wav')
					out_count+=1
					playlist=nwav
					time_total=st
				else:
					playlist+=nwav
					time_total+=st
	else:
		for i in range(len(pth_list)):
			nwav=AudioSegment.from_wav(pth_list[i])
			if(i==0):#如果是第一个文件
				playlist=nwav
			elif(i==len(pth_list)-1):#如果是最后一个文件
				playlist+=nwav
				playlist.export(out_path+str(out_count)+'.wav',format='wav')
			else:#正常情况
				playlist+=nwav
	return 1


def dir2list(pth):#将文件夹下文件路径转换为列表，并且添加中间路径
	flist = sorted(os.listdir(pth),key = lambda x:int(x[:-4]))
	flist_n=[]
	for i in flist:
		flist_n.append(pth.strip('/')+'/'+i)
	return flist_n
