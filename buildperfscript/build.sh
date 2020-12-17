#!/bin/bash
clear
if [ -f ./perfliststapsupport.txt ]
then
echo "The file perfliststapsupport.txt exists."
read -r -p "Are you want to reGenerate the perfliststapsupport.txt? [Y/n] " input

case $input in
    [yY][eE][sS]|[yY])
		echo "Yes"
		stap -l "perf.*.*"> perfliststapsupport.txt
		python addfnalias.py
		;;

    [nN][oO]|[nN])
		echo " "
       	;;

    *)
		echo "Invalid input..."
		exit 1
		;;
esac

else
echo 'Generate perf event which systemtap support'
		stap -l "perf.*.*"> perfliststapsupport.txt
		python addfnalias.py
fi

clear
echo "The perf values are saved in perfliststapsupport.txt"
filesCount=`cat perfliststapsupport.txt |wc -l`

if [ $filesCount -gt 16 ]
then
echo "Simultaneous uses of too many perf values will slower the execution of the profiled program."
echo "Simultaneous uses of perf values CAN'T be greater than 16"
echo "perf values is "$filesCount
echo "You MUST DELETE some lines in perfliststapsupport.txt, which perf events you don't wanna profiling. "
else
echo "Simultaneous uses of too many perf values will slower the execution of the profiled program."
echo "perf values is "$filesCount
echo "You may wanna delete the lines in perfliststapsupport.txt, which perf events you don't wanna profiling. "
fi

read -r -p "Edit perfliststapsupport.txt(vim perfliststapsupport.txt)? [Y/n] " input
case $input in
    [yY][eE][sS]|[yY])
		echo "Now, run the shell: vim perfliststapsupport.txt"
		sleep 2
		vim perfliststapsupport.txt
		;;

    [nN][oO]|[nN])
		echo "No"
      	;;

    *)
		echo "Invalid input..."
		exit 1
		;;
esac

clear
filesCount=`cat perfliststapsupport.txt |wc -l`

if [ $filesCount -gt 16 ]
then
echo "Simultaneous uses of too many perf values will slower the execution of the profiled program."
echo "Simultaneous uses of perf values CAN'T be greater than 16"
echo "perf values is "$filesCount
echo "You MUST DELETE some lines in perfliststapsupport.txt, which perf events you don't wanna profiling. "
exit
fi
python genyourscript.py
echo "If there is no error, these 3 files are generated:"
echo "genPerfStp.py processPerfdata2kexue.py perftreegrid.html"
echo "You can copy/move the .py files into (fpowertool path)/tools/ and the .html file into (fpowertool path)/treegrid/"

read -r -p "Move the files now? [Y/n] " input
case $input in
    [yY][eE][sS]|[yY])
mv genPerfStp.py ../tools/genPerfStp.py
mv processPerfdata2kexue.py ../tools/processPerfdata2kexue.py
mv perftreegrid.html ../treegrid/perftreegrid.html
		;;

    [nN][oO]|[nN])
		echo "Finished. Bye"
		exit 1
       	;;

    *)
		echo "Invalid input..."
		exit 1
		;;
esac
echo "Finished."






