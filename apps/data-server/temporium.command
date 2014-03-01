#!/bin/bash
#set -x
#
# the temporium main script
#  
# 
# @author Benoît VERJAT
# @since  01.02.2014
#

function nega_process {
  
  # convert image to be expose into greyscale, negate and crop it at the right size
  convert $nega_listPath$nega_name \
  -resize 1920x1920^ -gravity Center -crop 1920x1080+0+0 \
  -modulate 100,0,100 \
  -auto-level \
  -negate \
  $nega_path

  # open $nega # for testing
}
function nega_getWebcam {
  
  # get image from the webcam
  
  # countdown
  say "next picture $i minutes" &
  sleep 60
  say "next picture 10 seconds" &
  for (( i=10; i>0; i--)); do
    sleep 1
    say "$i"
  done
  
  say "0 !" &
  now=$(date +"%y.%m.%d-%H.%M.%S")
  
  # get the image
  imagesnap "$nega_listPath/$now.jpg"
}
function timelaps_render {
  # lauch timelaps render script ( render the animation with ffmpeg)
  bash $path"/exptomov.sh" &
  sleep 15
}
function timelaps_display {
  # display the video player window and play live.mp4
  killall -9 "VLC"
  $vlc --noaudio --fullscreen --loop ~/temporium/assets/captation/exp/live.mp4 2> /dev/null &
}
function PDE_tell {
  # send OSC message to ExposerFlasher 
  python $path/osc/sender.py 127.0.0.1 4242 $1
}
function PDE_run {
  # run a processing sketch 
  if [[ $# -eq 0 ]] ; then
    echo 'warning ! no sketch'
    echo 'runPDE [sketch] [run|present]'
    exit 0
  fi

  patch=$1
  echo "load $patch"

  processing-java --sketch="$patch" --output=/tmp/processing_output --force --$2
}
function camera_init {
  
  # make sure the camera is available.
  killall PTPCamera 

  # launch detection
  gphoto2 --auto-detect
  gphoto2 --summary
}
function capation_init {
  
  now=$(date +"%y.%m.%d_%H.%M.%S")
  
  # mouve previous captation to archive
  mkdir "$captation/exp-$now/"
  
  mv "$exp/*.jpg"  "$captation/exp-$now/"
  cp $exp/live.mp4 "$captation/exp-$now/$now.mp4"
  
  # create new exp folder
  mkdir $exp
  
  # create sequence title  
  label="$(date +"%y.%m.%d-%H:%M:%S")"
  #convert -pointsize 36 -size 1920x1080 -gravity center -background black -fill white label:$label "$exp/_000.JPG" # freetype bug on 'pretneuf', need fix
  
  # duplicate sequence title ( 50 images => 2 sec )
  for (( i=50; i>0; i--)); do
    #cp "$exp/_000.JPG" "$exp/_00$i.JPG"
    cp "$captation/_000.JPG" "$exp/_00$i.jpg"
	done
}

# path definition

path="`dirname \"$0\"`"               #
path="`( cd \"$path\" && pwd )`"      # get absolute path

assets=$path"/../../assets/"          # main asset folder
nega_listPath="$assets/waitinglist/"  # image to be expose waiting list
archive="$assets/archive/"            # exposed image archives

captation=$assets"/captation/"        # exposures archives
exp="$captation/exp"                  # current exposure pictures
live="$exp/live.mp4"                  # current live timelapse move

EF=$path"/exposerFlasher"             # exposerFlasher processing patch path
EFdata="$EF/data/"                    # exposerFlasher data path

vlc='/Applications/VLC.app/Contents/MacOS/VLC' # vlc app path

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
  
  # clean file name in waiting list
  detox -rv $nega_listPath
  
  # get waiting list
  nega_list=$(find $nega_listPath -type f ! -iname "*sync*" ! -iname "*.DS_Store" -exec printf '.' \; | wc -c  | tr -d ' ')
 
  # Take snapshot if no picture in waiting list
  if [[ $nega_list > 0 ]];then
    echo "say $nega_list pictures waiting !"
    else
    nega_getWebcam
    sleep 1
  fi

  # select image to expose
  nega_raw=$(find $nega_listPath -maxdepth 1 -iname '*.jpg' | head -1)
  nega_name=$(basename $nega_raw)
  nega_path=$EFdata"last.png"

  # process image to expose
  say "processing picture."
  nega_process

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
  
  # remove exposed image from waiting list
  mv -v $nega_listPath$nega_name $archive$nega_name

  # waiting for aquarium to be cleaned
  say "exposure finished !"
  sleep 60
  say "next exposure in 1 minute"
  sleep 60
done