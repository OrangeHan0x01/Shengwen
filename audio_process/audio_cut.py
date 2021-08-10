# -*- coding: utf-8 -*-
from pydub import AudioSegment

def audio_cut(input_path,out_path,start=0,end=0):#start、end以毫秒为单位，输入0表示设置成空，比如开始为空表示开始的全截取直到end，wav格式
    input_music = AudioSegment.from_wav(input_path) # 加载wav音频
    if(start and end):
        output_music = input_music[start:end]
    elif(start):
        output_music = input_music[start:]
    elif(end):
        output_music = input_music[:end]
    else:
        output_music = input_music
    output_music.export(out_path, format="wav")#注意：输出后的文件似乎是被占用的，需要退出程序才能使用