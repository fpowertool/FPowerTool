#!/bin/bash
#stap -v /home/gwei/FPowerTool/tools/functioncount.stp 'process("/home/gwei/abcdef/abc").function("*")' -c "/home/gwei/abcdef/abc" -o app.funcount
stapinbg=`ps -ef|grep stap` &
if [ "$stapinbg" ]
then
ps -ef|grep stap
echo "kill the stap process in background!"
ps -efww|grep -w 'stap'|grep -v grep|cut -c 9-19|xargs kill -9
fi



if [ x$1 != x ]
then
echo "note: use the absolute/full path of your program"
currentpwd=$(pwd )
DIR=$(cd $(dirname $0) && pwd )

s1="$DIR/tools/functioncount.stp"
a0="stap -v "
a2=" 'process(\""
a3="\").function(\"*\")' -c \""
a4="\" -o app.funcount"
echo $a0$s1$a2$1$a3$*$a4
eval  $a0$s1$a2$1$a3$*$a4

#date +%s_%N >fptperfprofiling.t1 &&  $*  &&date +%s_%N >fptperfprofiling.t2
echo '-------------'
echo 'The run times count of the function run is saved in app.funcount. '
echo 'Check the file app.funcount. An easy way to find the tiny functions is according to the execution time of the program and the running times of the function. '
echo 'Remove the tiny functions for profiling, and reduce the profiling overhead.'
echo  "run 'python $DIR/tools/FPowerTool.genfunctionstp.py app.funcount nubmer' to create function profiling .stp file."
echo "run 'python $DIR/tools/genPerfStp.py app.funcount  number' to create perf profiling .stp file. \nThe fucntions which run times is bigger than the number won't be processed. "
else
echo "run 'sh $0 /fullpath/yourexe args'"
echo "note: use the full path of your program"
fi
