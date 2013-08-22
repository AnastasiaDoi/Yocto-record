#!/usr/bin/python
# -*- coding: utf-8 -*-
# Display and recording script for Yoctopuce modules(s)
# Ready for zero/one Yocto-Meteo and/or one to three Yocto-Thermocouples Modules
# Tested with Python 3.3 (http://www.python.org/download/)
# Content of directory \YoctoLib.python.XXXX\Source\ (yocto_xxx.py files)  
# Downloadable here: http://www.yoctopuce.com/EN/libraries.php (YoctoLib.python.XXXX.zip)
# must be in ~\Python3.3\Lib\ directory, with the other *.py files
# or uncomment following lines to add ../../Sources to the PYTHONPATH (adjust for your case)
# sys.path.append(os.path.join("..","..","Sources"))
# For detailed instructions: https://github.com/SebastienCaillat/Yoctopuce-Meteo-Temperature/
# Type meteo+tc.py in console to start program
#      meteo+tc.py name to append 'name' to the file name (optional)
#      meteo+tc.py help or ? for short instructions
# Last update S. Caillat 22/08/2013

import os,sys,time,datetime
time0 = time.time()
from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *

def help():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname+' with no argument: print & save data to file')
    print(scriptname+' <project_name>: append project_name to data file name')
    print(scriptname+' <nofile>: just display, no data file saved')
    print('See settings section in '+scriptname+' for other options') 
    sys.exit()

# Adjust interval time for data display & recording (module sleep time)
# Parameters are target time, real time, adjusted sleep value,
#                relaxation factor, tolerance (in percentage) & status
def adjust_time(target,loop,adjusted,rel,tol,mode): 
    diff = loop*1000 - target
    ratio = abs (diff/target)
    if ratio < tol : return adjusted  # Do noting if under tolerance
    if mode == "talk" : print ("Adjusting interval, target",target,\
    ",adj. %4.0f" %adjusted,",act. %4.0f" %(loop*1000),",er.: %0.3f" %ratio,\
    "% >",tol,"%") # Display message if time is adjusted
    if diff > 0 : adjusted = adjusted - diff/rel
    elif diff < 0 : adjusted = adjusted + abs(diff/rel)
    return adjusted

# Manage connexion or module error messages
def die(msg): sys.exit(msg+' (check USB cable)')
errmsg=YRefParam()
                    # ----------- Settings -------------------
                    # Inteval between two recordings, including script to run
sleep_target = 1000 # unit millisecond (1000 = 1 sec) (usage 900~1000 or more)
                    # Time will be adjusted to reach target
sleep_adjusted=sleep_target
relax = 5           # Factor for time loop adjustement (between 1 and 5) 
tolerance = 0.005   # Percentage time error accepted (0.01 = 1 %) (0.01 ~ 0.002)
#status = 'talk'    # display message at time adjust if value is 'talk'
status = 'none'
sep = ","           # Separator for data file (recommended " " or ",")
savedata = True     # default value, data is saved unless <nofile> as argument

if len(sys.argv) > 1:
    projectname=sys.argv[1]  # Project name to add to filename
    if projectname =='help' or projectname =='?': help()
    if projectname =='nofile': savedata = False

if YAPI.RegisterHub("http://127.0.0.1:4444") == 0:
    print ("VirtualHub is on")
if YAPI.RegisterHub("usb") == 0:
    print ("VirtualHub is off")

# retreive any humidity and temperature sensor
sensorH = YHumidity.FirstHumidity()
sensorT = YTemperature.FirstTemperature()

if sensorH is None:
    print('No Meteo module connected')
else:
    m = sensorH.get_module()
    target = m.get_serialNumber()
    if not m.isOnline(): die('device Meteo not connected')
    else:
        humSensor = YHumidity.FindHumidity(target+'.humidity')
        pressSensor = YPressure.FindPressure(target+'.pressure')
        tempSensor = YTemperature.FindTemperature(target+'.temperature')
        # retreive Meteo module serial
        serial=sensorH.get_module().get_serialNumber()
        logical=sensorH.get_module().get_logicalName()

if sensorT is None:
    die('No Thermocouple module connected')
else:
    t = sensorT.get_module()
    targetT = t.get_serialNumber()
    if not t.isOnline() : die('device Thermocouple not connected')
    
