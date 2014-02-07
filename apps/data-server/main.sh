#!/bin/bash
# set -x

assets="../../assets/"
waitingList="$assets/waitinglist/"
archive="$assets/archive/"
EF="exposerFlasher"
EFdata="$EF/data/"

mkdir -v $waitingList $archive $EFdata

function runPDE {
  # run a processing sketch 
  if [[ $# -eq 0 ]] ; then
      echo 'warning ! no sketch'
      echo 'runPDE [sketch] [run|present]'
      exit 0
  fi
  
  path="`dirname \"$0\"`"              # relative
  path="`( cd \"$path\" && pwd )`"
  
  patch=$path/$1
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

negaSource=$(find $waitingList -maxdepth 1 -iname '*.jpg' | head -1)
negaName=$(basename $negaSource)
nega=$EFdata"last.png"

negaProcess

# Run projection and automation
open -a EOS\ Utility.app $scan &
runPDE $EF present &
runSikuli $EF/stagiaire.sikuli

mv -v $waitingList$negaName $archive$negaName
echo "files in list : "$(ls $waitingList)