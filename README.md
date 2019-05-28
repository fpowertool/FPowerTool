# FPowerTool

#### Description
A Function-level Power Profiling Tool

The profile server needs: python, systemtap, papi.
The presentation server needs: easyui, grafana, influxdb.

#### Usage

Example of raytrace.

Put FPowerTool files into your path of profile application.

1. Count the functions.

```
stap -v tools/functioncount.stp 'process("/home/gwei/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc/bin/bodytrack").function("*")' -c "/home/gwei/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc/bin/bodytrack sequenceB_2 4 2 2000 5 0 1" -o app.funcount
```
2. Generate .stp file to decide which functions to profile.

```
python tools/FPowerTool.genfunctionstp.py app.funcount 5000
```

3. Profile the application.
```
sh FPowerTool.sh /home/gwei/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc/bin/bodytrack sequenceB_2 4 2 2000 5 0 1 
```

Output 2 timestamp file:fpt.t1, fpt.t2
Output rapl data: rapl.log
Output resutlt data: fptfun.log
 

4. Deal with the result.


Post data to InfluxDB.
```
python tools/FPowerTool.postRapl2influx.py rapl.log
python tools/FPowerTool.postTime2influx.py fpt raytrace
```

Process the result. Output treegriddata
```
python tools/FPowerTool.processRAPLwithFunc.py fptfun.log rapl.log  treegriddata 
```

5. Presentation.

Open your grafana web site, configure with your influxdb, to see the graphical visualization.

Put treegriddata file into jquery-easyui-1.5.5.6\treegrid\. use a websever,open fluid.html to see the result.