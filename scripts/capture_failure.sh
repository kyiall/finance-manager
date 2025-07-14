#!/bin/bash
count=0

while true; do
	((count++))
	./fails_rarely.sh >>output.txt 2>>errors.txt
	if [[ $? -ne 0 ]]; then
		echo "Script failed on run #$count"
		echo "Standard output:"
		cat output.txt
		echo "Standard error:"
		cat errors.txt
		break
	fi
done	
