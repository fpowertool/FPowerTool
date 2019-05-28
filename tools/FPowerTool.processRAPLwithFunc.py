#coding=utf-8
'''
处理结果，计算函数的能耗

函数时间信息
1534238761646464 1 __libc_csu_init
1534238761646475 1 _init
1534238761646478 -1 _init
1534238761646480 1 frame_dummy
1534238761646483 1 register_tm_clones
1534238761646485 -1 register_tm_clones
1534238761646487 -1 frame_dummy

power数据
0 begin-------
1534238755592090 p0=22766113 p1=21606445 d0=2990722 d1=3036499
1534238755593453 p0=21789550 p1=23132324 d0=4180908 d1=4180908
'''

import time
import linecache
import sys

def main(argv): #argv[1]
	print '参数1是函数时间信息的文件名，2是rapl数据',argv[0],argv[1]
	funSumPowerList=[]
	funPowerList=[]
	treegriddataList=[]
	
	funTimeData=linecache.getlines(argv[0])
	raplData=linecache.getlines(argv[1])
	print len(raplData)
	#lenfunTimeData=len(funTimeData)
	index=0
	for i in range( 1,(len(funTimeData)+1) ):
		#i, 1~ len-1， 0行是空的
		tmpline=linecache.getline(argv[0],i)
		
		tmpline=tmpline.strip()
		ft1=ft2=0
		if tmpline.split(' ')[1]=='1':
			print(i,tmpline)
			
			ft1=int(tmpline.split(' ')[0])
			funname=tmpline.split(' ')[2]
			tmp=0
			#linecache里没第0行，所以这里的行数要注意下，for里是有第0行的
			for j in funTimeData:
				if tmp<=(i-1) or j.split(' ')[1]=='1':
					tmp=tmp+1
					continue
				if j.split(' ')[2].strip()== funname:
					ft2=int(j.split(' ')[0])
					print j
					break
			pt11=pt12=pt21=pt22=0
			tmptime1=tmptime2=0
			for k in raplData:
				tmptime2=int(k.split(' ')[0])
				if ft1>=tmptime1 and ft1<=tmptime2:
					pt11=tmptime1
					pt12=tmptime2
				if ft2>=tmptime1 and ft2<=tmptime2:
					pt21=tmptime1
					pt22=tmptime2
					break
				tmptime1=int(k.split(' ')[0])
			print ft1,ft2,funname,pt11,pt12,pt21,pt22
			#计算i行函数的能耗
			p0=p1=d0=d1=0.0
			if(pt11==pt21 and pt12==pt22):
				for m in raplData:
					tmpt=int(m.split(' ')[0])
					#1534238755593453 p0=21789550 p1=23132324 d0=4180908 d1=4180908
					if tmpt==pt22:
						tmpdata=pdataconvert(m.strip())
						#print m
						p0=tmpdata[0]*1.0*(ft2-ft1)/(pt22-pt21)
						p1=tmpdata[1]*1.0*(ft2-ft1)/(pt22-pt21)
						d0=tmpdata[2]*1.0*(ft2-ft1)/(pt22-pt21)
						d1=tmpdata[3]*1.0*(ft2-ft1)/(pt22-pt21)
						break
			else:
				tmptime1=tmptime2=0
				for m in raplData:
					tmpt=int(m.split(' ')[0])
					if tmpt==pt12:
						#print m
						tmpdata=pdataconvert(m.strip())
						p0=tmpdata[0]*1.0*(pt12-ft1)/(pt12-pt11)
						p1=tmpdata[1]*1.0*(pt12-ft1)/(pt12-pt11)
						d0=tmpdata[2]*1.0*(pt12-ft1)/(pt12-pt11)
						d1=tmpdata[3]*1.0*(pt12-ft1)/(pt12-pt11)
						continue
					if tmpt>pt12 and tmpt<pt21:
						#print m
						tmpdata=pdataconvert(m.strip())
						p0+=tmpdata[0]*1.0
						p1+=tmpdata[1]*1.0
						d0+=tmpdata[2]*1.0
						d1+=tmpdata[3]*1.0
						continue
					if tmpt==pt22:
						#print m
						tmpdata=pdataconvert(m.strip())
						p0+=tmpdata[0]*1.0*(ft2-pt21)/(pt22-pt21)
						p1+=tmpdata[1]*1.0*(ft2-pt21)/(pt22-pt21)
						d0+=tmpdata[2]*1.0*(ft2-pt21)/(pt22-pt21)
						d1+=tmpdata[3]*1.0*(ft2-pt21)/(pt22-pt21)
						break
			#函数的能耗 或者在这里追加到一个文件，次数也是很多的
			#funPowerList.append([funname,p0,p1,d0,d1])
			print funname,p0,p1,d0,d1
			funPowerList.append([str(ft1),str(ft2),funname,str(p0),str(p1),str(d0),str(d1)])
			#treegriddataList
			#treegriddataList.append()
			#print funPowerList

	print '生成treegrid data'
	'''
	name_age={"da_wang":27,"liu":26,"kong":12}用dict表示刚好,但注意dict中是单引号
	
	{"id":11,"name":"fun1","power":"111,1111,2222,333","_parentId":0},
	{"id":0,"name":"functions"},
	{"id":11,"region":"Albin","f1":2000,"f2":1800,"f3":1903,"f4":2183,"f5":2133,"f6":1923,"f7":2018,"f8":1838,"_parentId":1},
	{"id":2,"region":"Washington"},
	{"id":21,"region":"Bellingham","f1":2000,"f2":1800,"f3":1903,"f4":2183,"f5":2133,"f6":1923,"f7":2018,"f8":1838,"_parentId":2},
	{"id":24,"region":"Monroe","f1":2000,"f2":1800,"f3":1903,"f4":2183,"f5":2133,"f6":1923,"f7":2018,"f8":1838,"_parentId":2}
	],"footer":[
	{"region":"Total","f1":14000,"f2":12600,"f3":13321,"f4":15281,"f5":14931,"f6":13461,"f7":14126,"f8":12866}
]}
	'''
	#filename=argv[2]+".treegrid"+str(currenttime.tm_mon)+str(currenttime.tm_mday)+str(currenttime.tm_hour)+str(currenttime.tm_min)
	filename='treegriddata'
	fw = open( filename,'w')
	fw.writelines(['''{"total":'''+str(len(funPowerList))+''',"rows":['''])
	fw.writelines(['\n'])
	
	funPowerList2=funPowerList
	for i,v in enumerate(funPowerList):
		parentID=0
		print i,v #i从0开始
		#[time1,time2,funname,p0,p1,d0,d1]
		ftime1=int(v[0])
		ftime2=int(v[1])
		#for i2,v2 in enumerate(funPowerList[(i+1):]): # i2也是从0开始，这样就不知道行数了
		for i2,v2 in enumerate(funPowerList):
			ftime3=int(v2[0])
			ftime4=int(v2[1])
			if ftime3<ftime1 and ftime2<ftime4:
				parentID=i2+1
				continue
			if ftime2<ftime3:
				break
		if parentID!=0:
			#string='''{'id':'''+ str(i+1)+ ''','name':'''+v[2]+''','p0':'''+i[3]+''','p1':'''+i[4]+''','d0':'''+i[5]+''','d1':'''+i[6]+''','_parentId':'''+str(parentID)+'}'
			#fw.writelines([str({'id':i+1,'name':v[2],'p0':i[3],'p1':i[4],'d0':i[5],'d1':i[6],'_parentId':parentID})])
			#tmpdict={'id':(i+1),'name':v[2],'p0':v[3],'p1':v[4],'d0':v[5],'d1':v[6],'_parentId':parentID}
			tmpdict={'id':(i+1),'name':v[2],'p0':round(float(v[3])),'p1':round(float(v[4])),'d0':round(float(v[5])),'d1':round(float(v[6])),'_parentId':parentID}
		else:
			tmpdict={'id':(i+1),'name':v[2],'p0':round(float(v[3])),'p1':round(float(v[4])),'d0':round(float(v[5])),'d1':round(float(v[6]))}
		#.replace('\'','"')单引号的json格式不识别，应该为双引号
		fw.writelines([str(tmpdict).replace('\'','"'),'\n']) 
		if i+1 != len(funPowerList):
			fw.writelines([','])
		#treegriddataList.append()
	fw.writelines([']}'])
	fw.close()

def pdataconvert(p):
	print p
	#p0=21789550 p1=23132324 d0=4180908 d1=4180908
	tmp=p.split(' ')
	return [int(tmp[1].split('=')[1]),int(tmp[2].split('=')[1]),int(tmp[3].split('=')[1]),int(tmp[4].split('=')[1])]



if __name__ == "__main__":
	print "arg1: function info file. arg2: rapl data. "
	main(sys.argv[1:]) #参数0是文件名，不传入下面的函数

	
 