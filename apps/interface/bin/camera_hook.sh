#!/bin/bash
#
# waits the camera actions and send OSC orders depending on state
# 
# @author Benoît VERJAT
# @since  01.02.2014
# 

case "$ACTION" in
    init)

        ;;
    start)
        echo "$self: START"
        python osc/sender.py 127.0.0.1 3333 /EF flash
        ;;
    download)
        python osc/sender.py 127.0.0.1 3333 /EF expose
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