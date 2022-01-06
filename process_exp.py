# -*- coding: utf-8 -*-
from __future__ import print_function
#这个文件是数据处理示例
#需要提前准备一个文件夹，将视频放在/test_videos下
#句子分割的输出会在新产生的save_audio文件夹中
#导入时直接导入audio_process即可，这里是为了让使用的函数更清晰
import os
from audio_process.audio_extract import video_cutaudio as vc
from audio_process.audio_extract import video_addaudio as va
from audio_process.voice_extract import voice_extract,mp3towav,pth_get
import audio_process.speech_segmentation as seg
import audio_process.audio_splice as audio_splice
import audio_process.indexlist as indexlist
import audio_process.savetool as st
import audio_process.baiduSR as SR
from audio_process.tts_make import tts as tts
import audio_process.red_time
import audio_process.speedchange
import audio_process.sub_append
import shutil
import time

in_pth='test_videos/整篇幅4.mp4'#输入路径，也将会是最后视频的输出路径，不同格式的视频也只需要改动文件名。
out_pth='test_output/'#中间文件保存路径
audio_pth='save_audio/'#中间的分段可识别音频保存路径

#moviepy能处理多种视频格式，如果你不放心，可以使用下面这两条已经被注释的语句，其中绝对路径如果不知道可以用pth_get(相对路径)生成：
#to_mp4='ffmpeg -i ' + 视频文件绝对路径 +' ' + '生成文件的绝对路径'
#os.system(to_mp4)

#先创建文件夹（如果需要从不同用户上传并分开保存下载就要用到，单机可以不用）
isExists=os.path.exists(out_pth.rstrip('/'))
if not isExists:
	os.makedirs(out_pth)
isExists=os.path.exists(audio_pth.rstrip('/'))
if not isExists:
	os.makedirs(audio_pth)
#第一步：提取视频语音
videodura=vc(in_pth,out_pth+'pre1.mp3','test_output/无声音.mp4')#第三个参数为空字符时不输出视频，为路径时输出静音视频
print(videodura)#输出视频长度
#第二步：语音提取降噪
mp3towav(out_pth+'pre1.mp3','test_output/pre1.wav')#输入需要wav文件，mp3不行
#voice_extract(out_pth+'pre1.wav',out_pth+'ve')#函数内部的pth_get是因为这里用命令行需要输入绝对路径，这一步只做示例，实际使用时只有较大噪音时有必要

#第三步：句子分割，以下参数不用改，sr是采样率不能改不然无法正常识别
frame_size = 256
frame_shift = 128
sr = 16000
seg_point = seg.multi_segmentation("./test_output/pre1.wav", sr, frame_size, frame_shift, save_dir=audio_pth,cluster_method='bic')#进行语音分割，默认音频提取到save_audio文件夹，平台多用户时建议存储到不同以uid命名的文件夹

#将语音拼接到接近15s，预备之后用百度api语音识别（准确率更高，但是效率会降低，在不安装语言模型的情况下也能有高准确率）之后生成index_list文件，为之后生成字幕文件做准备
alist = audio_splice.dir2list(audio_pth)
audio_splice.audio_combine(alist,'spliced_audio/',tl=10)#这个文件夹会自动检测创建，这个函数不需要返回值
shutil.rmtree(audio_pth)#如果用户需要再调节，尝试不同的阈值，就不应该现在用这个函数删除文件夹
alist = audio_splice.dir2list('spliced_audio/')
indexlist.indexlist('test_output/',alist)#注意，indexlist生成的音频开始时间和持续时间均为保留两位小数

#使用百度语音api识别，同时生成字幕文件
SRmodel=SR.BaiduSR()#如果是使用离线模型识别，去掉
stool=st.savetool(out_pth+'subtitle.txt')#初始化存储工具对象，并指定文件存储目标，如果已有该文件，则内容会覆盖
try:
	rtool=st.readtool('test_output/index_list.txt')
except:
	print('没有index_list.txt文件，请先使用indexlist方法进行生成')

