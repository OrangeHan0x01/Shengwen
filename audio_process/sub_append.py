# -*- coding: utf-8 -*-
from os.path import splitext
from moviepy.editor import (VideoFileClip,TextClip,CompositeVideoClip)

#一个合成方法，生成字幕文件建议使用savetool
def sub_append(fpath,sub_path,usefont='./font/STXIHEI.TTF',usefontsize=22,usecolor='red',usebottom_position=100):#输入参数：视频文件路径，字幕文件路径
	src_video = fpath
	sentences = sub_path
	video = VideoFileClip(src_video)
	w,h=video.w,video.h
	txts = []
	flag_p = 1
	with open(sentences,encoding='utf8') as fp:
		for line in fp:
			sentence,start,span = line.split('& ')
			start,span=map(float,(start,span))
			try:
				txt = (TextClip(sentence,fontsize=usefontsize,font=usefont,size=(w-20,40),align='center',color=usecolor).set_position((10,h-usebottom_position)).set_duration(span).set_start(start))
				if(flag_p):
					print('使用字体为：'+usefont)
					flag_p = 0
			#首先考虑本地字体文件，没有则尝试linux自带的字体，但是这个字体不支持中文，建议修改
			except:
				txt = (TextClip(sentence,fontsize=usefontsize,font='AR-PL-UMing-CN',size=(w-20,40),align='center',color=usecolor).set_position((10,h-usebottom_position)).set_duration(span).set_start(start))
				if(flag_p):
					print('使用体为：'+'AR-PL-UMing-CN')
					flag_p = 0
			txts.append(txt)
	video = CompositeVideoClip([video,*txts])
	fn,ext = splitext(src_video)
	video.write_videofile(f'{fn}_withsub{ext}')


