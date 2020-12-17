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
def process(argv):
	print('用python执行。参数1：函数统计文件,参数2：次数，小于这个的才会被输出。文件中格式是：  函数名 次数' )
	print('要处理的文件名：'+argv[0])
	print('小于这个次数的函数才会被处理：'+argv[1])
	print('''Using python to execute this script. 
arg1 is the function count file. arg2 is a number, the function will processed when the run count is lower than arg2.
''')
	with open(argv[0],'r') as myFile,  open('fnperf.stp','w') as f:
		f.writelines(['''#! /usr/bin/env stap

probe perf.hw.branch_instructions
    .$1
    .counter("bi") { }
probe perf.hw.branch_misses.$1.counter("bm") { }

probe perf.hw.cache_misses.$1.counter("cm") { }
probe perf.hw.cache_references.$1.counter("cr") { }

probe perf.hw.instructions.$1.counter("ins") { }
#三个基本成正比
probe perf.hw.cpu_cycles.$1.counter("cc") { }
probe perf.hw.ref_cpu_cycles.$1.counter("rcc") { }
#probe perf.hw.bus_cycles.$1.counter("mybus") { }  #saw: identifier 

#probe perf.hw.stalled_cycles_backend.$1.counter("scb") { }
#probe perf.hw.stalled_cycles_frontend.$1.counter("scf") { }

#alignment_faults计数为0
#probe perf.sw.alignment_faults.$1.counter("aligf") { } #saw: identifier 


probe perf.sw.context_switches.$1.counter("csw") { }
probe perf.sw.cpu_clock.$1.counter("ccl") { }

#cpu_migrations在npb里的这个是0
#probe perf.sw.cpu_migrations.$1.counter("cmi") { }


#probe perf.sw.emulation_faults.$1.counter("efa") { }
probe perf.sw.page_faults.$1.counter("pfa") { }
#probe perf.sw.page_faults_maj.$1.counter("pfm") { }
#probe perf.sw.page_faults_min.$1.counter("pfm2") { }
probe perf.sw.task_clock.$1.counter("tcl") { }

		\n'''])

		#lines=csv.reader(myFile)
		line = myFile.readline()
		#for line in lines:
		error=0
		while line:
			#print(line)
			s=str(line).split(' ')
			#print(s)
			#if len(s)==2 and int(s[1])< int(argv[1].strip()) :
			try:
				if int(s[1])< int(argv[1]) and s[0]!='_start':
					f.write('probe $1.function("'+s[0]+'").call{  printf("'+s[0]+',1,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d \\n", '+\
					'@perf("bi"), @perf("bm"), @perf("cm"), @perf("cr"), @perf("ins"), @perf("cc"), @perf("rcc") , '+\
					'@perf("csw") ,  @perf("ccl") ,@perf("pfa") ,  @perf("tcl") ); }\n')
					f.write('probe $1.function("'+s[0]+'").return{  printf("'+s[0]+',2,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d \\n", '+\
					'@perf("bi"), @perf("bm"), @perf("cm"), @perf("cr"), @perf("ins"), @perf("cc"), @perf("rcc") , '+\
					'@perf("csw") ,  @perf("ccl") ,@perf("pfa") ,  @perf("tcl") ); }\n')
					f.write('\n')
			except:
				error=1
				print("error:\n"+str(line))
			line = myFile.readline()
		if error ==1 :
			print('---------')
			print('你可能需要手动添加error信息中的函数，可以使用*号作为通配符')
			print('There are some errors with some funcitons. You can use * to deal with it.')
			print('''eg:
error:__find<__gnu_cxx::__normal_iterator<ISG::Node**, std::vector<ISG::Node*> >, ISG::Node*> 6
error:operator<< <std::char_traits<char> > 5probe $1.function("__find*").call{ trace(1, $$parms) }\n
you may wanna add the two functions by manual. something similar with following:
probe $1.function("__find*").call { ...copy from the fnperf.stp file...}
probe $1.function("__find*").return { ......}
probe $1.function("operator*").call{ ...... }
probe $1.function("operator*").return { ......}
---------
''')
	print('Finished. check fnperf.stp file.')


if __name__ == '__main__':
	process(sys.argv[1:])


