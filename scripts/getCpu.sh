#!/bin/bash
CPU=`top -b -d1 -n1|grep -i "Cpu(s)"| awk '{print $5}' |cut -d '%' -f1`
echo "100 - $CPU"   | bc
