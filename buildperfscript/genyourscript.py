# coding=utf-8
'''
perf.hw.cache_misses cache_misses
perf.hw.cache_references cache_references
'''

with open('perfliststapsupport.txt','r') as f:
	lines=f.readlines()
if len( lines)==0:
	print('ERROR! No data in perfliststapsupport.txt')
	exit
a=[]
b=[]
for line in lines:
	#print(line)
	#perf.hw.cache_misses cache_misses 第一个放a[1],第二个放b[1]
	tmp=line.strip().split(' ')
	a.append(tmp[0])
	b.append(tmp[1])

	
#with open('genPerfStp.py','w') as f:
f=open('genPerfStp.py','w')
f.write('''# coding=utf-8
import sys

def process(argv):
	print('用python执行。参数1：函数统计文件,参数2：次数，小于这个的才会被输出。文件中格式是：  函数名 次数' )
	print('要处理的文件名：'+argv[0])
	print('小于这个次数的函数才会被处理：'+argv[1])
	print("Using python to execute this script. \\narg1 is the function count file. arg2 is a number, the function will processed when the run count is lower than arg2.")
	with open(argv[0],'r') as myFile,  open('fnperf.stp','w') as f:
		f.writelines([\'\'\'#! /usr/bin/env stap
''')
dd=""
for i in range(len(a)):
	f.write('probe '+a[i]+'.$1.counter("'+b[i]+'"){} \n')
	dd+=''
	
f.write('''
		\\n\'\'\'])

		line = myFile.readline()
		error=0
		while line:
			#print(line)
			s=str(line).split(' ')
			try:
				if int(s[1])< int(argv[1]) and s[0]!='_start':
''')
dd=pp=""
for i in range(len(a)):
	dd+='%d'
	pp+='@perf("'+b[i]+'")'
	if i != len(a)-1:
		dd+=','
		pp+=','

f.write('''
					f.write('probe $1.function("'+s[0]+'").call{  printf("'+s[0]+',1,'''+dd+''' \\\\n", '''+pp+''' ); }\\n')
					f.write('probe $1.function("'+s[0]+'").return{  printf("'+s[0]+',2,'''+dd+''' \\\\n", '''+pp+''' ); }\\n')
''')

f.write('''
					f.write('\\n')
			except:
				error=1
				print("error:\\n"+str(line))
			line = myFile.readline()
		if error ==1 :
			print('---------')
			print('你可能需要手动添加error信息中的函数，可以使用*号作为通配符')
			print('There are some errors with some funcitons. You can use * to deal with it.')
			print(\'\'\'eg:
error:__find<__gnu_cxx::__normal_iterator<ISG::Node**, std::vector<ISG::Node*> >, ISG::Node*> 6
error:operator<< <std::char_traits<char> > 5probe $1.function("__find*").call{ trace(1, $$parms) }\\n
you may wanna add the two functions by manual. something similar with following:
probe $1.function("__find*").call { ...copy from the fnperf.stp file...}
probe $1.function("__find*").return { ......}
probe $1.function("operator*").call{ ...... }
probe $1.function("operator*").return { ......}
---------
\'\'\')
	print('Finished. check fnperf.stp file.')


if __name__ == '__main__':
	process(sys.argv[1:])
''')

f.close()


########生成 处理数据生成treegird的 py脚本#####################
f=open('processPerfdata2kexue.py','w')

f.write('''#coding=utf-8
\'\'\'
process the perf data. the data similar with followings....
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

\'\'\'

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
''')

pp=""
for i in range(len(b)):
	#'bi':data2kexue(int(j.split(',')[2])-int(tmpline.split(',')[2]))
	ijia2=str(i+2)
	pp+="'"+b[i]+"':data2kexue(int(j.split(',')["+ijia2+"])-int(tmpline.split(',')["+ijia2+"]))"
	if i != len(b)-1:
		pp+=','

f.write('''
								tmpdict={'id':(i),'name':funname,'''+pp+'''			}

							else:
								tmpdict={'id':(i),'name':funname,'''+pp+'''		,'_parentId':parentID}
''')

f.write('''

							#################tmpline和j间的数据
							funPerfList.append(tmpdict)

							break #结束这个函数的了。
					else:
							chongming=chongming-1
							continue


	currenttime = time.strftime('%Y%m%d.%H%M',time.localtime(time.time()))
	filename='treegridPerfData'+currenttime
	print("Save result to file: "+filename)
	with open( filename,'w') as fw:
		fw.writelines([\'\'\'{"total":\'\'\'+str(len(perfData))+\'\'\',"rows":[\'\'\'])
		fw.writelines(['\\n'])
		k=1
		kk=len(funPerfList)
		for i in funPerfList:
			fw.writelines([str(i).replace('\\'','"'),'\\n']) 
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


''')
f.close()								

f=open('perftreegrid.html','w')

f.write('''
<!DOCTYPE html>
<html>
<head>

	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	
	<title>TreeGrid with Footer - jQuery EasyUI Demo</title>
	<link rel="stylesheet" type="text/css" href="easyui.css">
	<link rel="stylesheet" type="text/css" href="icon.css">
	<link rel="stylesheet" type="text/css" href="demo.css">

	<script type="text/javascript" src="jquery.min.js"></script>
	<script type="text/javascript" src="jquery.easyui.min.js"></script>
<script>	function getQueryVariable(variable)
{
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == variable){return pair[1];}
       }
       return(false);
}
</script>
</head>
<body>
	<h2>TreeGrid with Footer</h2>
	<p>Show summary information on TreeGrid footer.</p>
	<div style="margin:20px 0;">
		<form action="perftreegrid.html" method="get">
    <div>
         <label for="search"></label></p>
<input name="file" id="file" value="" size="50">
<script>
    var url_string = window.location.href; //window.location.href
    var url = new URL(url_string);
    var c = url.searchParams.get("file");
    document.getElementById("file").value = c;
</script>   
         <button>open</button>
    </div>
</form></p>

	</div>
	<div style="margin:20px 0;"></div>
	
	<table id="tg"></table>
	<script type="text/javascript">
		$(function(){
			$('#tg').treegrid({
				title:'Functions Perf Info.',
				iconCls:'icon-ok',
				width:1500,
				height:850,
				rownumbers: false,
				animate:false,
				collapsible:false,
				fitColumns:true,
				url:getQueryVariable('file'),
				method: 'get',
				idField:'id',
				treeField:'name',
				showFooter:true,
				columns:[[
	                {title:'Fn Name',field:'name',width:100},
''')
pp=""
for i in range(len(b)):
	pp+="{field:'"+b[i]+"',title:'"+b[i]+"',width:61}"
	if i != len(b)-1:
		pp+=','
		

f.write(pp)
'''					{field:'bi',title:'bi',width:61},
					{field:'bm',title:'bm',width:61},
					{field:'cm',title:'cm',width:63},
					{field:'cr',title:'cr',width:63},
					{field:'ins',title:'ins',width:61},
					{field:'cc',title:'cc',width:61},
					{field:'rcc',title:'rcc',width:63},
					{field:'csw',title:'csw',width:63},
					{field:'ccl',title:'ccl',width:61},
					{field:'pfa',title:'pfa',width:61},
					{field:'tcl',title:'tcl',width:63}
'''

f.write('''
					]]
			});
		})
		$('.datagrid-cell').css('font-size','66px');
	</script>


</body>
</html>
''')


