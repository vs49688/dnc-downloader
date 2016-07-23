#!/bin/bash

# curl -OJL https://wikileaks.org/dnc-emails//get/<id-here>
# IDs range from [1, 22456]

OUTPUT_FILE="dncdownload.log"
rm -rf eml output $OUTPUT_FILE

exec {FD}>$OUTPUT_FILE

mkdir eml output
cd eml
mkdir tmp
cd tmp

for i in {1..22456}; do
	echo "Downloading $i..." | tee -a /dev/fd/$FD
	curl -OJL "https://wikileaks.org/dnc-emails//get/$i" > "../../output/$i.stdout" 2> "../../output/$i.stderr"
	CURLRET=$?

	if [ $CURLRET -ne 0 ]; then
		rm -rf *
		echo " * Failed to download: cURL returned $CURLRET. See output/$i.stderr for more information." | tee -a /dev/fd/$FD
		break
	fi

	EMLFILE=`ls -1 | head -1`

	EXT=${EMLFILE,,}
	EXT=${EXT##*.}
	if [ "${EXT}" != "eml" ]; then
		rm -rf *
		echo " * Failed to download: File unavailable, try again." | tee -a /dev/fd/$FD
		break
	fi

	OUTFILE=`printf "%05d" $i`_$EMLFILE
	mv "$EMLFILE" "../$OUTFILE"
done

cd ..
rm -rf tmp
