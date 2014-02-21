#!/bin/bash

# auto compile to video the JPG of the current folder
freq=30 # fréquence de compilation
path="$(dirname $0)/../../assets/captation/exp"

cd $path

while true; do
  imagescount=$(find $path -type f -iname "*.JPG" -exec printf '.' \; | wc -c  | tr -d ' ')
  
  say "$imagescount images"
  
  echo "Refresh live movie ($imagescount)"
  
	ffmpeg -loglevel panic -f image2 -pattern_type glob -i '*.JPG' -r 25 -vcodec mpeg4 -b 30000k -vf scale=1920:-1 -y tmp.mp4
	cp -f tmp.mp4 live.mp4
	sleep $freq
done