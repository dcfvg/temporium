pwd 

for (( i=10000; i>0; i--)); do
	sleep 1 &
	printf "next shot in $i s \r"
	wait
done