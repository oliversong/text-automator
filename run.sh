#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games

echo "ANALYZE" >> ~/Desktop/hellos
python parse_sms.py > output
python analyzer.py output
#python delete.py
