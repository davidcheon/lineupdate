@echo off

rem ----------------start-----------------------
rem =================1:device==========================
rem -----------------init:makedir-------------------------

adb -s %1 shell "su -c '[ ! -d /vendor/test/shieldfriends/data ] && mkdir -p /vendor/test/shieldfriends/data && chmod -R 777 /vendor'"

adb -s %1 push D:\david\test\shieldfriends\shieldanddeletefriends.sh /vendor/test/shieldfriends/

adb -s %1 shell sh /vendor/test/shieldfriends/shieldanddeletefriends.sh %2
