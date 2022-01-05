#!/bin/bash
sudo apt-get -y install libmagick++-dev
sudo apt-get -y install espeak
sudo apt-get -y install python3-pyaudio
sudo apt-get -y install imagemagick
sudo apt-get -y install ffmpeg
cd ..
python -m pip install paddlepaddle==2.2.1 -i https://mirror.baidu.com/pypi/simple
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
wget http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
tar -xvzf yasm-1.3.0.tar.gz
cd yasm-1.3.0/
./configure
sudo make
sudo make install
cd ../setup
mkdir ../pretrained_models
mkdir ../pretrained_models/2stems
cp 2stems.tar.gz ../pretrained_models/2stems/
rm -f 2stems.tar.gz
cd ../pretrained_models/2stems/
tar -xvzf 2stems.tar.gz
rm -f 2stems.tar.gz


