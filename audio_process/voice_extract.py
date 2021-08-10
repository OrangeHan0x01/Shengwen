# -*- coding: utf-8 -*-
#Python -m spleeter separate -i 你要处理的文件的绝对路径 -p spleeter:2stems -o 你要获得的结果文件的文件夹路径
import os
import shutil
def pth_get(input_path):#用于获取绝对路径
	print(os.path.abspath(input_path))
	return os.path.abspath(input_path)

def mp3towav(input_path,output_path):#绝对路径
	exestr='ffmpeg -i '
	exestr+=pth_get(input_path)
	exestr+=' -ar 16000 -ac 1 -acodec pcm_s16le '
	exestr+=pth_get(output_path)
	ret = os.system(exestr)
	return ret

def voice_extract(input_path,output_path):#注意输入绝对路径，output_path应该是一个新的单独文件夹
	exestr='spleeter separate'
	exestr+=' -i '
	exestr+=pth_get(input_path)
	exestr+=' -p spleeter:2stems -o '
	exestr+=pth_get(output_path)
	ret = os.system(exestr)
	fname=input_path.split('/')[-1].split('.')[0]
	os.remove(pth_get(input_path))
	mp3towav(output_path+'/'+fname+'/vocals.wav',output_path+'/vocals_new.wav')
	shutil.move(output_path+'/vocals_new.wav',input_path)
	shutil.rmtree(output_path+'/'+fname)
	return ret
