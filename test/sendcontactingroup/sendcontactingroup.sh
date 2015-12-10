#!/bin/bash

usage(){
	echo $"Usage:datafilename.txt"
}
clicklineapp(){
	input tap 480 340
	sleep 1
}
backtohome(){
	input keyevent 3
	sleep 1
}

orderfirst(){
	input tap 55 175
	input tap 55 175
	sleep 1
}

clickgroup(){
	input tap 300 440
	sleep 0.3
	input tap 130 845
	sleep 0.5
}
clickgroupplusflag(){
	input tap 35 1037
	sleep 0.3
	input tap 105 345
	sleep 0.5
}
backtomain(){
	input keyevent 4
	sleep 0.3
	orderfirst
}
clearphonenumber(){
	input tap 560 160 
	sleep 0.3
}
typephonenumber(){
	clickgroupplusflag
	
	lines=$(cat /vendor/test/sendcontactingroup/data/data.txt|wc -l)
	for i in $(seq 1 $lines)
	do
		NUMBER=$(sed -n "${i}p" /vendor/test/sendcontactingroup/data/data.txt)
		clearphonenumber
		echo $i $NUMBER
		
		input text ${NUMBER:0:14}
		sleep 0.5
		input tap 300 285
		sleep 0.3
#		clearphonenumber
		input tap 300 1040
		sleep 1
		if (($i!=$lines))
		then
		clickgroupplusflag
		fi
		
	done
	backtomain
	backtohome
}
#--------------start-----------------------
#if (($# != 1))
#then
#	usage
#	exit 1
#fi
#DATAFILENAME=$1

backtohome

clicklineapp

orderfirst

clickgroup

typephonenumber
