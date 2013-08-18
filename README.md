# Yoctopuce-Meteo-Temperature
===========================

Data recording for Yoctopuce Meteo (Weather) and Thermocouples modules in Python 

This small program allows displaying in a terminal (text mode, updated every second):
* Pressure
* Humidity
* Temperature(s)

from zero to one **[Yocto-Meteo](http://www.yoctopuce.com/EN/products/capteurs-usb/yocto-meteo)** module
and/or zero to three thermocouples **[Yocto-Thermocouples](http://www.yoctopuce.com/EN/products/usb-sensors/yocto-thermocouple)** module(s).

At the same type a text file is created, updated every second (by default): **Date-Time-Module1-Module2-....txt**. 
Separators are spaces, easily importable in Libreoffice Calc, Excel or any plotting software

This is a draft version, tested with three modules (1 Meteo & 2 thermocouples), works in direct usb mode, or with VirtualHub running.

***

## Required components

* Yocto-Meteo and/or Yocto-Thermocouples modules from yoctopuce (http://www.yoctopuce.com/)
* Yoctopuce Python libraries http://www.yoctopuce.com/EN/libraries.php (YoctoLib.python.XXXX.zip)
* Python 3.x: http://www.python.org/download/
* Meteo+TC.py script

## Installation

* Install Python (with option to declare path)
* Copy content of the directory \YoctoLib.python.XXXX\Source\
* to ~\Python3.3\Lib\ directory were Python was installed

## Starting the program 

* Put Meteo+TC.py on any directory, where the datafiles will be stored
* Open command prompt in this directory (shift+right click in Explorer)
* Type Meteo+TC.py
* Names of the recognized modules should appear
* Date, time, temperatures, pressure & humidity should be displayed every second
* Same date should be saved in text file in column 
* Name of the text file will be Date-time-modules-types.txt
* for example: 2013-08-18-08-12-21-Thermo-Meteo.txt
* Optional: Type Meteo+TC.py name will append a name to the data file
* for example: 2013-08-18-08-12-21-Thermo-Meteo_name.txt

## Stoping the program

* Type [Ctrl+C] to stop
* Import data file in any graphic software (delimiter are spaces)
* Have fun !

