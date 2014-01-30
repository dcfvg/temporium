#!/bin/bash
# set -x

assets="../../assets/"
waitingList="$assets/waitinglist/"
archive="$assets/archive/"

mkdir -v $waitingList $archive

function runPDE {
  # run a processing sketch 
  if [[ $# -eq 0 ]] ; then
      echo 'warning ! no sketch'
      echo 'runPDE [sketch] [run|present]'
      exit 0
  fi
  patch=$(pwd)/$1
  processing-java --sketch="$patch" --output=/tmp/processing_output --force --$2
}
function runSikuli {
  # run a sikuli automation 
  sikuliIDE="/Applications/SikuliX-IDE.app/Contents/runIDE"
  $sikuliIDE -r $1
}

runPDE Bezier run &
ls /