# Yocto-record

## Data recording for Yocto-Thermocouple and Yocto-Meteo (Weather) modules in Python 

This small program allows to display and record **temperature**, **humidity** and **pressure** from **[Yocto-Meteo](http://www.yoctopuce.com/EN/products/capteurs-usb/yocto-meteo)**
module or **[Yocto-Thermocouples](http://www.yoctopuce.com/EN/products/usb-sensors/yocto-thermocouple)** module(s).

Data are displayed in a terminal (text mode) and updated every second (or any selected time interval).

Recordings are saved in a text file: **Date-Time-Module1-Module2-xxx.csv**. Separators are coma (can be changed), easily importable in Libreoffice Calc, Excel or any plotting software.

This version was tested with three modules (meteo & thermocouples),
works in direct usb mode, or with VirtualHub running.

## Updates
- 2013/11: Thanks to Yoctopuce support team, added basic error [exceptions handling] (http://docs.python.org/3.3/tutorial/errors.html#handling-exceptions) with (`try` & `except`), project name changed to yocto-record.py
- 2013/09: Meteo+tc.py first version.


***

## Required components

* Yocto-Meteo and/or Yocto-Thermocouples modules from Yoctopuce (http://www.yoctopuce.com/)
* Yoctopuce Python libraries: http://www.yoctopuce.com/EN/libraries.php (`YoctoLib.python.XXXX.zip`)
* Python 3.x: http://www.python.org/download/
* `yocto-record.py` script (from https://github.com/SebastienCaillat/Yoctopuce-Meteo-Temperature)

## Installation

* Install Python (with option to declare path for Windows users)
* Copy content of the directory `\YoctoLib.python.XXXX\Source\` (`yocto_api.py` and others `yocto_XXX.py` files)
to `~\Python3.3\Lib\` directory were Python is installed

## Starting the program 

* Put `yocto-record.py` on any directory, where the datafiles will be stored
* Open command prompt in this directory (Windows user: shift+right click in Explorer)
* Linux users, allow file to be executable, type: `chmod +x yocto-record.py`
* Type `yocto-record.py` (Win) or `./yocto-record.py` (Linux)  
=> Names of the recognized module(s) should appear  
=> Date, time, temperatures, pressure & humidity should be displayed every second
* Data will be saved in text file in column
* Name of the text file will be `Date-time-modules-types.csv` 
=> for example: `2013-08-18-08-12-21-Thermo-Meteo.csv`

**Warning:** Starting for Python IDLE will make data file empty (I don't know why...)

## Data file example

```
Day Time Temperature(°C) Pressure(mb) RH(%) Module: METEOMK1-0D163  
2013/08/19 14:18:41,24.0,1016,43  
2013/08/19 14:18:42,24.0,1016,43  
2013/08/19 14:18:43,24.0,1016,43  
```
## Settings

Some settings are avalaible using arguments:

* `yocto-record.py name` => will append a name to the data file  
=> for example: `2013-08-18-08-12-21-Thermo-Meteo-name.csv`
* `yocto-record.py nofile` to avoid saving to datafile
* `yocto-record.py help` or `?` for a very short help  

Other settings are available in the program (see settings section):

* Sample time: default is 1 second (automaticaly adjusted by the program to include script run time)
* Separator: default is coma (,)
* File extension: .txt or .csv
* Time by default is in iso format i.e. 2013-09-16T08:52:35.589860, can be chaged to custom

## Stoping the program

* Type [`Ctrl+c`] to stop the programm
* Import data file in any graphic software (delimiters are coma)
* Have fun!

