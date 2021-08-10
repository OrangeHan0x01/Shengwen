# -*- coding: utf-8 -*-
import contextlib
import os
import struct
import wave
import numpy as np
from pydub import AudioSegment

def get_time(origin_wav):#获得源文件时间长度
    with contextlib.closing(wave.open(origin_wav, 'rb')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

def red_time(path_wav, time,middle_path):#输入：需要修改的音频路径，要修改到的时间（请确保比原时间长，不然不会修改），中间产生的空白语音的保存路径
    with contextlib.closing(wave.open(path_wav, 'rb')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
# 判断当时语音长度
        if time > round(duration, 2):#保留2位小数
            durations = round(time - round(duration, 2), 2)#这个是与时间的差
            creata_wav(durations, path_wav, middle_path)

def creata_wav(durations=None, path_wav=None, out=None):#out是保存中间空白音频的位置，之后删除即可
    framerate = 16000
    sample_width = 2
    duration = durations
    frequency = 2000
    volume = 1000
    x = np.linspace(0, duration, num=int(duration * framerate))
    y = np.sin(0 * np.pi * frequency * x) * volume
    sine_wave = y
    sine = out
    with wave.open(sine, 'wb') as wf:
        wf.setnchannels(1)
        wf.setframerate(framerate)
        wf.setsampwidth(sample_width)
        for i in sine_wave:
            data = struct.pack('<h', int(i))
            wf.writeframesraw(data)
        wf.close()
    red_wav(path_wav, sine)

def red_wav(path_wav, sine):#data2是放在后面的，也就是空白音频，前面是正常音频，现在考虑使用AudioSegment来合成
	owav=AudioSegment.from_wav(path_wav)+AudioSegment.from_wav(sine)
	os.remove(path_wav)
	owav.export(path_wav,format='wav')
