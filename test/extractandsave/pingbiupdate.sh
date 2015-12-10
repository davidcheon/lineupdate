#!/bin/bash
usage(){
	echo $"Usage:matchnumber counts"
}

#-------------start-----------
if (($# != 2))
then
	usage
	exit 1
fi

i=0
tag=1
ymove=491
yclick=260
input tap 560 80
sleep 0.3
input tap 380 160
sleep 0.3
input text $1
sleep 1
while (($i<$2-8))
do
	if (($tag%10==0))
	then
		ymove=$(($ymove+5))
	else
		ymove=491
	fi
	if (($i!=0))
	then
		input swipe 300 600 300 $ymove 1000
	fi
	
	input tap 300 $yclick
	sleep 0.3
	i=$(($i+1))
	tag=$(($tag+1))
done
input swipe 300 600 300 $ymove 1000
sleep 0.3
tmp=0
while (($i<$2))
do
	input tap 300 $(($yclick+$tmp*100))
	sleep 0.3	
	tmp=$(($tmp+1))
	i=$(($i+1))
done
input tap 170 1030
sleep 0.3
input tap 410 650
