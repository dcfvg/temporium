function timelaps_render {
  # lauch timelaps render script ( render the animation with ffmpeg)
	
  cd $exp
	
	speed=${1-1}

	# TODO : adapt to movie size : 1888 x 1062 

  ffmpeg -loglevel panic -f image2 -pattern_type glob -i '*.jpg' -r 25 -vcodec mpeg4 -b 30000k -vf scale=1888:-1 -y tmp.mp4
  
  # replace live movie
  cp -f tmp.mp4 live.mp4

	oscSend	life_reload 1
}

exp=../assets/exp
timelaps_render 1