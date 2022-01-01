# -*- coding: utf-8 -*-
from __future__ import print_function
import os
from audio_process.audio_extract import video_cutaudio as vc
from audio_process.voice_extract import mp3towav
import audio_process.speech_segmentation as seg
import audio_process.audio_splice as audio_splice
import audio_process.indexlist as indexlist
import audio_process.savetool as st
import audio_process.pdrec as pd
import audio_process.red_time
import audio_process.sub_append
import shutil

in_pth='test_videos/整篇幅4.mp4'#输入路径，也将会是最后视频的输出路径，不同格式的视频也只需要改动文件名。
out_pth='test_output/'#中间文件保存路径
audio_pth='save_audio/'#中间的分段可识别音频保存路径
out_video='test_videos/整篇幅4.mp4'

isExists=os.path.exists(out_pth.rstrip('/'))
if not isExists:
	os.makedirs(out_pth)
isExists=os.path.exists(audio_pth.rstrip('/'))
if not isExists:
	os.makedirs(audio_pth)
videodura=vc(in_pth,out_pth+'pre1.mp3','test_output/无声音.mp4')#第三个参数为空字符时不输出视频，为路径时输出静音视频
print('Video duration: ',videodura)#输出视频长度
mp3towav(out_pth+'pre1.mp3',out_pth+'pre1.wav')#输入需要wav文件，mp3不行
frame_size = 256
frame_shift = 128
sr = 16000
seg_point = seg.multi_segmentation('./'+out_pth+'pre1.wav', sr, frame_size, frame_shift, save_dir=audio_pth,cluster_method='bic')
alist = audio_splice.dir2list(audio_pth)
audio_splice.audio_combine(alist,'spliced_audio/',tl=10)#这个文件夹会自动检测创建，这个函数不需要返回值
shutil.rmtree(audio_pth)#如果用户需要再调节，尝试不同的阈值，就不应该现在用这个函数删除文件夹
alist = audio_splice.dir2list('spliced_audio/')
indexlist.indexlist(out_pth,alist)#注意，indexlist生成的音频开始时间和持续时间均为保留两位小数
stool=st.savetool(out_pth+'subtitle.txt')#初始化存储工具对象，并指定文件存储目标，如果已有该文件，则内容会覆盖
rtool=st.readtool(out_pth+'index_list.txt')

for item in alist:
	rret=rtool.read(item)#读出对应音频的[t_start,t_keep]
	print('开始识别文件：',item)
	recresult =pd.pd_asr(file=item)#如果要英译中，换成pd_st即可
	stool.str_save(recresult,t_start=rret[0],t_keep=rret[1])#api_save的返回值1或0代表调用是否成功
stool.close()

while(1):
	ifbreak=input('现在你可以修改你test_output目录下的字幕文件subtitle.txt，修改完毕并确保为utf-8编码格式后请输入continue:')
	if(ifbreak=='continue'):
		break

audio_splice.audio_combine(alist,'final_audio/',tl=0)#注意/号不可以缺少
audio_process.sub_append.sub_append(out_video,out_pth+'subtitle.txt',usecolor='red')