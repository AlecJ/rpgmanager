#!/bin/sh
echo "Running entry point CMD: $@"
cd /
for f in /entry.d/* ;
do
	echo "Executing $f"
	source $f
	cd /
done