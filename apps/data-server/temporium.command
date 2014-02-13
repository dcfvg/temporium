#!/bin/bash
# set -x

vlc='/Applications/VLC.app/Contents/MacOS/VLC'

path="`dirname \"$0\"`"              # relative
path="`( cd \"$path\" && pwd )`"

assets=$path"/../../assets/"
waitingList="$assets/waitinglist/"
archive="$assets/archive/"
captation="/Users/etudiant/Desktop/temporium/assets/captation/"
live="$captation/exp/live.mp4"
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

# launch animation play/processing
killall -9 "VLC"
bash "$captation/exptomov.sh" &
$vlc --noaudio --video-x=255 --video-y=0 --width=1025 --height=810 --loop /Users/etudiant/Desktop/temporium/assets/captation/exp/live.mp4 &

while true
do

  # Take snapshot if no picture
  waitingfiles=$(find $waitingList -type f ! -iname "*sync*" -exec printf '.' \; | wc -c  | tr -d ' ')
 
  if [[ $waitingfiles > 0 ]];then
    echo "say $waitingfiles pictures waiting !"
    else
    webcamimage
    sleep 1
  fi

  # get source
  negaSource=$(find $waitingList -maxdepth 1 -iname '*.jpg' | head -1)
  negaName=$(basename $negaSource)
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
  sleep 300

done