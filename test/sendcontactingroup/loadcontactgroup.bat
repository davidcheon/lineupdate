@echo off

rem ----------------start-----------------------
rem =================1:device==========================
rem -----------------init:makedir-------------------------

rem adb -s %1 shell "su -c '[ ! -d /vendor/test/sendcontactingroup/data ] && mkdir -p /vendor/test/sendcontactingroup/data && chmod -R 777 /vendor'"

rem --------------------init over-------------------------------
rem ---------------------2:datafilename---------------------------------------
rem adb -s %1 push data/%2 /vendor/test/sendcontactingroup/data/data.txt
adb -s %1 push D:\david\test\sendcontactingroup\sendcontactingroup.sh /vendor/test/sendcontactingroup/

adb -s %1 shell sh /vendor/test/sendcontactingroup/sendcontactingroup.sh
