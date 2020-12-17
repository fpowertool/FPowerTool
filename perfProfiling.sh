#!/bin/bash
stapinbg= `ps -ef|grep stap|grep fptfnperf.log` &
if [ "$stapinbg" ]
then
#ps -ef|grep stap|grep fptfnperf.log
#ps -efww|grep -w 'stap'|grep -v grep|cut -c 9-19|xargs kill -9
#ps -efww|grep -w 'stapio'|grep -v grep|cut -c 9-19|xargs kill -9
ps -ef | grep stap | grep -v grep | awk '{print $2}' | xargs kill -9
echo "kill the stap process in background!"

fi

if [ x$1 != x ]
then
s1=$1
s0="stap -v fnperf.stp 'process("
s2=")'  -o fptfnperf.log  &"

echo $s0\"$s1\"$s2
eval  $s0\"$s1\"$s2
sleep 6 
echo "Start run your app..."
sleep 1	
#date +%s_%N >fptperfprofiling.t1 &&  $*  &&date +%s_%N >fptperfprofiling.t2
date +%s_%N >>timep.log && likwid-pin -c 22  $*  && date +%s_%N >>timep.log
#date +%s_%N >>timep.log &&   $*  && date +%s_%N >>timep.log

sleep 3 
echo "stop systemtap..."
#using > /dev/null 2>&1 will redirect all your command output (both stdout and stderr ) to /dev/null 
#not good:ps -efww|grep -w 'stapio'|grep -v grep|cut -c 9-19|xargs kill -9 > /dev/null 
ps -ef | grep stap | grep -v grep | awk '{print $2}' | xargs kill -9
sleep 2
echo 'rm all stap module...'
lsmod | grep stap | grep -v grep | awk '{print $1}' |xargs rmmod

# 2>&1
sleep 1

echo 'Result is saved in fptfnperf.log. now process Perf data in fptfnperf.log'

DIR=$(cd $(dirname $0) && pwd )
echo python $DIR\/tools/processPerfdata2kexue.py fptfnperf.log
eval python $DIR\/tools/processPerfdata2kexue.py fptfnperf.log

else
    #no args...
    echo "usesage: sh yourpath/perfProfiling.sh" "runyourapp"
    echo "note: use the absolute pathname or full path."
    echo "eg: sh /root/fpowertool/perfProfiling.sh" "/home/gwei/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc/bin/bodytrack sequenceB_2 4 2 2000 5 0 1 "
fi
