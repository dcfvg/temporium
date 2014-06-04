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
pwd

nodebin="bin/"
public="public/" 	                          # main public folder
archive="$public/archive"                   # media archives

exposures=$archive"/exposures"              # exposures archives
exp=$public"exposure"						            # current exposure pictures
oscScript=$nodebin"/osc/sender.py"          # osc sender 

function camera_init {
  # make sure the camera is available.
  killall PTPCamera 

  # launch detection
  gphoto2 --auto-detect
  gphoto2 --summary
}
function timelaps_archive {

  now=$(date +"%y.%m.%d-%H.%M.%S")

  archiveDir="$exposures/exp-"$now"/"
  
  # mouv previous exposures to archive
  mkdir $archiveDir
  
  mv $exp/*.jpg $archiveDir
  mv $exp/data.json $archiveDir
}

# init
timelaps_archive
camera_init
python $oscScript 127.0.0.1 3333 /EF flash

say "starting exposure !"

# picture loop
while true;
do
	((i++))
	printf "# $i \n"

	#%y.%m.%d_%H.%M.%S.%C
	photoName=$(printf %04d $i)

	echo $photoName

	gphoto2 \
 	--capture-image-and-download \
  	--hook-script $nodebin/camera_hook.sh \
  	--force-overwrite \
  	--filename "public/exposure/"$photoName".jpg"

  	python $oscScript 127.0.0.1 3333 image_capture $exp/$photoName.jpg

  sleep 2
done