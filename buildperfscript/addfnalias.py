# coding=utf-8
'''
perf.hw.cache_misses cache_misses
perf.hw.cache_references cache_references
perf.hw.cpu_cycles cpu_cycles
'''
def main():
        with open('perfliststapsupport.txt','r') as f:
                lines=f.readlines()
        with open('perfliststapsupport.txt','w') as f:
                if len( lines)==0:
                        print('ERROR! No data in perfliststapsupport.txt')
                        exit
                for line in lines:
                        #print(line)
                        a=line.strip()+' '+line.split('.')[2]
                        f.write(a)

if __name__ == '__main__':
		main()
