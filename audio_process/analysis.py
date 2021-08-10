# -*- coding: utf-8 -*-
import wave
#测试用文件，用于测试wav文件的参数
wavFile= '65.wav'
f=wave.open(wavFile)
params = f.getparams()
Channels = f.getnchannels()
SampleRate = f.getframerate()
bit_type = f.getsampwidth() * 8
frames = f.getnframes()
# Duration 也就是音频时长 = 采样点数/采样率 
Duration = wav_time = frames / float(SampleRate)#单位为s

print("音频头参数：", params)
print("通道数(Channels)：", Channels)
print("采样率(SampleRate)：", SampleRate)
print("比特(Precision)：", bit_type)
print("采样点数(frames)：", frames)
print("帧数或者时间(Duration)：", Duration)
