import paddle
from paddlespeech.cli import ASRExecutor
from paddlespeech.cli import STExecutor

def pd_asr(file,tgt_lang='zh'):#中文语音识别
	asr_executor = ASRExecutor()
	if(tgt_lang=='zh'):
		text = asr_executor(model='conformer_wenetspeech',lang=tgt_lang,sample_rate=16000,config=None,ckpt_path=None,audio_file=file,force_yes=False,device=paddle.get_device())
	elif(tgt_lang=='en'):
		text = asr_executor(model='transformer_librispeech',lang=tgt_lang,sample_rate=16000,config=None,ckpt_path=None,audio_file=file,force_yes=False,device=paddle.get_device())
	else:
		text='目前只能识别中文和英文'
	print('识别结果：',text)
	return text


def pd_st(file,srl='en',tgl='zh'):#英文语音翻译
	st_executor = STExecutor()
	text = st_executor(model='fat_st_ted',src_lang=srl,tgt_lang=tgl,sample_rate=16000,config=None,ckpt_path=None,audio_file=file,device=paddle.get_device())
	print('翻译结果：',text)
	return text
