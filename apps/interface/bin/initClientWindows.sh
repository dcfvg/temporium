
killall -9 "Google Chrome"

sleep 3

open '/Applications/Google Chrome.app'

osascript -e '
tell application "Google Chrome"
	open location "http://localhost:8080/player"
	activate
	
	delay 2
	
	get bounds of first window
	set bounds of first window to {2000, 0, 3000, 1000}
	
	tell window 1 to enter presentation mode
end tell


tell application "Google Chrome"
	make new window
	open location "http://localhost:8080/exposure"
	activate
	
	delay 2
	
	get bounds of first window
	set bounds of first window to {0, 0, 1000, 1000}
	
	tell window 1 to enter presentation mode
end tell
'