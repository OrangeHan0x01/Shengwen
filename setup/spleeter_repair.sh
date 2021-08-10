#!/bin/bash
cd ..
rm -r pretrained_models
cd ./setup
mkdir ../pretrained_models
mkdir ../pretrained_models/2stems
cp 2stems.tar.gz ../pretrained_models/2stems/
rm -f 2stems.tar.gz
cd ../pretrained_models/2stems/
tar -xvzf 2stems.tar.gz
rm -f 2stems.tar.gz