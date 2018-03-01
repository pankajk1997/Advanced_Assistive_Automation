#!/bin/bash

CLIP_FILE=clipfile.txt
INC_FILE=incrementer.txt 	
FLAG_FILE=newsflag.txt
CMDFLAG_FILE=cmdflag.txt
SWITCH_FILE=switch.txt
UNLOCK_FILE=unlock.txt
ORIG_FILE=origclip.txt
INPUT_FILE=input.txt

echo 'Voice Assistance Started -Behan' > $CLIP_FILE
echo 'Voice Assistance Started -Behan' | xclip -selection clipboard
prevclip="Voice Assistance Started -Behan"
i=1
echo $i > $INC_FILE
newsflag=0
echo $newsflag > $FLAG_FILE
printf 00 > $SWITCH_FILE
echo "" > $ORIG_FILE
echo "ClipData { text/plain \"Copied Text\" {T:} }" > $INPUT_FILE
j=".ogg"
k="/home/pi/Music/"

while /bin/true
do

wd=""
x=""
echo "" > $CLIP_FILE
input=$(cat "$INPUT_FILE")

if [ "$input" == "ClipData { text/plain \"Copied Text\" {T:} }" ]
then
echo "$(xclip -selection clipboard -o)" > $ORIG_FILE
else
echo "$(cat "$INPUT_FILE")" > $ORIG_FILE
echo '' | xclip -selection clipboard
fi

origclip=$(cat "$ORIG_FILE")
origclip=${origclip,,}

if [[ $origclip != $prevclip ]]
then
for wd in $origclip
do

echo "0" > $CMDFLAG_FILE
clipboard=$x$wd

