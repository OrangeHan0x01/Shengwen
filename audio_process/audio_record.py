# -*- coding: utf-8 -*-
#解决方案是，使用masr的record，用pyinstaller编译为exe格式文件来录制音频
import pyaudio
import wave
import argparse

parser = argparse.ArgumentParser(description="使用方法：")
parser.add_argument("-o","--output_path",help="输出音频wav文件的路径及文件名")
parser.add_argument("-t","--time",help="录制时长，整数")
args = parser.parse_args()
framerate = 16000
NUM_SAMPLES = 2000
channels = 1
sampwidth = 2
TIME = 10


def save_wave_file(filename, data):
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def record(f='record.wav', time1=5):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=framerate,
        input=True,
        frames_per_buffer=NUM_SAMPLES,
    )
    my_buf = []
    count = 0
    print("录音中")
    while count < TIME * time1:
        string_audio_data = stream.read(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        count += 1
        print(".", end="", flush=True)

    save_wave_file(f, my_buf)
    stream.close()


if(args.output_path and args.time):
    record(args.output_path, int(args.time))
elif(args.output_path):
    record(args.output_path,5)
elif(args.time):
    record('record.wav',int(args.time))
else:
    print('缺少参数！请使用 -h参数获取帮助信息')
    exit=input()
