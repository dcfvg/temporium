#!/bin/bash
#set -x

vlc='/Applications/VLC.app/Contents/MacOS/VLC'

path="`dirname \"$0\"`"              # relative
path="`( cd \"$path\" && pwd )`"

assets=$path"/../../assets/"
nega_listPath="$assets/waitinglist/"
archive="$assets/archive/"

captation=$assets"/captation/"
exp="$captation/exp"
live="$exp/live.mp4"

EF=$path"/exposerFlasher"
EFdata="$EF/data/"

mkdir -v $nega_listPath $archive $EFdata

function nega_process {
  convert $nega_listPath$nega_name \
  -resize 1920x1920^ -gravity Center -crop 1920x1080+0+0 \
  -modulate 100,0,100 \
  -auto-level \
  -negate \
  $nega_path

  # open $nega # for testing
}
function nega_getWebcam {
  # capture countdown
  say "next picture $i minutes" &
  sleep 60

  say "next picture 10 seconds" &
  
  for (( i=10; i>0; i--)); do
    sleep 1
    say "$i"
  done
  
  say "0 !" &
  now=$(date +"%y.%m.%d-%H.%M.%S")
  imagesnap "$nega_listPath/$now.jpg"
}
function timelaps_render {
  bash $path"/exptomov.sh" &
  sleep 15
}
function timelaps_display {
  killall -9 "VLC"
  $vlc --noaudio --fullscreen --loop ~/temporium/assets/captation/exp/live.mp4 2> /dev/null &
}
function PDE_tell {
  python $path/osc/sender.py sender.py 127.0.0.1 4242 $1
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
  
  mkdir "$captation/exp-$now/"
  
  mv "$exp/*.jpg"  "$captation/exp-$now/"
  cp $exp/live.mp4 "$captation/exp-$now/$now.mp4"
  mkdir $exp
  
  label="$(date +"%y.%m.%d-%H:%M:%S")"
  #convert -pointsize 36 -size 1920x1080 -gravity center -background black -fill white label:$label "$exp/_000.JPG"
  
  for (( i=50; i>0; i--)); do
    #cp "$exp/_000.JPG" "$exp/_00$i.JPG"
    cp "$captation/_000.JPG" "$exp/_00$i.jpg"
	done
}

camera_interval=0
camera_framePerCaptation=1000

PDE_run $EF run &

while true
do
  
  # init
  capation_init
  camera_init
  
  # Take snapshot if no picture
  detox -rv $nega_listPath
  nega_list=$(find $nega_listPath -type f ! -iname "*sync*" ! -iname "*.DS_Store" -exec printf '.' \; | wc -c  | tr -d ' ')
 
  if [[ $nega_list > 0 ]];then
    echo "say $nega_list pictures waiting !"
    else
    nega_getWebcam
    sleep 1
  fi

  # get source
  nega_raw=$(find $nega_listPath -maxdepth 1 -iname '*.jpg' | head -1)
  nega_name=$(basename $nega_raw)
  nega_path=$EFdata"last.png"

  # image processing
  say "processing picture."
  nega_process

  # Run projection and automation
  say "starting exposure !"
  
  timelaps_display
  
  PDE_tell img_reload
  PDE_tell reset_time
  
  for (( i=$camera_framePerCaptation; i>0; i--)); do
    sleep $camera_interval &
    
    # --interval $camera_interval --frames $camera_framePerCaptation \
    gphoto2 \
    --capture-image-and-download \
    --hook-script $path/hook.sh \
    --filename ~/temporium/assets/exp/%y.%m.%d_%H.%M.%S.%C
  done
  
  # remove file from list
  mv -v $nega_listPath$nega_name $archive$nega_name

  # wait for wash
  say "exposure finished !"
  sleep 60
  say "next exposure in 1 minute"
  sleep 60
done