print('Device(s) list:')        # Determine device list: 3 usb + VirtualHub
module1 = module2 = module3 = []
modulequantity = 0
module = YModule.FirstModule()  # Meteo was called before
while module is not None:
     modulequantity = modulequantity+1
     print(module.get_serialNumber()+' ('+module.get_productName()+')')
     if module.get_serialNumber()[:7] == 'VIRTHUB':
        module = module.nextModule() # VirtualHub first so jump to next module
     if module.get_serialNumber()[:7] == 'METEOMK':
        print ("=> Module n°",modulequantity,": Temperature, Pressure & Humidity")
        if modulequantity == 1:
            module1 = 'Meteo'
            module1name = module.get_serialNumber()
        if modulequantity == 2:
            module2 = 'Meteo'
            module2name = module.get_serialNumber()
        if modulequantity == 3:
            module3 = 'Meteo'
            module3name=module.get_serialNumber()
     if module.get_serialNumber()[:7] == 'THRMCPL':
        print ("=> Module n°",modulequantity,": 2 Thermocouples")
        if modulequantity == 1:
            module1 = 'Thermo'
            module1name = module.get_serialNumber()
            channel1 = YTemperature.FindTemperature(module1name+'.temperature1')
            channel2 = YTemperature.FindTemperature(module1name+'.temperature2')
        if modulequantity == 2:
            module2 = 'Thermo'
            module2name = module.get_serialNumber()
            channel3 = YTemperature.FindTemperature(module2name+'.temperature1')
            channel4 = YTemperature.FindTemperature(module2name+'.temperature2')
        if modulequantity == 3:
            module3 = 'Thermo'
            module3name = module.get_serialNumber()
            channel5 = YTemperature.FindTemperature(module3name+'.temperature1')
            channel6 = YTemperature.FindTemperature(module3name+'.temperature2')
     module = module.nextModule()
print ("Total:",modulequantity, "module(s) connected")

if savedata is True:        # Set data file name: date-time-module(s).txt
    filename = module1 
    if modulequantity == 2: filename = filename+'-'+module2
    if modulequantity == 3: filename = filename+'-'+module2+'-'+module3
    if len(sys.argv) > 1: filename = filename+'-'+projectname
    nowdash = time.strftime('%Y-%m-%d-%H-%M-%S')
    filename = nowdash+'-'+filename+'.txt'
    print ("Saving data to: "+filename)
    f=open(filename,'w')    # Open data file
# print ('Init done in %2.3f' %(time.time()-time0), "s") # if needed

# Following blocs are for one, two or three modules connected
# One module: Meteo
if modulequantity == 1 and module1 == 'Meteo':
    print ('Meteo alone')
    print ("Time Temperature (°C) Pressure (mb) RH (%) (ctrl-c to stop) "+serial)
    if savedata == True :
        f.write("Day Time"+sep+"Temperature(°C)"+sep+"Pressure(mb)"\
                +sep+"RH(%)"+sep+"Module: "+serial+"\n") 
    while True:
        time_loop = time.time()
        nowshort = time.strftime('%H:%M:%S')
        print(nowshort +" | %2.1f" % tempSensor.get_currentValue()\
        +" °C %4.0f" % pressSensor.get_currentValue()\
        +" mb %2.0f" % humSensor.get_currentValue())
        if savedata == True:
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+'%2.1f' % tempSensor.get_currentValue()\
            +sep+"%4.0f" % pressSensor.get_currentValue()\
            +sep+"%2.0f" % humSensor.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)

# One module: Thermocouples 
if modulequantity == 1 and module1 == 'Thermo':
    print ('Thermo alone')
    print ("Time Temp-1 (°C) Temp-2 (°C) (ctrl-c to stop) "+module1name)
    if savedata == True :
        f.write("Day Time"+sep+"Temp-1(°C)"+sep+"Temp-2(°C)"\
                    +sep+"Module: "+module1name+"\n")
    while True :
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %4.1f" % channel1.get_currentValue()\
        + " °C %4.1f" % channel2.get_currentValue()+ " °C")
        if savedata == True:
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%4.1f" % channel1.get_currentValue()\
            +sep+"%4.1f" % channel2.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)

# Two modules: Meteo and Thermocouples (case 1)
if modulequantity == 2 and module1 == 'Thermo' and module2 == 'Meteo':
    print ('Meteo and Temp')
    print("Time Temp. (°C) Pres. (mb) RH (%)"+\
          " Temp-1 (°C) Temp-2 (°C) (ctrl-c to stop)")
    if savedata == True:
        f.write("Day Time"+sep+"Temperature(°C)"+sep+"Pressure(mb)"+sep+"RH(%)"\
                +sep+"Temp-1(°C)"+sep+"Temp-2(°C)"+sep+"Modules: "\
                +serial+" & "+module1name+"\n")
    while True:
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %4.1f" % channel1.get_currentValue()\
        + " °C %4.1f" % channel2.get_currentValue()+ " °C")
        if savedata == True:
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%2.1f" % tempSensor.get_currentValue()\
            +sep+"%4.0f" % pressSensor.get_currentValue()\
            +sep+"%2.0f" % humSensor.get_currentValue()\
            +sep+"%4.1f" % channel1.get_currentValue()\
            +sep+"%4.1f" % channel2.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)

