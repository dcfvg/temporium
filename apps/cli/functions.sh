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
