#!/bin/bash
backup_f_d()
{
	echo "Calling the backup function"
	mkdir -p $destination
		echo "Checking exit status for creating backup destination"
		if (( $? != 0 )); then
			echo "Destination creation failed"
			exit
		fi
	#Copying file/directory to a backup location
	cp -r $src $destination
		if (( $? != 0 )); then
		   echo "Copy command failed"
			exit
		else
			#List destination directory if copy command succeeds
			ls -ltr $destination
		fi
}

disk_util()
{
	df -h
		if (( $? != 0 )); then
   		echo "Disk utilization check failed"
   		exit
		fi
}

function=$1
if [[ $function == "backup" ]]; then
	echo "Call backup_f_d"
	src=$2
	dest=$3
	RUNNER=$4
	TS=`date "+%m%d%y%H%S"`
	destination=$dest/$RUNNER/$TS
	backup_f_d $src $destination
elif [[ $function == "diskcheck" ]]; then
	echo "Calling the disk utilization function"
	THRESHOLD=$2
	disk_util $THRESHOLD
else
	echo "$function is not a  defined function"
fi 

