#!/bin/bash
#set -x
# 
# @author Benoît VERJAT
# @since  01.02.2014
#

# make sure the camera is available.
killall PTPCamera 

# launch detection
gphoto2 --auto-detect
gphoto2 --summary

# capture
gphoto2 --capture-image-and-download --interval 2 --frames 30 --hook-script camera_hook.sh --filename ../../assets/exp/-%y.%m.%d_%H.%M.%S.%C