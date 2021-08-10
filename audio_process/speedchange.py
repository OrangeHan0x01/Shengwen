# -*- coding: utf-8 -*-
#1、两位小数的精确度（ffmpeg直接实现）
#2、验证ffmpeg变速后采样率是否变化（测试得不变）
#3、最后小数位可以使用裁剪的方式剪掉一点，不影响状况（应该不用裁剪了）
#4、加入重录制，重录也应该可以采用这套变速
#已知合成时，不需要长度一致但是音频多出视频的长度会丢失
#变速使用pydub和ffmpeg
import wave
import os

def pth_get(input_path):#用于获取绝对路径
	print (os.path.abspath(input_path))
	return os.path.abspath(input_path)

def atp_cal(origin_path,new_path):#计算两个音频文件的时间倍率，输出origin音频时长/new音频时长，并取两位小数,注意只能处理0.5-2倍，超出时告警
	f=wave.open(origin_path)
	SampleRate = f.getframerate()
	frames = f.getnframes()
	time1=frames / float(SampleRate)
	f=wave.open(origin_path)
	SampleRate = f.getframerate()
	frames = f.getnframes()
	time2=frames / float(SampleRate)
	m=time1/time2#倍率为原文件长度/准备用来替代的文件长度，之后speedchange修改用于替代的文件即可
	m=float('%.2f' %m)
	return m
def speedchange(input_path,output_path,multi=1.50):#绝对路径，改变音频长度并输出
	if(multi)>4:
		print('速率倍数过大！建议手动录制')
	if(multi)<0.25:
		print('速率倍数过小！建议手动录制')
	exestr='ffmpeg -i '
	exestr+=pth_get(input_path)
	exestr+=' -filter:a "atempo='
	exestr+=str(multi)
	exestr+='" '
	exestr+=pth_get(output_path)
	ret = os.system(exestr)
	return ret
#ffmpeg -n -i 222.wav -filter:a "atempo=2" output.wav
#注意，变速生成不能覆盖原文件，因此实际是变形的，这里追加一个替代源文件的函数
def audio_replace(origin_file,new_file):#删除原文件，然后给新文件改名,nf='test_1.txt',nf[:-4]='test_1'，nf[-4:]=.txt
	os.remove(origin_file)
	os.rename(new_file,origin_file)

def speed_variety(origin_path,new_path):#封装的方法，一步到位，但如果要手动测试音频状态的话，不应该用封装的方法，用作参考
	smulti=atp_cal(origin_path,new_path)
	out_path=new_path[:-4]+'_sc'+'.wav'
	speedchange(new_path,out_path,multi=smulti)
	os.remove(new_path)#用不到这个文件，删掉
	audio_replace(origin_path,out_path)#代替源文件
	
