import paddle
from paddlespeech.cli import ASRExecutor
from paddlespeech.cli import STExecutor

def pd_asr(file):
	asr_executor = ASRExecutor()
	text = asr_executor(model='conformer_wenetspeech',lang='zh',sample_rate=16000,config=None,ckpt_path=None,audio_file=file,force_yes=False,device=paddle.get_device())
	return text


def pd_st(file):
	st_executor = STExecutor()
	text = st_executor(model='fat_st_ted',src_lang='en',tgt_lang='zh',sample_rate=16000,config=None,ckpt_path=None,audio_file=file,device=paddle.get_device())
	return text