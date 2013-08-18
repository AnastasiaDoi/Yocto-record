#!/usr/bin/python
# -*- coding: utf-8 -*-
# Display and recording script for simultaneous usage
# of zero or one Yocto-Meteo and/or one to three Yocto-Thermocouples Modules
# Tested with Python 3.3 (http://www.python.org/download/)
# Make sure to copy \YoctoLib.python.XXXX\Source\ directory content
# downloadable here http://www.yoctopuce.com/EN/libraries.php
# to \Python3.3\Lib\ directory (with Python Path declared for Windows)
# Last update S. Caillat 18/08/2013

import os,sys,time #python lib to be used

from yocto_api import *
from yocto_humidity import *
from yocto_temperature import *
from yocto_pressure import *

# Manage connexion or module error messages
def die(msg): sys.exit(msg+' (check USB cable)')

errmsg=YRefParam()

if YAPI.RegisterHub("http://127.0.0.1:4444") == 0:
    print ("VirtualHub is on")
if YAPI.RegisterHub("usb") == 0:
    print ("VirtualHub is off")

#if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
#    if YAPI.RegisterHub("http://127.0.0.1:4444", errmsg) != YAPI.SUCCESS:
#        sys.exit("init error"+errmsg.value)
    
#if YAPI.RegisterHub("http://127.0.0.1:4444", errmsg) == YAPI.SUCCESS\
#    or YAPI.RegisterHub("usb", errmsg)== YAPI.SUCCESS:
#    sys.exit("init error"+errmsg.value)
# Setup the API to use local USB devices
#if YAPI.RegisterHub("http://127.0.0.1:4444", errmsg)!= YAPI.SUCCESS:
#if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS :
#    sys.exit("init error"+errmsg.value)

# retreive any humidity and temperature sensor
sensorH = YHumidity.FirstHumidity()
sensorT = YTemperature.FirstTemperature()

# Total time between two recordings, including script to run,
# unit is millisecond (1000 = 1 sec), approx. 700 - 1000 seems good value
# reduce a little while using with virtualHub and remote reporting 
sleeptime = 700

if sensorH is None :
#   die('No Meteo module connected')
    print('No Meteo module connected')
else:
    m = sensorH.get_module()
    target = m.get_serialNumber()
    if not m.isOnline() : die('device Meteo not connected')
    else:
        humSensor = YHumidity.FindHumidity(target+'.humidity')
        pressSensor = YPressure.FindPressure(target+'.pressure')
        tempSensor = YTemperature.FindTemperature(target+'.temperature')
        # retreive Meteo module serial
        serial=sensorH.get_module().get_serialNumber()
        logical=sensorH.get_module().get_logicalName()

if sensorT is None :
    die('No Thermocouple module connected')
else:
    t = sensorT.get_module()
    targetT = t.get_serialNumber()
    if not t.isOnline() : die('device Thermocouple not connected')
    
# Determine device list (3 usb) + VirtualHub
module1 = module2 = module3 = []

print('Device(s) list:')
module = YModule.FirstModule() # Meteo was called before
modulequantity = 0
while module is not None:
     modulequantity = modulequantity+1
     print(module.get_serialNumber()+' ('+module.get_productName()+')')
     if module.get_serialNumber()[:7] == 'VIRTHUB':
        module = module.nextModule() # VirtualHub is the first jump to next module
     if module.get_serialNumber()[:7] == 'METEOMK':
        print ("=> Module n°",modulequantity,": Temperature, Pressure & Humidity")
        if modulequantity == 1:
            module1 = 'Meteo'
            module1name=module.get_serialNumber()
        if modulequantity == 2:
            module2 = 'Meteo'
            module2name=module.get_serialNumber()
        if modulequantity == 3:
            module3 = 'Meteo'
            module3name=module.get_serialNumber()
     if module.get_serialNumber()[:7] == 'THRMCPL':
        print ("=> Module n°",modulequantity,": 2 Thermocouples")
        if modulequantity == 1:
            module1 = 'Thermo'
            module1name=module.get_serialNumber()
            channel1 = YTemperature.FindTemperature(module1name + '.temperature1')
            channel2 = YTemperature.FindTemperature(module1name + '.temperature2')
        if modulequantity == 2:
            module2 = 'Thermo'
            module2name=module.get_serialNumber()
            channel3 = YTemperature.FindTemperature(module2name + '.temperature1')
            channel4 = YTemperature.FindTemperature(module2name + '.temperature2')
        if modulequantity == 3:
            module3 = 'Thermo'
            module3name=module.get_serialNumber()
            channel5 = YTemperature.FindTemperature(module3name + '.temperature1')
            channel6 = YTemperature.FindTemperature(module3name + '.temperature2')
     module = module.nextModule()
