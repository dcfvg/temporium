#!/bin/bash
#set -x
#
# the temporium main script
#  
# 
# @author Benoît VERJAT
# @since  01.02.2014
#



# include var and functions for local use
source functions.sh  
PATH=/usr/local/bin/:$PATH

# setup folders
mkdir -v $assets $archive $captation $exp $EFdata
clear

# settings
camera_framePerCaptation=${1-650}

# init
exposure_init
camera_init
timelaps_init

# lanch nega in fs
# /Applications/Firefox.app/Contents/MacOS/firefox http://127.0.0.1:8080/exposure &
# sleep 7

oscSend EF imgReload   # reload picture 
oscSend EF resetTime   # reset timer

say "starting exposure !"

# picture loop
for (( i=$camera_framePerCaptation; i>0; i--)); do

	printf "# $i \n"

	gphoto2 \
 	--capture-image-and-download \
  	--hook-script $app/capture/camera_hook.sh \
  	--filename $exp/%y.%m.%d_%H.%M.%S.%C
done

timelaps_render
timelaps_finish

oscSend /EF kill

say "exposure finished !"