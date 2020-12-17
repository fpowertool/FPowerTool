#coding=utf-8
'''
处理结果，计算函数的perf数据

__libc_csu_init,1,424154,9486,17419,66920,2169581,5080376,6808900,73,3002282,206,2882919 
_init,1,426967,9672,17602,67470,2184141,5110961,6862275,73,3024033,207,2904232 
_init,2,428923,9734,17645,67537,2194276,5125099,6887575,73,3034142,207,2914361 
frame_dummy,1,430726,9784,17676,67592,2203558,5136967,6908600,73,3042625,207,2922789 
register_tm_clones,1,432729,9829,17718,67641,2213856,5150487,6932775,73,3052313,207,2932478 
register_tm_clones,2,434705,9876,17755,67681,2224084,5163829,6956600,73,3061855,207,2942032 
frame_dummy,2,436397,9911,17781,67708,2232898,5173624,6974125,73,3068866,207,2949051 
__libc_csu_init,2,438166,9950,17811,67740,2242092,5184477,6993475,73,3076647,207,2956829 
main,1,440458,9991,17840,67833,2253903,5200462,7022075,73,3088091,209,2968279 
MAIN__,1,543123,13022,18254,83148,2589825,6099292,8628225,73,3731727,215,3612310 


'''

import time
import linecache
import sys

def main(argv): #argv[1]
	#print('参数1是perf数据',argv[0])
	print ("arg1: perf data file ")
	funSumPowerList=[]
	funPerfList=[]
	treegriddataList=[]
	
	perfData=linecache.getlines(argv[0])
	print ('lines:'+str(len(perfData)) )
	parentlinetmp=1

	for i in range( 1,(len(perfData)+1) ):
		#i, 1~ len-1?， 0行是空的
		tmpline=linecache.getline(argv[0],i)
		tmpline=tmpline.strip()
		funname=tmpline.split(',')[0]
		callreturn=tmpline.split(',')[1]
		if callreturn=='2':
			continue
		#print(i)
		#print(tmpline)
		
		#linecache里没第0行，所以这里的行数要注意下，for里是有第0行的
		tmp=0
		chongming=0
		treegridnumber=0
		for j in perfData:
			if tmp<=(i-1) :
				tmp=tmp+1
				continue
			jFunName=j.split(',')[0]
			jcallreturn=j.split(',')[1]

			if	j.split(',')[1]=='1': #不是1就是2啊
					if j.split(',')[0].strip()== funname:
							chongming=chongming+1
					tmp=tmp+1
			elif j.split(',')[0].strip()== funname:
					if chongming==0:
							#找到return行
							#第i行找爹
							zhaodieline=i-1
							no2=0 #有一个2就有一个1
							parentID=-1
							while zhaodieline>=parentlinetmp:
								#print(linecache.getline(argv[0],zhaodieline))
								cORr=linecache.getline(argv[0],zhaodieline).split(',')[1]
								#print(cORr)
								if cORr=='2':
									no2+=1
									zhaodieline=zhaodieline-1
								else:
									if no2!=0:
										no2=no2-1
										zhaodieline=zhaodieline-1
										continue
									else:
										#找到了
										parentID=zhaodieline
										break
							if parentID<0:
								parentlinetmp=i #第i行没有父亲，以后只检查到i
								#@perf("bi"), @perf("bm"), @perf("cm"), @perf("cr"), @perf("ins"), @perf("cc"), @perf("rcc") , @perf("csw") ,  @perf("ccl") ,@perf("pfa") ,  @perf("tcl") 
								tmpdict={'id':(i),'name':funname,'bi':data2kexue(int(j.split(',')[2])-int(tmpline.split(',')[2])),'bm':data2kexue(int(j.split(',')[3])-int(tmpline.split(',')[3])),'cm':data2kexue(int(j.split(',')[4])-int(tmpline.split(',')[4])),\
								'cr':data2kexue(int(j.split(',')[5])-int(tmpline.split(',')[5])),'ins':data2kexue(int(j.split(',')[6])-int(tmpline.split(',')[6])),'cc':data2kexue(int(j.split(',')[7])-int(tmpline.split(',')[7])), 'rcc':data2kexue(int(j.split(',')[8])-int(tmpline.split(',')[8])), \
								'csw':data2kexue(int(j.split(',')[9])-int(tmpline.split(',')[9])), 'ccl':data2kexue(int(j.split(',')[10])-int(tmpline.split(',')[10])), 'pfa':data2kexue(int(j.split(',')[11])-int(tmpline.split(',')[11])),'tcl':data2kexue(int(j.split(',')[12])-int(tmpline.split(',')[12]))\
								}
								
							else:
								tmpdict={'id':(i),'name':funname,'bi':data2kexue(int(j.split(',')[2])-int(tmpline.split(',')[2])),'bm':data2kexue(int(j.split(',')[3])-int(tmpline.split(',')[3])),'cm':data2kexue(int(j.split(',')[4])-int(tmpline.split(',')[4])),\
								'cr':data2kexue(int(j.split(',')[5])-int(tmpline.split(',')[5])),'ins':data2kexue(int(j.split(',')[6])-int(tmpline.split(',')[6])),'cc':data2kexue(int(j.split(',')[7])-int(tmpline.split(',')[7])), 'rcc':data2kexue(int(j.split(',')[8])-int(tmpline.split(',')[8])), \
								'csw':data2kexue(int(j.split(',')[9])-int(tmpline.split(',')[9])), 'ccl':data2kexue(int(j.split(',')[10])-int(tmpline.split(',')[10])), 'pfa':data2kexue(int(j.split(',')[11])-int(tmpline.split(',')[11])),'tcl':data2kexue(int(j.split(',')[12])-int(tmpline.split(',')[12]))\
								,'_parentId':parentID}
							#################tmpline和j间的数据
							funPerfList.append(tmpdict)

							break #结束这个函数的了。
					else:
							chongming=chongming-1
							continue


	currenttime = time.strftime('%Y%m%d.%H%M',time.localtime(time.time()))
	filename='treegridPerfData'+currenttime
	#print("将结果保存到文件,文件名为 treegridPerfData.时间 \n")
	print("Save result to file: "+filename)
	with open( filename,'w') as fw:
		fw.writelines(['''{"total":'''+str(len(perfData))+''',"rows":['''])
		fw.writelines(['\n'])
		k=1
		kk=len(funPerfList)
		for i in funPerfList:
			fw.writelines([str(i).replace('\'','"'),'\n']) 
			if k<kk:
				k=k+1
				fw.writelines([','])
		fw.writelines([']}'])



def data2kexue(t):
	#如果大于1w就用科学计数
	t=t
	if t>=10000:
		return '%.2e'%t
	return str(t)




if __name__ == "__main__":
	main(sys.argv[1:]) #参数0是文件名，不传入下面的函数

