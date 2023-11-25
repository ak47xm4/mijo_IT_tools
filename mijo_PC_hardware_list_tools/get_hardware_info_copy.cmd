@echo off

chcp 65001>nul

cd /d %~dp0

@REM host name get
FOR /F "usebackq" %%i IN (`hostname`) DO SET host=%%i
ECHO %host%


set hwfolder="the path to put cpuz and cyrstaldiskinfo txt , htm file"


@REM copy to desktop

mkdir %userprofile%\desktop\get_hardware_info_mijo\

set ddd=%userprofile%\desktop\get_hardware_info_mijo

XCOPY cpu-z_2.08-en %ddd%\cpu-z_2.08-en /S /I /Y /F /H /V /COMPRESS
XCOPY CrystalDiskInfoPortable %ddd%\CrystalDiskInfoPortable /S /I /Y /F /H /V /COMPRESS




cd /d %ddd%

echo "1001"

mkdir %hwfolder%\%host%\

echo "1002"

REM cpuz HW info

"cpu-z_2.08-en\cpuz_x64.exe" -html=cpuz

echo "1101"

COPY "cpu-z_2.08-en\cpuz.htm" "%hwfolder%\%host%\cpuz.htm"

echo "1102"

REM ssd hdd info

"CrystalDiskInfoPortable\DiskInfo64.exe" /CopyExit

echo "1201"

mkdir %hwfolder%\%host%\Smart\

echo "1202"


@REM XCOPY CrystalDiskInfoPortable\Smart\ %hwfolder%\%host%\Smart\ /S /I /Y /F /H /V /COMPRESS
COPY CrystalDiskInfoPortable\DiskInfo.txt %hwfolder%\%host%\DiskInfo.txt /Y

echo "1203"


cd /d ..

del %ddd% /S /Q
rmdir %ddd% /S /Q

echo "1301"

REM pause