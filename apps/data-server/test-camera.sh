#!/bin/bash
#set -x

# make sure the camera is available.
killall PTPCamera 

# launch detection
gphoto2 --auto-detect
gphoto2 --summary

# capture
gphoto2 --capture-image-and-download --interval 5 --frames 3 --hook-script hook.sh --filename ../../assets/exp/-%y.%m.%d_%H.%M.%S.%C