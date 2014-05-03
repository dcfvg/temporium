# path definition

path="`dirname \"$0\"`"               #
path="`( cd \"$path\" && pwd )`"      # get absolute path

assets=$path"/../../assets/"          # main asset folder
nega_listPath="$assets/waitinglist/"  # image to be expose waiting list
archive="$assets/archive/"            # exposed image archives

captation=$assets"/captation/"        # exposures archives
exp="$captation/exp"                  # current exposure pictures
live="$exp/live.mp4"                  # current live timelapse move

EF=$path"/exposerFlasher"             # exposerFlasher processing patch path
EFdata="$EF/data/"                    # exposerFlasher data path

vlc='/Applications/VLC.app/Contents/MacOS/VLC' # vlc app path