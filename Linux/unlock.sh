#!/bin/bash

#Read first character of unlock file
count=$(head -c 1 ~/Documents/HAP/unlock.txt)

if [ "$count" == "1" ]	#If file content is "1"
then
if ! pgrep -x "aplay" > /dev/null	#If "aplay" service not already running
then					#If another alarm is not ON already
pico2wave -w speaking.wav "Welcome"			#Correct Password
aplay speaking.wav
rm speaking.wav			#Give Authentication status as voice feedback
fi &
else
if ! pgrep -x "aplay" > /dev/null
then
pico2wave -w speaking.wav "Wrong Password"	#Wrong Password
aplay speaking.wav
rm speaking.wav			#Give Authentication status as voice feedback
fi &
fi
