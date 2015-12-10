#!/bin/bash
i=0
tag=1
ymove=500
yclick=265
while(($i<$1))
do
#	if(($tag%10==0))
#	then
#		ymove=$(($ymove+5))	
#	else
#		ymove=500
#	fi
#	if (($i!=0))
#	then
#		input swipe 300 600 300 $ymove 1000
#	fi
	input swipe 300 $yclick 300 $yclick 1000
	sleep 0.3

	input tap 300 650
	sleep 0.3
	
	input tap 410 610
	sleep 1
	i=$(($i+1))
	tag=$(($tag+1))
done
