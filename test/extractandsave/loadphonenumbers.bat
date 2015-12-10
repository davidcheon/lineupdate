@echo off
rem ---------start-----------
rem adb -s 127.0.0.1:19105 push exportphonenumbers.sh /vendor/test/

rem adb -s 127.0.0.1:19105 shell "su -c 'rm -rf /sdcard/Download/*'"

rem adb -s 127.0.0.1:19105 shell sh /vendor/test/exportphonenumbers.sh 1130
rem adb -s 127.0.0.1:19105 shell sh /vendor/test/exportphonenumbers.sh %1

rem adb -s 127.0.0.1:19105 shell "su -c 'rm -rf /sdcard/Download/9j'"

rem adb -s 127.0.0.1:19105 shell "su -c 'cat /sdcard/Download/* > /vendor/test/data/data.txt'"

rem adb -s 127.0.0.1:19105  pull /vendor/test/data/data.txt data

rem -----------start---------------
rem =======1:device 2:friendscounts 3:savefilename==========================
rem ----------init:makedir---------------
adb -s %1 shell "su -c '[ ! -d /vendor/test/extractandsave/data ] && mkdir -p /vendor/test/extractandsave/data && chmod -R 777 /vendor'"

adb -s %1 shell "su -c '[ ! -d /vendor/test/sendcontactingroup/data ] && mkdir -p /vendor/test/sendcontactingroup/data && chmod -R 777 /vendor'"

rem -----------init over--------------------------
adb -s %1 push D:\david\test\extractandsave\exportphonenumbers.sh /vendor/test/extractandsave/

adb -s %1 shell "su -c 'rm -rf /sdcard/Download/*'"

adb -s %1 shell sh /vendor/test/extractandsave/exportphonenumbers.sh %2

adb -s %1 shell "su -c '[ -d /sdcard/Download/9j ] && rm -rf /sdcard/Download/9j'"


adb -s %1 shell "su -c 'cat /sdcard/Download/* > /vendor/test/extractandsave/data/data.txt'"

adb -s %1  pull /vendor/test/extractandsave/data/data.txt D:\david\test\extractandsave\data\%3.txt

python D:\david\test\extractandsave\getphonenumberfromtext.py %3
copy D:\david\test\extractandsave\result\%3.txt D:\david\test\sendcontactingroup\data\
adb -s %1 push D:\david\test\extractandsave\result\%3.txt /vendor/test/sendcontactingroup/data/data.txt

