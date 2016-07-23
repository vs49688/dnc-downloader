#!/bin/bash

# curl -OJL https://wikileaks.org/dnc-emails//get/<id-here>
# IDs range from [1, 22456]

rm -rf eml output
mkdir eml
mkdir output
cd eml

for i in {1..22456};
do
	echo "Downloading $i..."
	curl -OJL "https://wikileaks.org/dnc-emails//get/$i" > "../output/$i.stdout" 2> "../output/$i.stderr";
done
