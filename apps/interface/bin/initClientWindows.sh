#!/bin/sh

killall -9 "Safari"
killall -9 "Google Chrome"

sleep 3

osascript <<EOF
tell application "Google Chrome"
	open location "http://localhost:8080/exposure"
	activate
	
	delay 2
	
	get bounds of first window
	set bounds of first window to {2500, 0, 3500, 1000}
	
	tell window 1 to enter presentation mode
end tell
EOF

open -a /Applications/Safari.app http://localhost:8080/player

osascript<<EOF	
tell application "System Events"
	tell process "Safari"
   		keystroke "f" using {control down, command down}
   	end tell
end tell
EOF