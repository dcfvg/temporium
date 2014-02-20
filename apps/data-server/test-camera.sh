#!/bin/bash
#set -x

# make sure the camera is available.
killall PTPCamera 

# launch detection
gphoto2 --auto-detect
gphoto2 --summary

# capture
gphoto2 --capture-image
gphoto2 --capture-image-and-download