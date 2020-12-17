# coding=utf-8

import os

import subprocess
import time,sys
import linecache

from threading import Thread



def postTime2influx(argv):
	print('shell的时间戳文件名，不带.t1的：'+argv[0])

	t1=subprocess.getoutput("cat "+argv[0]+".t1")
	t2=subprocess.getoutput("cat "+argv[0]+".t2")
	print(t1)
	print(t2)
	#写annotation
	#curl -i -XPOST 'http://115.25.138.206:3000/write?db=powertest' --data-binary 'cpu_load_short,host=server01,region=us-west value=0.64 1434055562000000000'
	#curl -i POST "http://115.25.138.209:8086/write?db=powertest" --data-binary 'events title="Deployed v1",text="Release note",tags="thesetags" 1534238769115957399'
	annotation1='''curl -X POST 'http://115.25.138.209:8086/write?db=powertest' --data-binary 'events title="'''+argv[1]+'''",text="timestamp before app run",tags="start" '''+t1.replace('_','')+''' ' '''
	annotation2='''curl -X POST 'http://115.25.138.209:8086/write?db=powertest' --data-binary 'events title="'''+argv[1]+'''",text="timestamp after app run",tags="stop" '''+t2.replace('_','')+''' ' '''
	print(annotation1)
	cmdouput=subprocess.getoutput(annotation1)
	if cmdouput.find('error'):
		print (cmdouput)
	cmdouput=subprocess.getoutput(annotation2)
	if cmdouput.find('error'):
		print (cmdouput)
	return


if __name__ == '__main__':
	print('arg1 timestamp file name, without .t1 or .t2\n  arg2:your appname \n参数1：shell的时间戳文件名，不带.t1的. 参数2：appname' )
	postTime2influx(sys.argv[1:])
