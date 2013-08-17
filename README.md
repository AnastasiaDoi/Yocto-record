# Yoctopuce-Meteo-Temperature
===========================

Data recording for Yoctopuce Meteo (Weather) and Thermocouples modules in Python 

This small program allows displaying in a terminal (text mode, updated every second):
* Pressure
* Humidity
* Temperature

from **[Yocto-Meteo](http://www.yoctopuce.com/EN/products/capteurs-usb/yocto-meteo)** module
and/or two temperatures from **[Yocto-Thermocouples](http://www.yoctopuce.com/EN/products/usb-sensors/yocto-thermocouple)** module.

At the same type a text file is created, updated every second: **Date-Time-Module1-Module2.txt**. 
Separators are spaces, easily importable in Libreoffice Calc, Excel or any plotting software

This is a draft version, tested with two modules, works in direct usb mode, but still buggy when VirtualHub is running...
