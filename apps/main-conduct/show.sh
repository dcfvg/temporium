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
source /Users/immersion/temporium/apps/cli/functions.sh  

# setup folders
mkdir -v $assets $archive $captation $exp $EFdata
clear

# settings
camera_framePerCaptation=5

# init
exposure_init
camera_init
timelaps_init

# lanch nega in fs
PDE_run $EF run &
sleep 5

oscSend EF_imgReload   # reload picture 
oscSend EF_resetTime   # reset timer

say "starting exposure !"

# picture loop
for (( i=$camera_framePerCaptation; i>0; i--)); do

	printf "# $i \n"

	gphoto2 \
 	--capture-image-and-download \
  	--hook-script $app/capture/hook.sh \
  	--filename $exp/%y.%m.%d_%H.%M.%S.%C
done

timelaps_render

oscSend EF_kill

say "exposure finished !"