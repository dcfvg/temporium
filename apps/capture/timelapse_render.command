#!/bin/bash
# auto compile to video the JPG of the current folder
# 
# @author Benoît VERJAT
# @since  01.02.2014
#

# param
freq=30 # render frequence in seconds
path="$(dirname $0)/../../assets/captation/exp"


# init
# go to curent exposure folder
cd $path

while true; do
  
  # count images 
  imagescount=$(find $path -type f -iname "*.JPG" -exec printf '.' \; | wc -c  | tr -d ' ')  
  echo "Refresh live movie ($imagescount)"
  
  # render move
	ffmpeg -loglevel panic -f image2 -pattern_type glob -i '*.jpg' -r 25 -vcodec mpeg4 -b 30000k -vf scale=1920:-1 -y tmp.mp4
	
	# replace live movie
	cp -f tmp.mp4 live.mp4
	
	# wait for next render
	sleep $freq
done