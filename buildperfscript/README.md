# Build your own fpowertool perf related scripts

Use cd into this path, and run 'sh build.sh'

If successed, finished.

-----------

If above not success, you can do as followings.
		
* Check the perf values which systemtap support. And save into perfliststapsupport.txt

```
stap -l "perf.*.*"
stap -l "perf.*.*"> perfliststapsupport.txt
python addfnalias.py
```

* Modify perfliststapsupport.txt

The perf values are saved in perfliststapsupport.txt

Simultaneous uses of too many perf values will slower the execution of the profiled program. Simultaneous uses of perf values CAN'T be greater than 16

You can delete the lines in perfliststapsupport.txt, which perf events you don't wanna profiling. Keep the perf values number <=16.

* Generate scripts.

   python genyourscript.py

If there is no error, these 3 files are generated: genPerfStp.py processPerfdata2kexue.py perftreegrid.html

Copy/move the .py files into (fpowertool path)/tools/ and the .html file into (fpowertool path)/treegrid/"

```
mv genPerfStp.py ../tools/genPerfStp.py
mv processPerfdata2kexue.py ../tools/processPerfdata2kexue.py
mv perftreegrid.html ../treegrid/perftreegrid.html
```

