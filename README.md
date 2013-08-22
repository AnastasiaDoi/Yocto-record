# Yoctopuce-Meteo-Temperature
===========================

## Data recording for Yoctopuce Meteo (Weather) and Thermocouples modules in Python 

This small program allows displaying in a terminal (text mode, updated every second):
* Pressure
* Humidity
* Temperature(s)

From zero to one **[Yocto-Meteo](http://www.yoctopuce.com/EN/products/capteurs-usb/yocto-meteo)**
module and/or zero to three thermocouples
**[Yocto-Thermocouples](http://www.yoctopuce.com/EN/products/usb-sensors/yocto-thermocouple)** module(s).

At the same type a text file is created, updated every second (by default): **Date-Time-Module1-Module2-....txt**. 
Separators are coma (or any other caracter), easily importable in Libreoffice Calc, Excel or any plotting software.

This is a draft version, tested with three modules (1 Meteo & 2 thermocouples),
works in direct usb mode, or with VirtualHub running.

***

## Required components

* Yocto-Meteo and/or Yocto-Thermocouples modules from Yoctopuce (http://www.yoctopuce.com/)
* Yoctopuce Python libraries: http://www.yoctopuce.com/EN/libraries.php (YoctoLib.python.XXXX.zip)
* Python 3.x: http://www.python.org/download/
* Meteo+TC.py script (from https://github.com/SebastienCaillat/Yoctopuce-Meteo-Temperature)

## Installation

* Install Python (with option to declare path)
* Copy content of the directory \YoctoLib.python.XXXX\Source\ (yocto_api.py and other yocto_XXX.py files)
to ~\Python3.3\Lib\ directory were Python was installed

## Starting the program 

* Put Meteo+TC.py on any directory, where the datafiles will be stored
* Open command prompt in this directory (Windows user: shift+right click in Explorer)
* Type Meteo+TC.py  
=> Names of the recognized module(s) should appear  
=> Date, time, temperatures, pressure & humidity should be displayed every second
* Same data will be saved in text file in column 
* Name of the text file will be Date-time-modules-types.txt  
=> for example: 2013-08-18-08-12-21-Thermo-Meteo.txt

## Data file example

Day Time Temperature(°C) Pressure(mb) RH(%) Module: METEOMK1-0D163  
2013/08/19 14:18:41,24.0,1016,43  
2013/08/19 14:18:42,24.0,1016,43  
2013/08/19 14:18:43,24.0,1016,43  

## Settings
Some settings are avalaible using argument:
* Meteo+TC.py name => will append a name to the data file  
=> for example: 2013-08-18-08-12-21-Thermo-Meteo-name.txt
* Meteo+TC.py nofile to avoid saving to datafile
* Meteo+TC.py help or ? for a very short help  

Other settings are available in the program:
* Sample time: default is 1 second, automaticaly adjusted by the program to include script run time 
* Separator: default is coma (,)

## Stoping the program

* Type [Ctrl+c] to stop the programm
* Import data file in any graphic software (delimiter are coma)
* Have fun!

