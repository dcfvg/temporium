#!/bin/sh

osascript<<EOF	
tell application "Safari"
	activate
	tell application "System Events"
   		keystroke "f" using {control down, command down}
   	end tell
end tell
EOF