print ("Total:",modulequantity, "module(s) connected")

#Define data file name date/time/module(s)
filename = module1
if modulequantity == 2: filename = filename+'-'+module2
if modulequantity == 3: filename = filename+'-'+module2+'-'+module3
nowdash = time.strftime('%Y-%m-%d-%H-%M-%S')
filename = nowdash+'-'+filename+'.txt'
print ("Data file name: "+filename)

# Open data file
# Print values on terminal & save data to file
# Default time is every second, defined by 'sleeptime' value  
f=open(filename,'w')

# One module: Meteo
if (module1 == 'Meteo' or module2 == 'Meteo') and (modulequantity == 1):
    print ('Meteo alone')
    print("Time Temperature (°C) Pressure (mb) RH (%) (ctrl-c to stop) "+serial) 
    f.write("Day Time Temperature(°C) Pressure(mb) RH(%) Module: "+serial+"\n") 
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort +" | %2.1f" % tempSensor.get_currentValue()\
        +" °C %4.0f" % pressSensor.get_currentValue()\
        +" mb %2.0f" % humSensor.get_currentValue() + " % | file:"+ filename)
        f.write(now+" "+'%2.1f' % tempSensor.get_currentValue()\
        +" %4.0f" % pressSensor.get_currentValue()\
        +" %2.0f" % humSensor.get_currentValue()+"\n")    
        YAPI.Sleep(sleeptime)

# One module: Thermocouples 
if (module1 == 'Thermo' or module2 == 'Thermo') and (modulequantity == 1):
    print ('Thermo alone')
    print("Time Temp-1 (°C) Temp-2 (°C) (ctrl-c to stop)"+module1name)
    f.write("Day Time Temp-1(°C) Temp-2(°C) Module: "+module1name+"\n")
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % channel1.get_currentValue()\
        + " °C %2.1f" % channel2.get_currentValue()+ " °C")
        f.write(now + " %2.1f" % channel1.get_currentValue()\
        + " %2.1f" % channel2.get_currentValue()+"\n")    
        YAPI.Sleep(sleeptime)

# Two modules: Meteo and Thermocouples
if (module1 == 'Thermo' or module2 == 'Thermo' or module3 == 'Thermo')\
    and (module2 == 'Meteo' or module3 == 'Meteo') and (modulequantity == 2):
    print ('Meteo and Temp')
    print("Time Temp. (°C) Pres. (mb) RH (%) Temp-1 (°C) Temp-2 (°C) (ctrl-c to stop)")
    f.write("Day Time Temperature(°C) Pressure(mb) RH(%) Temp-1(°C) Temp-2(°C) Modules: "\
            +serial+" & "+module1name+"\n")
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %2.1f" % channel1.get_currentValue()\
        + " °C %2.1f" % channel2.get_currentValue()+ " °C")
        f.write(now + " %2.1f" % tempSensor.get_currentValue()\
        + " %4.0f" % pressSensor.get_currentValue()\
        + " %2.0f" % humSensor.get_currentValue()\
        + " %2.1f" % channel1.get_currentValue()\
        + " %2.1f" % channel2.get_currentValue()+"\n")    
        YAPI.Sleep(sleeptime)

# Two modules: Thermocouples
if (module1 == 'Thermo' or module2 == 'Thermo' or module3 == 'Thermo')\
    and (module2 == 'Thermo' or module3 == 'Thermo') and (modulequantity == 2):
    print ('Temp & Temp')
    print("Time Temp-1 (°C) Temp-2 (°C) Temp-3 (°C) Temp-4 (°C) (ctrl-c to stop)")
    f.write("Day Time Temp-1(°C) Temp-2(°C) Temp-3(°C) Temp-4(°C) Modules: "\
            +module1name+" & "+module2name+"\n") 
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % channel1.get_currentValue()\
        + " °C %2.1f" % channel2.get_currentValue()\
        + " °C %2.1f" % channel3.get_currentValue()\
        + " °C %2.1f" % channel4.get_currentValue()+ " °C")
        f.write(now + " %2.1f" % channel1.get_currentValue()\
        + " %2.1f" % channel2.get_currentValue()\
        + " %2.1f" % channel3.get_currentValue()\
        + " %2.1f" % channel4.get_currentValue()+"\n")  
        YAPI.Sleep(sleeptime)

