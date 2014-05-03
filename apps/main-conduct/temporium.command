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
source ../path.sh
source ../cli/functions.sh	

# settings
camera_interval=0
camera_framePerCaptation=1000

# init session
mkdir -v $assets $nega_listPath $captation $archive $EFdata
PDE_run $EF run &

# lanch
while true 
do
  
  # init exposure
  capation_init
  camera_init
  
  say "starting exposure !"
    
  PDE_tell img_reload   # reload picture 
  PDE_tell reset_time   # reset timer
  
  # tell camera to take picture 
  for (( i=$camera_framePerCaptation; i>0; i--)); do
    sleep $camera_interval &
    
    # --interval $camera_interval --frames $camera_framePerCaptation \
    gphoto2 \
    --capture-image-and-download \
    --hook-script $path/hook.sh \
    --filename ~/temporium/assets/captation/exp/%y.%m.%d_%H.%M.%S.%C
  done

  # waiting for aquarium to be cleaned
  say "exposure finished !"
done