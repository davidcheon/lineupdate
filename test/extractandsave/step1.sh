#!/bin/bash
DEVICE=""

usage(){
	echo $"Usage: friendscounts"
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

clickgroupbutton(){
	input tap 300 430
	sleep 1
}

clickgroupchatbutton(){
	input tap 130 840
	sleep 1
}

cleargroupchathistory(){
	input tap 560 80
	sleep 0.3
	input tap 521 320
	sleep 0.3
	input tap 300 400
	sleep 0.3
	input tap 420 640
	sleep 1
	input tap 300 550
	sleep 0.3
}

clickgroupchatplusbutton(){
	input tap 35 1040
	sleep 0.3
}

clickgroupchatfriendscontactsbutton(){
	input tap 95 340
	sleep 1
}

choosefriendingroupchat(){

}
#-------------start-----------
if (($# != 1))
then
	usage
	exit 1
fi
#DEVICE=$1
FRIENDS=$1
backtohome

clicklineapp

orderfirst

clickgroupbutton

clickgroupchatbutton

cleargroupchathistory

clickgroupchatplusbutton

clickgroupchatfriendscontactsbutton
