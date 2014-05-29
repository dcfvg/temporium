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

# settings
camera_framePerCaptation=${1-650}

# init
camera_init

oscSend EF imgReload   # reload picture 
oscSend EF resetTime   # reset timer

say "starting exposure !"

# picture loop
for (( i=$camera_framePerCaptation; i>0; i--)); do

	printf "# $i \n"

	#%y.%m.%d_%H.%M.%S.%C
	photoName=$(printf %04d $i)

	gphoto2 \
 	--capture-image-and-download \
  	--hook-script $app/capture/camera_hook.sh \
  	--filename $exp/$photoName

  	oscSend EF_picture $i $exp/$photoName

done

say "exposure finished !"