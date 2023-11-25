@echo off

chcp 65001>nul

REM cd /d %~dp0

cd /d %userprofile%\desktop\

@REM host name get
FOR /F "usebackq" %%i IN (`hostname`) DO SET host=%%i
ECHO %host%



set hwfolder="the path to put cpuz and cyrstaldiskinfo txt , htm file"



echo "1001"

mkdir %hwfolder%\%host%\

echo "1002"



wmic /OUTPUT:mijo_USB_HW_id.tmp path Win32_USBControllerDevice get Dependent

copy mijo_USB_HW_id.tmp %hwfolder%%host%\USB_HW_id.txt /Y

del mijo_USB_HW_id.tmp /S /Q

echo "1301"


REM pause 