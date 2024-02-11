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
	if [[ $DISK_UTILIZATION > $THRESHOLD ]]; then
		echo "WARNING!!! Disk utilization is at $DISK_UTILIZATION%, over the $THRESHOLD% threshold"
	else
		echo "Disk utilization is $DISK_UTILIZATION%"
	fi
}

#Main body
#Counting command line argument
if (( $# == 0 )); then
	echo "This script should be run with command line arguments"
#Check the function called
elif [[ $1 == "backup" ]]; then
	echo "Calling the backup function"
	src=$2
	dest=$3
	RUNNER=$4
	TS=`date "+%m%d%y%H%S"`
	destination=$dest/$RUNNER/$TS
	echo "This function has $# command line argument(s)"
	#Providing the runner with usage if the wrong number of command line arguments is provided
	if (( $# != 4 )); then
		echo "USAGE: Enter 4 command line arguments, e.g.,"
		echo "./testargs.sh backup /home/oracle/scripts/practicedir_abi_sep23/file2.txt /home/oracle/scripts/practicedir_abi_sep23/backup1.10 ABIB"
		exit
	fi
	#The backup function when called with the right number of command line argument will run but provide usage if $# is not equal to 4
	backup_f_d $src $destination $RUNNER
elif [[ $1 == "diskcheck" ]]; then
	echo "Calling the disk utilization function"
	THRESHOLD=$2
	DISK=$3
	echo "This function has $# command line argument(s)"
	#Providing the runner with usage if the wrong number of command line arguments is provided
	if (( $# != 3 )); then
		echo "USAGE: Enter 3 command line arguments, e.g.,"
		echo "./testargs.sh discheck 50 /u01"
		exit
	fi
	disk_util $THRESHOLD $DISK
else
	echo "Your entry is not a defined function"
fi 