# Two modules: Meteo and Thermocouples (case 2)
if modulequantity == 2 and module2 == 'Thermo' and module1 == 'Meteo':
    print ('Meteo and Temp')
    print("Time Temp. (°C) Pres. (mb) RH (%)"+\
          " Temp-1 (°C) Temp-2 (°C) (ctrl-c to stop)")
    if savedata == True:
        f.write("Day Time"+sep+"Temperature(°C)"+sep+"Pressure(mb)"+sep+"RH(%)"\
                +sep+"Temp-1(°C)"+sep+"Temp-2(°C)"+sep+"Modules: "\
                +serial+" & "+module1name+"\n")
    while True:
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %4.1f" % channel3.get_currentValue()\
        + " °C %4.1f" % channel4.get_currentValue()+ " °C")
        if savedata == True:
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%2.1f" % tempSensor.get_currentValue()\
            +sep+"%4.0f" % pressSensor.get_currentValue()\
            +sep+"%2.0f" % humSensor.get_currentValue()\
            +sep+"%4.1f" % channel3.get_currentValue()\
            +sep+"%4.1f" % channel4.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)

# Two modules: Thermocouples
if modulequantity == 2 and module1 == 'Thermo' and module2 == 'Thermo':
    print ('Temp & Temp')
    print("Time Temp-1 (°C) Temp-2 (°C) Temp-3 (°C) Temp-4 (°C) (ctrl-c to stop)")
    if savedata == True :
        f.write("Day Time"+sep+"Temp-1(°C)"+sep+"Temp-2(°C)"\
                +sep+"Temp-3(°C)"+sep+"Temp-4(°C)"\
                +sep+"Modules: "+module1name+" & "+module2name+"\n")
    while True:
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %4.1f" % channel1.get_currentValue()\
        + " °C %4.1f" % channel2.get_currentValue()\
        + " °C %4.1f" % channel3.get_currentValue()\
        + " °C %4.1f" % channel4.get_currentValue()+ " °C")
        if savedata == True:
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%4.1f" % channel1.get_currentValue()\
            +sep+"%4.1f" % channel2.get_currentValue()\
            +sep+"%4.1f" % channel3.get_currentValue()\
            +sep+"%4.1f" % channel4.get_currentValue()+"\n")
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)

# Three modules: one Meteo and two Thermocouples (case 1: Meteo is the last)
if modulequantity == 3 and module1 == 'Thermo' and module2 == 'Thermo'\
    and module3 == 'Meteo':
    print ('Meteo and Temp & Temp')
    print("Time T (°C) Pres. (mb) RH (%) T-1 (°C) T-2 (°C) T-3 (°C) T-4 (°C) (ctrl-c stop)")
    if savedata == True :
        f.write("Day Time"+sep+"Temperature(°C)"+sep+"Pressure(mb)"\
                +sep+"RH(%)"+sep+"Temp-1(°C)"+sep+"Temp-2(°C)"\
                +sep+"Temp-3(°C)"+sep+"Temp-4(°C)"+sep+"Modules: "\
                +serial+" & "+module1name+" & "+module2name+"\n") 
    while True:
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %4.1f" % channel1.get_currentValue()\
        + " °C %4.1f" % channel2.get_currentValue()\
        + " °C %4.1f" % channel3.get_currentValue()\
        + " °C %4.1f" % channel4.get_currentValue()+ " °C")
        if savedata == True :
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%2.1f" % tempSensor.get_currentValue()\
            +sep+"%4.0f" % pressSensor.get_currentValue()\
            +sep+"%2.0f" % humSensor.get_currentValue()\
            +sep+"%4.1f" % channel1.get_currentValue()\
            +sep+"%4.1f" % channel2.get_currentValue()\
            +sep+"%4.1f" % channel3.get_currentValue()\
            +sep+"%4.1f" % channel4.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)
        
