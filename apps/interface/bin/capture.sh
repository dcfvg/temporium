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
assets="$tempoPath/apps/interface/public/" 	# main assets folder
archive="$assets/archive"                   # media archives

captation=$archive"/exposures"              # exposures archives
exp="$assets/exposure"						# current exposure pictures

function camera_init {
  # make sure the camera is available.
  killall PTPCamera 

  # launch detection
  gphoto2 --auto-detect
  gphoto2 --summary
}
function timelaps_archive {
  timelaps_firstFrame=$(basename $(find $exp -maxdepth 1 -iname '*.jpg' | head -1))
  timelaps_firstFrameName="${timelaps_firstFrame%.*}"
  
  archiveDir="$captation/exp-"$timelaps_firstFrameName"/"
  
  # mouv previous captation to archive
  mkdir archiveDir
  
  mv $exp/*.jpg archiveDir
  mv $exp/data.json archiveDir
}

# init

timelaps_archive
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