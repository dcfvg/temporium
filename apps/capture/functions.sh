# path definition
# ===============

#set -x
current=$(pwd)
assets="../../assets"                  			  # main assets folder
archive="$assets/archive"                   # media archives

captation=$archive"/exposures"              # exposures archives
exp="$assets/exp"                           # current exposure pictures

EF=$current"/exposerFlasher"            							# exposerFlasher processing patch path
EFdata="$EF/data"                           # exposerFlasher data path

nega_source="$assets/sources/nega.png"
nega_expose="$EFdata/nega.png"

flash_source="$assets/sources/flash.png"      
flash_expose="$EFdata/flash.png"

# function
# ========

# formation captation
function camera_init {
  
  # make sure the camera is available.
  killall PTPCamera 

  # launch detection
  gphoto2 --auto-detect
  gphoto2 --summary
}
function timelaps_init {

  # create new exp folder
  rm -rf $exp
  mkdir $exp

}
function timelaps_render {
  # lauch timelaps render script ( render the animation with ffmpeg)

  cd $exp

  # render mov
  ffmpeg -loglevel panic -f image2 -pattern_type glob -i '*.jpg' -r 25 -vcodec mpeg4 -b 30000k -vf scale=1920:-1 -y tmp.mp4
  
  # replace live movie
  cp -f tmp.mp4 live.mp4

	cd $current
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

# utils
function oscSend {
  # send OSC message to ExposerFlasher 
  set -x
  python $current"/osc/sender.py" 127.0.0.1 4242 $1 $2
  set +x
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

  processing-java --sketch="$patch" --output=$assets/tmp --force --$2
}