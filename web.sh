#!/bin/bash
clear
DIR=$(cd $(dirname $0) && pwd )
ip=$(cat $DIR\/config.ini |grep ip  | grep -Eo '([0-9]*\.){3}[0-9]*')

if [ x$1 != x ]
then
echo 'Copy the datafile' $1 ' to '$DIR\/treegrid\/
eval cp $1 $DIR\/treegrid\/

echo "Open the web:"
echo "http://"$ip":8000/?file="$1  
echo "or"
echo "http://"$ip":8000/energytreegrid.html?file="$1
echo "http://"$ip":8000/perftreegrid.html?file="$1
echo '-------------------------------------------'

else
    #no args...
echo "You can also run:" $0 "datafilename"
echo "Open the web:"
echo "http://"$ip":8000"
echo '-------------------------------------------'
fi
#echo cd $DIR\/treegrid
eval cd $DIR\/treegrid

echo "Press CTRL+C to exit." 

python_version=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`

if [ $python_version -eq 2 ]
then
	python -m SimpleHTTPServer
else
	python -m http.server  # > /dev/null 2>&1
fi