if [[ "$clipboard" == *start* && "$clipboard" == *program* ]]
then
echo 1 > $CMDFLAG_FILE
pkill aplay
pkill ogg123
pkill python
pkill python3
pkill loop.py
python /home/pi/Documents/HAP/loop.py &
clipboard=${clipboard/*start/}
clipboard=${clipboard/*program/}
echo $clipboard > $CLIP_FILE
fi &

if [[ "$clipboard" == *stop* && "$clipboard" == *music* ]]
then
echo 1 > $CMDFLAG_FILE
pkill ogg123
clipboard=${clipboard/*stop/}
clipboard=${clipboard/*music/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *music* && "$clipboard" == *next* ]]
then
echo 1 > $CMDFLAG_FILE
pkill ogg123
i=$(head -c 2 $INC_FILE)
if ((i == 11))
then
i=1
echo $i > $INC_FILE
else
i=$((i+1))
echo $i > $INC_FILE
fi
ogg123 "$k$i$j"
clipboard=${clipboard/*music/}
clipboard=${clipboard/*next/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *music* && "$clipboard" == *previous* ]]
then
echo 1 > $CMDFLAG_FILE
pkill ogg123
i=$(head -c 2 $INC_FILE)
i=$((i-1))
echo $i > $INC_FILE
ogg123 "$k$i$j"
clipboard=${clipboard/*music/}
clipboard=${clipboard/*previous/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *play* && "$clipboard" == *music* ]]
then
echo 1 > $CMDFLAG_FILE
pkill ogg123
i=$(head -c 2 $INC_FILE)
ogg123 "$k$i$j"
clipboard=${clipboard/*play/}
clipboard=${clipboard/*music/}
echo $clipboard > $CLIP_FILE
fi &

if [[ "$clipboard" == *volume* && "$clipboard" == *increas* ]]
then
echo 1 > $CMDFLAG_FILE
amixer set PCM -- $[$(amixer get PCM|grep -o [0-9]*%|sed 's/%//')+10]%
clipboard=${clipboard/*volume/}
clipboard=${clipboard/*increas/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *volume* && "$clipboard" == *decreas* ]]
then
echo 1 > $CMDFLAG_FILE
amixer set PCM -- $[$(amixer get PCM|grep -o [0-9]*%|sed 's/%//')-10]%
clipboard=${clipboard/*volume/}
clipboard=${clipboard/*decreas/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *mute* ]]
then
echo 1 > $CMDFLAG_FILE
amixer sset 'PCM' 0%
clipboard=${clipboard/*mute/}
echo $clipboard > $CLIP_FILE
fi &

if [[ "$clipboard" == *news* ]]
then
echo 1 > $CMDFLAG_FILE
newsflag=$(head -c 1 $FLAG_FILE)
if [ $newsflag == 0 ]
then
newsflag=1
echo $newsflag > $FLAG_FILE
pkill ogg123
chromium-browser 'https://tunein.com/radio/NDTV-24X7-s151565/' &
pico2wave -w speaking.wav "I am streaming N D T V news radio for you"
aplay speaking.wav
rm speaking.wav
else
newsflag=0
echo $newsflag > $FLAG_FILE
pkill ogg123
pkill chromium-browse -n
pico2wave -w speaking.wav "I am closing N D T V news radio for you"
aplay speaking.wav
rm speaking.wav
fi &
clipboard=${clipboard/*news/}
echo $clipboard > $CLIP_FILE
fi &

if [[ "$clipboard" == *unlock* ]]
then
pkill ogg123
pico2wave -w speaking.wav "I have unlocked the doors for you"
aplay speaking.wav
rm speaking.wav
echo 1 > $CMDFLAG_FILE
printf 1 > $UNLOCK_FILE
clipboard=${clipboard/*unlock/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *lock* ]]
then
pkill ogg123
pico2wave -w speaking.wav "I have locked the doors for you"
aplay speaking.wav
rm speaking.wav
echo 1 > $CMDFLAG_FILE
printf 0 > $UNLOCK_FILE
clipboard=${clipboard/*lock/}
echo $clipboard > $CLIP_FILE
fi &

if [[ "$clipboard" == *first* && "$clipboard" == *switch* ]]||[[ "$clipboard" == *1st* && "$clipboard" == *switch* ]]
then
echo 1 > $CMDFLAG_FILE
r=$(head -c 1 $SWITCH_FILE)
s=$(tail -c 1 $SWITCH_FILE)
if ((r==0))
then
printf 1$s > $SWITCH_FILE
else
printf 0$s > $SWITCH_FILE
fi &
pkill ogg123
pico2wave -w speaking.wav "I have switched first appliance for you"
aplay speaking.wav
rm speaking.wav
clipboard=${clipboard/*first/}
clipboard=${clipboard/*switch/}
clipboard=${clipboard/*1st/}
echo $clipboard > $CLIP_FILE
elif [[ "$clipboard" == *second* && "$clipboard" == *switch* ]]||[[ "$clipboard" == *2nd* && "$clipboard" == *switch* ]]
then
echo 1 > $CMDFLAG_FILE
r=$(head -c 1 $SWITCH_FILE)
s=$(tail -c 1 $SWITCH_FILE)
if ((s==0))
then
printf $r'1' > $SWITCH_FILE
else
printf $r'0' > $SWITCH_FILE
fi &
pkill ogg123
pico2wave -w speaking.wav "I have switched second appliance for you"
aplay speaking.wav
rm speaking.wav
clipboard=${clipboard/*second/}
clipboard=${clipboard/*switch/}
clipboard=${clipboard/*2nd/}
echo $clipboard > $CLIP_FILE
fi &

if [[ "$clipboard" == *develop* ]]||[[ "$clipboard" == *yourself* ]]
then
echo 1 > $CMDFLAG_FILE
pkill ogg123
pico2wave -w speaking.wav "I am your Behan. I am the control center of all electrical appliances, in this industry, but yet, I am your assistant. I was originally developed by Pankaj, Ashwinder, Balpreet and Deepak, for their final year project. My purpose is to help disabled, or elderly people, get there work done, with voice commands, provide productivity, by automating tasks, and also increase laziness."
aplay speaking.wav
rm speaking.wav
clipboard=${clipboard/*develop/}
clipboard=${clipboard/*yourself/}
echo $clipboard > $CLIP_FILE
fi &
	
	if [ "$(head -c 1 $CMDFLAG_FILE)" == "0" ]
	then
	echo $clipboard > $CLIP_FILE
	fi
	x=$(cat "$CLIP_FILE")

done

# Typing or searching commands here

prevclip=$origclip

fi
done
