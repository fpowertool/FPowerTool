#!/bin/bash

if [ x$1 != x ]
then

s1=$1
s0="stap -v batch.energy.stp 'process("
s2=")'  -o fptfun.log &"

echo $s0\"$s1\"$s2
eval  $s0\"$s1\"$s2

sleep 3
echo "start rapl measuring"
stap -v /home/gwei/rapl4stap/raplpapi.stp -c "likwid-pin -c 2  /home/gwei/rapl4stap/raplpapi" > rapl.log &


sleep 5	
echo "run your app..."
#date +%s_%N >fpt.t1 &&  $*  &&date +%s_%N >fpt.t2
date +%s_%N >>time2.log 
likwid-pin -c 13-22   $*
date +%s_%N >>time2.log  
  
#date +%s_%N >>time2.log &&    $* && date +%s_%N >>time2.log  

sleep 5 
echo "stop fpowertool..."

ps -ef | grep raplpapi | grep -v grep | awk '{print $2}' | xargs kill -9

sleep 2
ps -ef | grep stap | grep -v grep | awk '{print $2}' | xargs kill -9

sleep 1
echo 'rmmod all stap mod'
lsmod | grep stap | grep -v grep | awk '{print $1}' |xargs rmmod
echo "profiling finished."

DIR=$(cd $(dirname $0) && pwd )
echo  "run 'python $DIR/tools/FPowerTool.processRAPLwithFunc.py fptfun.log rapl.log filenamesaveto' to process the result."


else
    #no args...
    echo "usesage: sh FPowerTool.sh runyourapp"
    echo "eg: sh FPowerTool.sh /home/gwei/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc/bin/bodytrack sequenceB_2 4 2 2000 5 0 1 "
fi
