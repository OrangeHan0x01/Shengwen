# -*- coding: utf-8 -*-
#生成一个index_list.txt文件描述每个音频文件的开始时间，方便网页显示
import wave
import os

def indexlist(dir_path,fn_list):#dirpath即此文件输出路径，可以带上/，fn_list可以用audio_splice中的dir2list方法生成，不要是同一个文件夹不然合并会出问题，index_list可以放在test_output中，这是一个中间文件夹，此外fn_list不只是文件名，是带路径的
	point_t=0
	filename=dir_path.strip('/')+'/'+'index_list.txt'
	if not os.path.isfile(filename):  # 无文件时创建
		fout = open(filename, mode="w", encoding="utf-8")
	else:#删除源文件
		os.remove(filename)
		fout = open(filename, mode="w", encoding="utf-8")
	for i in fn_list:
		f=wave.open(i)
		SampleRate = f.getframerate()
		frames = f.getnframes()
		Duration = frames / float(SampleRate)  # 单位为s，音频时间
		Duration=float('%.2f' %Duration)#保留2位小数
#fout写入格式为        当前文件名,开始时间,持续时间     ，之后把持续时间加入开始时间
		f.close()
		fout.write(i+','+str(point_t)+','+str(Duration))
		fout.write('\n')
		point_t+=Duration
		point_t=float('%.2f' %point_t)
	fout.write(str(point_t))#最后一行是总时长
	fout.close()
	return point_t#返回point_t作为总计时长
