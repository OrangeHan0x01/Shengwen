# -*- coding: utf-8 -*-
from moviepy.editor import *

def video_cutaudio(video_path='my_video.mp4',audio_path='my_audio.mp3',out_path='无声音.mp4'):
	video = VideoFileClip(video_path)
	videoduration=video.duration
	video.audio.write_audiofile(audio_path)#写入音频
	if out_path:
		video = video.without_audio()  #删除声音，返回新的视频对象，原有对象不更改
		video.write_videofile(out_path)
	print('[+]Successfully cut audio for: '+video_path)
	return videoduration

def video_addaudio(video_path='无声音.mp4',audio_path='my_audio.mp3',new_video='new_video.mp4'):
	video = VideoFileClip(video_path)
	videoduration=video.duration
	audio_clip = AudioFileClip(audio_path)
	video = video.set_audio(audio_clip)
	video.write_videofile(new_video)
	return videoduration

def video_cut(file_path, file_path_save, start = 0, end = None):#用于裁剪视频
	video_data = VideoFileClip(file_path)
	videoduration=video_data.duration
	video_new = video_data.subclip(start, end)
	video_new.write_videofile(file_path_save)
	video_data.reader.close()
	return videoduration

def get_duration(video_path):#用于获取视频时长
	video = VideoFileClip(video_path)
	videoduration=video.duration
	return videoduration
 
