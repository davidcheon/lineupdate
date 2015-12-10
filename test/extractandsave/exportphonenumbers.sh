#!/bin/bash
#606 * 1080
#the less the belower
#the more the upper
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

clickpen(){
	input tap 434 618
	sleep 0.3
}

copynumber(){
	input swipe 150 260 150 260 1500
	sleep 0.3
	input tap 460 80
	sleep 0.3
	input keyevent 4
	sleep 0.3
	input tap 415 630
	sleep 0.3
}
exportaction(){
	i=0
	tag=1
	ymoveto=491
	while (($i<$1-6))
		do
			if(($tag%10==0))
			then
				ymoveto=498.81
			else
				ymoveto=491
			fi
			if(($i!=0))
			then
				input swipe 300 600 300 ${ymoveto} 1000
		
				
				
			fi
			input tap 300 580
			sleep 0.5
			clickpen
			copynumber

			echo $i
			i=$(($i+1))
			tag=$(($tag+1))
		done
	tmp=0
	input swipe 300 600 300 ${ymoveto} 1000
	while(($i<$1))
	do
		if (($i!=$1-1))
		then
		input tap 300 $((580+$tmp*100))
		else
		input tap 300 1060
		fi
		sleep 0.5
		echo $i
		clickpen
		copynumber
		tmp=$(($tmp+1))
		i=$(($i+1))
	done

}

clickjianzhiduiapp(){
	input tap 114 710
	sleep 1
}
clearjianzhiduiexisted(){
	clickjianzhiduiapp
#	openbatbutton
	input tap 565 90
	sleep 0.3
#	clearall
	input tap 410 250
	sleep 0.3
#	clickokbutton
	input tap 440 670
	sleep 0.3
#	backhome
	backtohome
}
clearsdcarddownload(){
	su
	rm -rf /sdcard/Download/*
}
copytxttovendortestdata(){
	rm -rf /sdcard/Download/9j
	cat /sdcard/Download/* > /vendor/test/data/data.txt
}

batfile(){
	
	backtohome
	
	clickjianzhiduiapp
#	openbatbutton
	input tap 565 90
	sleep 0.3
#	clickbatbutton
	input tap 420 175
	sleep 0.3
#	newbatbutton
	input tap 300 1010
	sleep 0.3	
#	exportnutton
	input tap 300 1010
	sleep 0.3
#	back1
	input keyevent 4
	sleep 0.5
#	back2
	input keyevent 4
	sleep 0.3
#	backtohome
	backtohome

}
#-------------start-----------
if (($# != 1))
then
	usage
	exit 1
fi
FRIENDS=$1
backtohome

clearjianzhiduiexisted

clicklineapp

orderfirst

exportaction $FRIENDS

batfile
