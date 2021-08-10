# -*- coding: utf-8 -*-
import torch
import audio_process.feature as feature
from masr.models.conv import GatedConv
import torch.nn.functional as F
from ctcdecode import CTCBeamDecoder
import configparser as ConfigParser

def getConfig(section, key):
	config = ConfigParser.ConfigParser()
	pathforconfig = './general_config.conf'
	config.read(pathforconfig)
	return config[section][key]

alpha = 0.8
beta = 0.3
lm_path = getConfig('model_path','lm_model')
cutoff_top_n = 40
cutoff_prob = 1.0
beam_width = 32
num_processes = 4
blank_index = 0

model = GatedConv.load(getConfig('model_path','masr_model'))
model.eval()

decoder = CTCBeamDecoder(
    model.vocabulary,
    lm_path,
    alpha,
    beta,
    cutoff_top_n,
    cutoff_prob,
    beam_width,
    num_processes,
    blank_index,
)


def translate(vocab, out, out_len):
    return "".join([vocab[x] for x in out[0:out_len]])


def predict(f):
    wav = feature.load_audio(f)
    spec = feature.spectrogram(wav)
    spec.unsqueeze_(0)
    with torch.no_grad():
        y = model.cnn(spec)
        y = F.softmax(y, 1)
    y_len = torch.tensor([y.size(-1)])
    y = y.permute(0, 2, 1)  # B * T * V
    print("decoding")
    out, score, offset, out_len = decoder.decode(y, y_len)
    return translate(model.vocabulary, out[0][0], out_len[0][0])