# Three modules: one Meteo and two Thermocouples (case 1: Meteo is the last)
if (module1 == 'Thermo' and module2 == 'Thermo')\
    and module3 == 'Meteo' and (modulequantity == 3):
    print ('Meteo and Temp & Temp')
    print("Time T (°C) Pres. (mb) RH (%) T-1 (°C) T-2 (°C) T-3 (°C) T-4 (°C) (ctrl-c stop)")
    f.write("Day Time Temperature(°C) Pressure(mb) RH(%) Temp-1(°C) Temp-2(°C) Temp-3(°C) Temp-4(°C) Modules: "\
            +serial+" & "+module1name+" & "+module2name+"\n") 
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %2.1f" % channel1.get_currentValue()\
        + " °C %2.1f" % channel2.get_currentValue()\
        + " °C %2.1f" % channel3.get_currentValue()\
        + " °C %2.1f" % channel4.get_currentValue()+ " °C")
        f.write(now + " %2.1f" % tempSensor.get_currentValue()\
        + " %4.0f" % pressSensor.get_currentValue()\
        + " %2.0f" % humSensor.get_currentValue()\
        + " %2.1f" % channel1.get_currentValue()\
        + " %2.1f" % channel2.get_currentValue()\
        + " %2.1f" % channel3.get_currentValue()\
        + " %2.1f" % channel4.get_currentValue()+"\n")    
        YAPI.Sleep(sleeptime)

# Three modules: one Meteo and two Thermocouples (case 2: Meteo in position 2)
if (module1 == 'Thermo' and module3 == 'Thermo')\
    and module2 == 'Meteo' and (modulequantity == 3):
    print ('Meteo and Temp & Temp')
    print("Time T (°C) Pres. (mb) RH (%) T-1 (°C) T-2 (°C) T-3 (°C) T-4 (°C) (ctrl-c stop)")
    f.write("Day Time Temperature(°C) Pressure(mb) RH(%) Temp-1(°C) Temp-2(°C) Temp-3(°C) Temp-4(°C) Modules: "\
            +serial+" & "+module1name+" & "+module2name+"\n") 
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % tempSensor.get_currentValue()\
        + " °C %4.0f" % pressSensor.get_currentValue()\
        + " mb %2.0f" % humSensor.get_currentValue()\
        + " % |"+" %2.1f" % channel1.get_currentValue()\
        + " °C %2.1f" % channel2.get_currentValue()\
        + " °C %2.1f" % channel5.get_currentValue()\
        + " °C %2.1f" % channel6.get_currentValue()+ " °C")
        f.write(now + " %2.1f" % tempSensor.get_currentValue()\
        + " %4.0f" % pressSensor.get_currentValue()\
        + " %2.0f" % humSensor.get_currentValue()\
        + " %2.1f" % channel1.get_currentValue()\
        + " %2.1f" % channel2.get_currentValue()\
        + " %2.1f" % channel5.get_currentValue()\
        + " %2.1f" % channel6.get_currentValue()+"\n")    
        YAPI.Sleep(sleeptime)

# Three modules: Thermocouples
if (module1 == 'Thermo' and module2 == 'Thermo' and module3 == 'Thermo')\
    and (modulequantity == 3):
    print ('Temp and Temp & Temp')
    print("Time T-1 (°C) T-2 (°C) T-3 (°C) T-4 (°C) T-5 (°C) T-6 (°C) (ctrl-c stop)")
    f.write("Day Time Temp-1(°C) Temp-2(°C) Temp-3(°C) Temp-4(°C) Temp-5(°C) Temp-6(°C) Modules: "\
            +module1name+" & "+module2name+" & "+module3name+"\n") 
    while True:
        now = time.strftime('%Y/%m/%d %H:%M:%S')
        nowshort = time.strftime('%Hh%M:%Ss')
        print(nowshort + " | %2.1f" % channel1.get_currentValue()\
        + " °C %2.1f" % channel2.get_currentValue()\
        + " °C %2.1f" % channel3.get_currentValue()\
        + " °C %2.1f" % channel4.get_currentValue()\
        + " °C %2.1f" % channel5.get_currentValue()\
        + " °C %2.1f" % channel6.get_currentValue()+ " °C")
        f.write(now + " %2.1f" % channel1.get_currentValue()\
        + " %2.1f" % channel2.get_currentValue()\
        + " %2.1f" % channel3.get_currentValue()\
        + " %2.1f" % channel4.get_currentValue()\
        + " %2.1f" % channel5.get_currentValue()\
        + " %2.1f" % channel6.get_currentValue()+"\n")    
        YAPI.Sleep(sleeptime)
