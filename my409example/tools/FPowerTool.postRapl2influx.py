# coding=utf-8

import os

import subprocess
import time,sys
import linecache

from threading import Thread



def postRapl2influx(argv):
	print('rapl文件名：'+argv[0])
	raplpath=argv[0]
	print('读取rapllog: '+raplpath)
	raplData=linecache.getlines(raplpath)
	#i, 1~ len-1， 0行是空的 第1行是0 begin,回头把这个删了
	count=0
	file=0
	#fw = open(argv[0]+".influxdata.",'w')
	filenamepre=raplpath+".influxdata."
	for m in raplData:
		#1534238755602965 p0=43823242 p1=22216796 d0=8438110 d1=3021240
		#power,type=cpu0 value=1 time…
		tmp=m.strip().split(' ')
		if len(tmp)==2:
			continue
		if count==0:
			fw = open(filenamepre+str(file),'w')
			#print('打开文件'+filenamepre+str(file))
		fw.writelines(['cpu0 value=',tmp[1].split('=')[1],' ',tmp[0],'000\n'])
		fw.writelines(['cpu1 value=',tmp[2].split('=')[1],' ',tmp[0],'000\n'])
		fw.writelines(['dram0 value=',tmp[3].split('=')[1],' ',tmp[0],'000\n'])
		fw.writelines(['dram1 value=',tmp[4].split('=')[1],' ',tmp[0],'000\n'])
		count+=1
		if count==1250:  #5k行一输出，多了可能存不上
			fw.close()
			cmdouput=subprocess.getoutput("curl -i -XPOST 'http://115.25.138.209:8086/write?db=powertest' --data-binary @"+filenamepre+str(file))
			#print(cmdouput)
			if cmdouput.find('204 No Content')<1:
				print ('Error write influx!!!!!!!!not 204=== ')
			file+=1
			count=0
			
	if os.path.exists(filenamepre+str(file)):
		cmdouput=subprocess.getoutput("curl -i -XPOST 'http://115.25.138.209:8086/write?db=powertest' --data-binary @"+filenamepre+str(file))
		#print(cmdouput)
		if cmdouput.find('204 No Content')<1:
			print ('Error write influx!!!!!!!!not 204=== ')
	if fw.close !=True:
		fw.close()
	#删掉临时文件
	subprocess.getoutput("rm -fr "+filenamepre+"*")



if __name__ == '__main__':
	print('arg1:rapl data. \n参数1：rapl文件名' )
	postRapl2influx(sys.argv[1:])
