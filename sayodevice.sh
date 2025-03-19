#!/usr/bin/env bash
source ~/sb-env/bin/activate
cd /usr/local/lib/sayodevice
node=`hostname`
python3 keypadv2.py -s -c ${node}.json 
