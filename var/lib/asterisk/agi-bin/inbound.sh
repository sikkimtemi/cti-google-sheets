#!/bin/bash
nohup /var/lib/asterisk/agi-bin/sub_inbound.py $1 > /dev/null 2>&1 &
