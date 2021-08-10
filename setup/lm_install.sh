#!/bin/bash
cd ../masr
mkdir lm/
cd lm
sudo apt-get -y install g++
wget https://deepspeech.bj.bcebos.com/zh_lm/zh_giga.no_cna_cmn.prune01244.klm
cd ..
git clone --recursive https://github.com/parlance/ctcdecode.git
cd ctcdecode
python setup.py install
