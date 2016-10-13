#!/bin/bash

# curl -OJL https://wikileaks.org/podesta-emails//get/<id-here>
# IDs range from [1, 9077]

OUTPUT_FILE="podestadownload.log"
RETRY_TIMEOUT=1
RETRY_COUNT=2

rm -rf eml output $OUTPUT_FILE

exec {FD}>$OUTPUT_FILE

FD_PATH="/dev/fd/$FD"

mkdir eml output
cd eml
mkdir tmp
cd tmp

i=0
r=$RETRY_COUNT

while ((i <= 22456)); do
#for i in {1..22456}; do
	let i=i+1
	echo "Downloading $i..." | tee -a $FD_PATH
	curl -OJL "https://wikileaks.org/podesta-emails//get/$i" > "../../output/$i.stdout" 2> "../../output/$i.stderr"
	CURLRET=$?

	if [ $CURLRET -ne 0 ]; then
		rm -rf *
		echo " * Failed to download: cURL returned $CURLRET. See output/$i.stderr for more information." | tee -a $FD_PATH
		continue
	fi

	EMLFILE=`ls -1 | head -1`

	EXT=${EMLFILE,,}
	EXT=${EXT##*.}

	# This usually happens if we hit Wikileaks too fast, so just retry until it lets us.
	if [ "${EXT}" != "eml" ]; then
		rm -rf *
		echo " * Failed to download: File unavailable, trying again in $RETRY_TIMEOUT second(s)..." | tee -a $FD_PATH

		if [ $r -ne 0 ]; then
			let i=i-1
			let r=r-1
			sleep $RETRY_TIMEOUT
		else
			echo " * Failed to download: File unavailable, exceeded retry count. Skipping..." | tee -a $FD_PATH
			r=$RETRY_COUNT
		fi

		continue
	fi

	r=$RETRY_COUNT

	OUTFILE=`printf "%05d" $i`_$EMLFILE
	mv -- "$EMLFILE" "../$OUTFILE"
done

cd ..
rm -rf tmp
