#!/bin/bash
#
# waits the camera actions and send OSC orders depending on state
# 
# @author Benoît VERJAT
# @since  01.02.2014
# 


source functions.sh  

self=`basename $0`

case "$ACTION" in
    init)

        ;;
    start)
        echo "$self: START"
        oscSend EF_flash
        ;;
    download)
        oscSend EF_expose
        echo "$self: DOWNLOAD to $ARGUMENT" 
        ;;
    stop)
        echo "$self: STOP"
        ;;
    *)
        echo "$self: Unknown action: $ACTION"
        ;;
esac

exit 0