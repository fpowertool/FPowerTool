# coding=utf-8


import csv
import sys

'''
jinit_memory_mgr 256
jpeg_calc_output_dimensions 256
reset_error_mgr 256
jpeg_mem_init 256
start_pass_huff_decoder 256
jpeg_stdio_src 256
jpeg_CreateDecompress 256
self_destruct 256
'''
def postTime2influx(argv):
	print('要处理的文件名：'+argv[0])
	print('小于这个次数的函数才会被处理：'+argv[1])

	with open(argv[0],'rb') as myFile,  open('batch.stp','w') as f:


		f.writelines(['''#! /usr/bin/env stap

function trace(entry_p, extra) {
  %( $# > 1 %? if (tid() in trace) %)
  printf("%ld %d %s\\n",ettimeofday_us(),entry_p,ppfunc ()   )
}


%( $# > 1 %?
global trace
probe $2.call {
  trace[tid()] = 1
}
probe $2.return {
  delete trace[tid()]
}
%)
		\n'''])

		#lines=csv.reader(myFile)
		line = myFile.readline()
		#for line in lines:
		while line:
			#print(line)
			s=str(line).split(' ')
			print(s)
			#if len(s)==2 and int(s[1])< int(argv[1].strip()) :
			try:
				if int(s[1])< int(argv[1]) and s[0]!='_start':
					f.writelines(['probe $1.function("',s[0],'").call{ trace(1, $$parms) }\n'])
					f.writelines(['probe $1.function("',s[0],'").return { trace(-1, $$return)}\n'])
			except:
				print("error:"+str(line))
			line = myFile.readline()



if __name__ == '__main__':
	print('arg1:function count filename;arg2:a number, we want the functions which run times less than this number.' )
	postTime2influx(sys.argv[1:])
	print('over. check batch.stp file.')

