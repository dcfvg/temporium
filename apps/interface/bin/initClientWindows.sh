#!/bin/sh

killall -9 "Safari"
killall -9 "Google Chrome"

sleep 3

osascript <<EOF
tell application "Safari"
	activate
	make new document with properties {URL : "http://localhost:8080/player"}
    tell application "System Events"
    	tell process "Safari"
       		keystroke "f" using {control down, command down}
       	end tell
    end tell
end tell

tell application "Google Chrome"
	open location "http://localhost:8080/exposure"
	activate
	
	delay 2
	
	get bounds of first window
	set bounds of first window to {0, 0, 1000, 1000}
	
	tell window 1 to enter presentation mode
end tell
EOF