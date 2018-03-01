#!/bin/bash

#Read first character of alarm file
count=$(head -c 1 ~/Documents/HAP/alarm.txt)

if [ "$count" == "1" ]	#If file content is "1"
then
if ! pgrep -x "aplay" > /dev/null	#If "aplay" service not already running
then					#If another alarm is not ON already
aplay ~/Music/fire.wav &		#Play Fire Alarm
fi &
elif [ "$count" == "2" ]
then
if ! pgrep -x "aplay" > /dev/null
then
aplay ~/Music/intruder.wav &	#Similarly Play Theft Alarm
fi &
elif [ "$count" == "3" ]
then
if ! pgrep -x "aplay" > /dev/null
then
aplay ~/Music/gas.wav &			#Similarly Play Gas Alarm
fi &
else
pkill aplay	#Kill aplay service
fi &
