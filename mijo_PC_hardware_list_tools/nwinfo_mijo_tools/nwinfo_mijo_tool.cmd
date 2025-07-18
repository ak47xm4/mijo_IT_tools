@echo off
cd /d %~dp0

.\nwinfo.exe --format=json --output=report.json --cp=UTF8 --human --sys --disk --smart --display --usb --uefi --gpu --net --cpu --smbios=2

curl -X POST -H "Content-Type: application/json" -d @report.json "https://n8n-mijo199x.zeabur.app/webhook/5b106a15-3472-4e14-8a21-27330a346dbaa"