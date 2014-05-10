
# path definition
# ===============

#set -x

tempoPath="/Users/immersion/temporium"

app="$tempoPath/apps"                       # the scripts folder
assets="$tempoPath/assets"                  # main assets folder
archive="$assets/archive"                   # media archives

captation=$archive"/exposures"              # exposures archives
exp="$assets/exp"                           # current exposure pictures

EF=$app"/capture/exposerFlasher"            # exposerFlasher processing patch path
EFdata="$EF/data"                           # exposerFlasher data path

nega_source="$assets/sources/nega.png"
nega_expose="$EFdata/nega.png"

flash_source="$assets/sources/flash.png"      
flash_expose="$EFdata/flash.png"

vlc='/Applications/VLC.app/Contents/MacOS/VLC' # vlc app path


# function
# ========

# formation captation

function exposure_init {

  # refresh negative image and flash from assets folder
  rm $nega_path $flash_expose
  cp $nega_source $nega_expose
  cp $flash_source $flash_expose
}
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
	# TODO : adapt to movie size : 1888 x 1062 

  ffmpeg -loglevel panic -f image2 -pattern_type glob -i '*.jpg' -r 25 -vcodec mpeg4 -b 30000k -vf scale=1920:-1 -y tmp.mp4
  
  # replace live movie
  cp -f tmp.mp4 live.mp4

	oscSend	life_reload 1
}
function timelaps_display {
  # display the video player window and play live.mp4
  killall -9 "VLC"
  $vlc --noaudio --fullscreen --loop ~/temporium/assets/captation/exp/live.mp4 2> /dev/null &
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

# projected image (nega)
function nega_process {
  
  # convert image to be expose into greyscale, negate and crop it at the right size
  
  convert $nega_listPath$nega_name \
  -resize 1920x1920^ -gravity Center -crop 1920x1080+0+0 \
  -modulate 100,0,100 \
  -auto-level \
  -negate \
  $nega_expose

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

# utils
function oscSend {
  # send OSC message to ExposerFlasher 
  python $app/cli/osc/sender.py 127.0.0.1 4242 $1 $2
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