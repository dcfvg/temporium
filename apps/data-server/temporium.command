#!/bin/bash
# set -x

vlc='/Applications/VLC.app/Contents/MacOS/VLC'

path="`dirname \"$0\"`"              # relative
path="`( cd \"$path\" && pwd )`"

assets=$path"/../../assets/"
waitingList="$assets/waitinglist/"
archive="$assets/archive/"

captation=$assets"/captation/"
exp="$captation/exp"
live="$exp/live.mp4"

EF=$path"/exposerFlasher"
EFdata="$EF/data/"

mkdir -v $waitingList $archive $EFdata

function runPDE {
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
function runSikuli {
  # run a sikuli automation 
  sikuliIDE="/Applications/SikuliX-IDE.app/Contents/runIDE"
  $sikuliIDE -r $1
}
function negaProcess {
  
  say "processing picture."
  
  convert $waitingList$negaName \
  -resize 1920x1920^ -gravity Center -crop 1920x1080+0+0 \
  -modulate 100,0,100 \
  -auto-level \
  -negate \
  $nega

  # open $nega # for testing
}
function webcamimage {
  # capture countdown
  for (( i=1; i>0; i--)); do
    say "next picture $i minutes" 
    sleep 60
  done

  say "next picture 10 seconds"
  for (( i=10; i>0; i--)); do
    sleep 1
    say "$i"
  done
  
  say "0"

  # capture countdown
  now=$(date +"%y.%m.%d-%H.%M.%S")
  imagesnap "$waitingList/$now.jpg"
}
function newcapation {
  now=$(date +"%y.%m.%d_%H.%M.%S")
  
  mv $exp "$captation/exp-$now"
  mkdir $exp
  
  label="$(date +"%y.%m.%d-%H:%M:%S")"
  #convert -pointsize 36 -size 1920x1080 -gravity center -background black -fill white label:$label "$exp/_000.JPG"
  
  for (( i=50; i>0; i--)); do
    #cp "$exp/_000.JPG" "$exp/_00$i.JPG"
    cp "$captation/_000.JPG" "$exp/_00$i.JPG"
    
	done
}
function timelaps {
  killall -9 "VLC"
  bash $path"/exptomov.sh" &
  sleep 30
}
function lanchvideo {
  killall -9 "VLC"
  $vlc --noaudio --video-x=255 --video-y=0 --width=1025 --height=810 --loop ~/temporium/assets/captation/exp/live.mp4 &
}

# launch animation play/processing

git --git-dir=~/temporium/.git pull

timelaps

while true
do
  newcapation
  lanchvideo
  
  # Take snapshot if no picture
  waitingfiles=$(find $waitingList -type f ! -iname "*sync*" ! -iname "*.DS_Store" -exec printf '.' \; | wc -c  | tr -d ' ')
 
  if [[ $waitingfiles > 0 ]];then
    echo "say $waitingfiles pictures waiting !"
    else
    webcamimage
    sleep 1
  fi

  # get source
  negaSource=$(find $waitingList -maxdepth 1 -iname '*.jpg' | head -1)
  negaName=$(basename $negaSource)x
  nega=$EFdata"last.png"

  # image processing
  negaProcess
  say "starting exposure !"

  # Run projection and automation
  open -a EOS\ Utility.app $scan &
  runPDE $EF present &
  sleep 5
  runSikuli $EF/stagiaire.sikuli

  # remove file from list
  mv -v $waitingList$negaName $archive$negaName
  echo "files in list : "$(ls $waitingList)

  # wait for wash
  say "exposure finished !"
  sleep 120
  say "next exposure in 1 minute"
  sleep 60
  
done