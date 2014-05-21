
exp=exp
cd $exp

speed=${1-1}
zoom=${2-1}

# TODO : adapt to movie size : 1888 x 1062 

ffmpeg -f image2 \
-pattern_type glob -i '*.jpg' \
-c:v libx264 -preset ultrafast -qp 0 \
-r 25 -vf "scale=6000:-1, crop=1888:1062:0:0, setpts=(1/1)*PTS" \
-y tmp.mp4

# -framerate 25  \

# replace live movie
cp -f tmp.mp4 live.mp4

