#!/bin/bash
backup_f_d()
{
	echo "Calling the backup function"
	mkdir -p $destination
		echo "Checking exit status for creating backup destination"
		if (( $? != 0 )); then
			echo "Destination creation failed"
		fi
	#Copying file/directory to a backup location
	cp -r $src $destination
		if (( $? != 0 )); then
		   echo "Copy command failed"
		else
			#List destination directory if copy command succeeds
			ls -ltr $destination
		fi
}

disk_util()
{
	DISK_UTILIZATION=`df -h | grep $DISK | awk '{print $4}' | sed 's/%//g'`
	if (( $? != 0 )); then
		echo "Disk utilization check failed"
	elif [[ $DISK_UTILIZATION > $THRESHOLD ]]; then
		echo "WARNING!!! Disk utilization is at $DISK_UTILIZATION%, over the $THRESHOLD% threshold"
	else
		echo "Disk utilization is $DISK_UTILIZATION%"
	fi
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
	read -p "Enter threshold: " THRESHOLD
	read -p "Enter disk: " DISK
	echo "Calling the disk utilization function"
	disk_util $THRESHOLD $DISK
else
	echo "$1 is not a  defined function"
fi 

