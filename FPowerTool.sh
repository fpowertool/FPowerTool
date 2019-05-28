#!/bin/bash

if [ x$1 != x ]
then
echo "start rapl measuring"
stap -v /home/gwei/rapl4stap/raplpapi.stp -c "likwid-pin -c 2  /home/gwei/rapl4stap/raplpapi" > rapl.log &

sleep 3

s1=$1
s0="stap -v batch.stp 'process("
s2=")'  -o fptfun.log &"

echo $s0\"$s1\"$s2
eval  $s0\"$s1\"$s2

echo "run your app..."
sleep 2	
date +%s_%N >fpt.t1 &&  $*  &&date +%s_%N >fpt.t2

sleep 4
echo "stop fpowertool..."
ps -efww|grep -w 'raplpapi'|grep -v grep|cut -c 9-15|xargs kill -9
sleep 2
ps -efww|grep -w 'stapio'|grep -v grep|cut -c 9-15|xargs kill -9


else
    #...没有参数
    echo "usesage: sh FPowerTool.sh runyourapp"
    echo "eg: sh FPowerTool.sh /home/gwei/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc/bin/bodytrack sequenceB_2 4 2 2000 5 0 1 "
fi