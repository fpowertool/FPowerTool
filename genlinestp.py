#coding=utf-8
'''
'''
import sys
import os
def main(argv): #argv[1]
	binaryfilepath=argv[0]
	if not os.path.exists('./line.txt'):
		print("line.txt not exist\n")

	ttt='''#! /usr/bin/env stap
function trace(entry_p) {
  printf("%ld %d %s\\n",gettimeofday_us(),entry_p,ppfunc ()   )
}
'''
	with open('lineprofiling.stp','w') as f:
		f.write(ttt)


	filename='line.txt'#argv[0]
	try:
		with open(filename,'r') as f:
			lines=f.readlines()

		for line in lines:
			tmp=line.strip().split(' ')
			print('now process:')
			print(tmp)
			if len(tmp)==4:
				tmpfile=tmp[0]
				tmpstart = int(tmp[1])
				tmpend = int(tmp[2])
				tmpalias = tmp[3]
			elif len(tmp)==3:
				tmpfile=tmp[0]
				tmpstart = int(tmp[1])
				tmpend = int(tmp[2])
				tmpalias = 'f'+tmp[1]+'t'+tmp[2]

			#stap -L 'process("./lavaMD").statement("*@*kernel_cpu.c:*")' 
			shell='''stap -L 'process("'''+binaryfilepath+'''").statement("*@*'''+tmpfile+''':*")' '''
			print(shell)
			stream = os.popen(shell)
			
			output = stream.read()
			if output=='':
				print('we cant find the debug information, did you compile your program with -g flag? or use the right sourcecode filename?\nsomething is wrong....now exit..')
				#exit()
			output = output.split('\n')
			#print(output)
			#DWARF 
			dwarf={}   # line number, 
			#'process("/root/rodinia_3.1/openmp/lavaMD/lavaMD").statement("kernel_cpu@./kernel/kernel_cpu.c:103") $par:par_str $dim:dim_s long int $time4:long long int $alpha:double $a2:double $i:int $j:int $k:int $l:int $first_i:long int $rA:FOUR_VECTOR* $fA:FOUR_VECTOij:double $d:THREE_VECTOR\n'
			print(output[0])
			print(tmpfile)
			
			for i in output:
				try:
					
					if tmpfile in i:
						tmpva=i.split(tmpfile+':')[1] #kernel_cpu.c: split
						dwarf[int(tmpva.split('")')[0])]=tmpva #dwarf[103]=$par:par_str $dim..:int $first_i:long int 
						#print(int(tmpva.split('")')[0]))
						#print(dwarf[int(tmpva.split('")')[0])])
				except:
					pass
			#print(dwarf)

			#deal with the start and end  line 
			for j in sorted(dwarf):
				if j<tmpstart:
					continue
				if j>tmpstart:
					print('note: the start line number changed from '+str(tmpstart)+' to '+str(j)+'!\n')
				tmpstart =j
				break
			for j in sorted(dwarf):
				if j<tmpend:
					continue
				if j>tmpend:
					print('note: the end line number changed from '+str(tmpend)+' to '+str(j)+'!\n')
				tmpend =j
				break
			if len(tmp)==3:
				tmpalias = 'f'+tmp[1]+'t'+tmp[2]
			if tmpend == tmpstart:
				print('note: we did not process this snippet, as the start equals end line number!\n')
				continue
				#print(line[0] , dwarf[j])
			#write fo file
			with open('lineprofiling.stp','a') as f:
				f.write('probe $1.statement("*@*'+tmpfile+':'+str(tmpstart)+'" ){  \n')
				f.write('  printf("%ld 1 '+tmpalias+'\\n",gettimeofday_us() ) \n')
				f.write('} \n')
				f.write('probe $1.statement("*@*'+tmpfile+':'+str(tmpend)+'" ){  \n')
				f.write('  printf("%ld -1 '+tmpalias+'\\n",gettimeofday_us() ) \n')
				f.write('} \n\n')
	except Exception as e:
		print(e)
		print ('=== STEP ERROR INFO START')
		import traceback
		traceback.print_exc()
		print ('=== STEP ERROR INFO END')
		pass
	print('finished. you may check file: lineprofiling.stp')

if __name__ == "__main__":
	if len(sys.argv) ==1 :
		print('args need the .exe file path...\n')
		exit()
	print('the profiled execute file path:',sys.argv[1])
	print("you should write line.txt in current path already. now deal with the file line.txt\n")
	print("line.txt format: 'the .c/.f file name' 'start line number' 'end line number' 'alias'\neg:xx.c 11 22 snippet1\n")
	main(sys.argv[1:]) ##参数0是文件名，不传入下面的函数
