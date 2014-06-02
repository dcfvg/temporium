#!/bin/bash
#set -x
#
# the temporium main script
#  
# 
# @author Benoît VERJAT
# @since  01.02.2014
#
# path definition
# ===============

#set -x

tempoPath="~/Users/immersion/temporium"

app="$tempoPath/apps"                       # the scripts folder
assets="$tempoPath/assets"                  # main assets folder
archive="$assets/archive"                   # media archives

captation=$archive"/exposures"              # exposures archives
exp="$assets/exp"                           # current exposure pictures

function camera_init {
  # make sure the camera is available.
  killall PTPCamera 

  # launch detection
  gphoto2 --auto-detect
  gphoto2 --summary
}
function timelaps_finish {
  timelaps_firstFrame=$(basename $(find $exp -maxdepth 1 -iname '*.jpg' | head -1))
  timelaps_firstFrameName="${timelaps_firstFrame%.*}"

  # mouv previous captation to archive
  mkdir "$captation/exp-"$timelaps_firstFrameName
  
  cp $exp/*.jpg    "$captation/exp-"$timelaps_firstFrameName
  cp $exp/live.mp4 "$captation/exp-$timelaps_firstFrameName/$timelaps_firstFrameName.mp4"
  cp $exp/live.mp4 $assets/timelaps.mp4
}
function oscSend {
  # send OSC message to ExposerFlasher 
  python osc/sender.py 127.0.0.1 3333 $1 $2
}

# init

camera_init
python osc/sender.py 127.0.0.1 3333 /EF flash
python osc/sender.py 127.0.0.1 3333 /EF imgReload   # reload picture 

say "starting exposure !"

# picture loop
while true; 
do
	printf "# $i \n"

	#%y.%m.%d_%H.%M.%S.%C
	photoName=$(printf %04d $i)

	gphoto2 \
 	--capture-image-and-download \
  	--hook-script $app/capture/camera_hook.sh \
  	--force-overwrite \
  	--filename $exp/$photoName

  	python osc/sender.py 127.0.0.1 3333 image_capture $exp/$photoName
done