#!/bin/bash

# auto compile to video the JPG of the current folder

freq=30 # fréquence de compilation
path="$(dirname $0)/../../assets/captation/exp"

echo $path

mkdir -v $path
cd $path

while true; do
	ffmpeg -f image2 -pattern_type glob -i '*.JPG' -r 25 -vcodec mpeg4 -b 30000k -vf scale=1920:-1 -y tmp.mp4
	cp -f tmp.mp4 live.mp4
  	for (( i=$freq; i>0; i--)); do
    	sleep 1 &
    	printf "compiling in $i s \r"
    	wait    
    	printf "              \r"
  	done
done