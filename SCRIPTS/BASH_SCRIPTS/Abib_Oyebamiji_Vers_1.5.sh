#!/bin/bash

#Declaring functions
backup_f_d()
{
	echo "Calling the backup function"
	#Copying file/directory to a backup location
	mkdir -p $destination
	cp -r $src $destination
	ls -ltr $destination
}

disk_util()
{
	df -h
}

if [[ $1 == "backup" ]]; then
	echo "Call backup_f_d"
	src=$2
	dest=$3
	RUNNER=$4
	TS=`date "+%m%d%y%H%S"`
	destination=$dest/$RUNNER/$TS
	backup_f_d $src $destination
elif [[ $1 == "diskcheck" ]]; then
	echo "Calling the disk utilization function"
	THRESHOLD=$2
	disk_util $THRESHOLD
else
	echo "$1 is not a  defined function"
fi 