# Three modules: one Meteo and two Thermocouples (case 2: Meteo in position 2)
if modulequantity == 3 and module1 == 'Thermo' and module3 == 'Thermo'\
    and module2 == 'Meteo':
    print ('Meteo and Temp & Temp')
    print("Time T (°C) Pres. (mb) RH (%)"\
          +"T-1 (°C) T-2 (°C) T-3 (°C) T-4 (°C) (ctrl-c stop)")
    if savedata == True:
        f.write("Day Time"+sep+"Temperature(°C)"+sep+"Pressure(mb)"+sep+"RH(%)"\
                +sep+"Temp-1(°C)"+sep+"Temp-2(°C)"+sep+"Temp-3(°C)"+sep+"Temp-4(°C)"\
                +sep+"Modules: "+serial+" & "+module1name+" & "+module2name+"\n") 
    while True :
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %4.1f" % channel1.get_currentValue()\
        + " °C %4.1f" % channel2.get_currentValue()\
        + " °C %4.1f" % channel5.get_currentValue()\
        + " °C %4.1f" % channel6.get_currentValue()+ " °C")
        if savedata == True :
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%2.1f" % tempSensor.get_currentValue()\
            +sep+"%4.0f" % pressSensor.get_currentValue()\
            +sep+"%2.0f" % humSensor.get_currentValue()\
            +sep+"%4.1f" % channel1.get_currentValue()\
            +sep+"%4.1f" % channel2.get_currentValue()\
            +sep+"%4.1f" % channel5.get_currentValue()\
            +sep+"%4.1f" % channel6.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)
        
# Three modules: one Meteo and two Thermocouples (case 3: Meteo in position 1)
if modulequantity == 3 and module2 == 'Thermo' and module3 == 'Thermo'\
    and module1 == 'Meteo':
    print ('Meteo and Temp & Temp')
    print("Time T (°C) Pres. (mb) RH (%)"\
          +"T-1 (°C) T-2 (°C) T-3 (°C) T-4 (°C) (ctrl-c stop)")
    if savedata == True:
        f.write("Day Time"+sep+"Temperature(°C)"+sep+"Pressure(mb)"+sep+"RH(%)"\
                +sep+"Temp-1(°C)"+sep+"Temp-2(°C)"+sep+"Temp-3(°C)"+sep+"Temp-4(°C)"\
                +sep+"Modules: "+serial+" & "+module1name+" & "+module2name+"\n") 
    while True :
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %4.1f" % channel3.get_currentValue()\
        + " °C %4.1f" % channel4.get_currentValue()\
        + " °C %4.1f" % channel5.get_currentValue()\
        + " °C %4.1f" % channel6.get_currentValue()+ " °C")
        if savedata == True :
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%2.1f" % tempSensor.get_currentValue()\
            +sep+"%4.0f" % pressSensor.get_currentValue()\
            +sep+"%2.0f" % humSensor.get_currentValue()\
            +sep+"%4.1f" % channel3.get_currentValue()\
            +sep+"%4.1f" % channel4.get_currentValue()\
            +sep+"%4.1f" % channel5.get_currentValue()\
            +sep+"%4.1f" % channel6.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)

# Three modules: Thermocouples
if modulequantity == 3 and module1 == 'Thermo'\
   and module2 == 'Thermo' and module3 == 'Thermo':
    print ('Temp and Temp & Temp')
    print("Time T-1 (°C) T-2 (°C) T-3 (°C) T-4"\
          +"(°C) T-5 (°C) T-6 (°C) (ctrl-c stop)")
    if savedata == True:
        f.write("Day Time"+sep+"Temp-1(°C)"+sep+"Temp-2(°C)"\
                +sep+"Temp-3(°C)"+sep+"Temp-4(°C)"\
                +sep+"Temp-5(°C)"+sep+"Temp-6(°C)"+sep+"Modules: "\
                +module1name+" & "+module2name+" & "+module3name+"\n") 
    while True :
        time_loop = time.time()
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %4.1f" % channel1.get_currentValue()\
        + " °C %4.1f" % channel2.get_currentValue()\
        + " °C %4.1f" % channel3.get_currentValue()\
        + " °C %4.1f" % channel4.get_currentValue()\
        + " °C %4.1f" % channel5.get_currentValue()\
        + " °C %4.1f" % channel6.get_currentValue()+ " °C")
        if savedata == True:
            now = time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(now+sep+"%4.1f" % channel1.get_currentValue()\
            +sep+"%4.1f" % channel2.get_currentValue()\
            +sep+"%4.1f" % channel3.get_currentValue()\
            +sep+"%4.1f" % channel4.get_currentValue()\
            +sep+"%4.1f" % channel5.get_currentValue()\
            +sep+"%4.1f" % channel6.get_currentValue()+"\n")    
        YAPI.Sleep(sleep_adjusted)
        time_loop = time.time()-time_loop
        sleep_adjusted=adjust_time(sleep_target,time_loop,sleep_adjusted,\
                                   relax,tolerance,status)
# for all others cases
print ("\nOooops")
print ("Maybe more than three modules are connected\n"\
       +"or some are not recognized.")
print ("Try again, replug, have a break or modify this program...")