for item in alist:
	netsuccess = 0
	wtsuccess = 0
	rret=rtool.read(item)#读出对应音频的[t_start,t_keep]
	while(not(netsuccess and wtsuccess)):#只有当网络与并发限制都通过，状态为1时才结束识别，在网站使用时建议增加一个变量作为互斥量
		try:
			print('开始识别文件：',item)
			out_json =SRmodel.rec(file=item,outf='')#outf参数为空，则不记录到单独的文件中
			netsuccess = 1#代表成功收到json，但是json是否符合格式在savetool中进行判断
		except:
			print('网络错误')
			netsuccess = 0
		try:
			stool.api_save(out_json,t_start=rret[0],t_keep=rret[1])#api_save的返回值1或0代表调用是否成功
			wtsuccess = 1
		except:
			wtsuccess = 0
		print(netsuccess,wtsuccess)
		time.sleep(1)
#如果使用masr识别，只需要去除网络与并发的逻辑判断，保留rtool的相关函数，将api_save替换为str_save函数并输入masr的识别结果即可。
stool.close()
while(1):
	ifbreak=input('现在你可以修改你test_output目录下的字幕文件subtitle.txt，修改完毕并确保为utf-8编码格式后请输入continue:')
	if(ifbreak=='continue'):
		break
#生成一段tts合成语音，并用其进行变速，代替其中一段语音，这里选择替代8.wav，改为“非常容易理解”
#此外，也可以使用录音来进行替代，只要有符合对应采样率、采样位数、编码格式的wav文件即可，audio_process/audio_record.py是一个命令行工具，可以输入时间和输出路径参数用其进行录音
#如果要保证语音音色足够自然且与原本语音一致，建议使用重录音的方法，但必须尽可能使其在变换后时长与原语音一致，否则之后的语音和语音都会无法对齐，因此也应当尽可能少地做修改

tts('非常容易理解',out=out_pth+'test.mp3',rate=200,volume=1)#原语音吐字较快，因此这里也先使用较快的200字/分钟速率
mp3towav(out_pth+'test.mp3','test_output/test.wav')

#变速提供了4种方式：tts变速（语音合成时调整说话速度），ffmpeg变速，语音裁剪，语音末尾添加空白。可以根据需求使用，但是目前只建议对时间相差不大的tts语音进行变速以及添加空白，以使其相对更自然，自己上传的语音可以使用手动的裁剪
#方法2，ffmpeg变速，一步到位生成，但是语音可能会有些不自然，而且可能会有0.01-0.03秒的时间差异
audio_process.speedchange.speed_variety('spliced_audio/8.wav','test_output/test.wav')

#方法4，添加空白,之后用我们生成的test_output/test.wav代替spliced_audio/8.wav（前提是test.wav的时长<8.wav的时长）
#audio_process.red_time.red_time('test_output/test.wav', audio_process.red_time.get_time('spliced_audio/8.wav'),'test_output/middle_red.wav')
#audio_process.speedchange.audio_replace('spliced_audio/8.wav','test_output/test.wav')
#replaced_audio='spliced_audio/8.wav'#也可以考虑只把拼接只作为语音识别的手段，不删除save_audio中原本的数据，再在这里进行替换，但这样容易造成新语音比原语音长的情况，只能用变速或裁剪
#注意：由于字幕文件生成封装好的方式是总体生成，需要将生成的tts的文字修改到字幕文件中时建议：由于行号对应文件名，可以在tts时修改的文件名同时传入并取同一行来修改文件中的文字
#如果只是改文字不改语音，就不需要前面的内容，直接写这句即可
#st.changeline(out_pth+'subtitle.txt',int(replaced_audio.split('/')[-1][:-4]),'非常容易理解')
#合成所有语音，准备合成到视频中
audio_splice.audio_combine(alist,'final_audio/',tl=0)#注意/号不可以缺少
#合成到视频
va('test_output/无声音.mp4','final_audio/0.wav','test_videos/整篇幅4_改动.mp4')
#合成字幕文件到视频
audio_process.sub_append.sub_append('test_videos/整篇幅4_改动.mp4',out_pth+'subtitle.txt',usefont='./font/STXIHEI.TTF',usefontsize=20,usecolor='red',usebottom_position=100)#要合成的视频,字幕文件，之后跟着的是使用的可选参数的默认值（可以自己修改），最后生成的文件名为集合概述_改动_withsub.mp4，和合成用的视频在同一文件夹下
#删除中间文件夹
#shutil.rmtree(out_pth)
#shutil.rmtree('spliced_audio')测试时别打开
