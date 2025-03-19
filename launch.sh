#!/usr/bin/env bash
source PYENV/bin/activate
nm-online
cd /usr/local/lib//sayodevice
node=`hostname`
python3 keypadv2.py -s -c ${node}.json
