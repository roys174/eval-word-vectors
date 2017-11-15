#!/usr/bin/env bash

if [ "$#" -lt "2" ]; then
	echo "Usage: word_sim.py <vector file> <evaluation dir/file> <file proportions>"
	exit -1
elif [ -d $2 ]; then
	python ./all_wordsim.py $1 $2 $3
else
	python ./wordsim.py $1 $2
fi
