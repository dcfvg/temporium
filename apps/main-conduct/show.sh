#!/bin/bash
#set -x
#
# the temporium main script
#  
# 
# @author Benoît VERJAT
# @since  01.02.2014
#



clear
# settings
camera_interval=0
camera_framePerCaptation=2

# include var and functions for local use
source /Users/immersion/temporium/apps/cli/functions.sh  

# init session
PDE_run $EF run &

# init exposure


exposure_init
camera_init
timelaps_init

say "starting exposure !"
  
PDE_tell img_reload   # reload picture 
PDE_tell reset_time   # reset timer

# tell camera to take picture 
for (( i=$camera_framePerCaptation; i>0; i--)); do
  sleep $camera_interval &
  
  # --interval $camera_interval --frames $camera_framePerCaptation \
  gphoto2 \
  --capture-image-and-download \
  --hook-script $app/capture/hook.sh \
  --filename $exp/%y.%m.%d_%H.%M.%S.%C
done

timelaps_render

say "exposure finished !"