@echo off

call D:\david\test\extractandsave\loadphonenumbers.bat %1 %2 %3

call D:\david\test\sendcontactingroup\loadcontactgroup.bat %1

call D:\david\test\shieldfriends\loadshieldfriends.bat %1
