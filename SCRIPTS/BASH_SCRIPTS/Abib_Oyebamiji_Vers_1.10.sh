#!/bin/bash

TS=`date "+%m%d%y%H%S"`
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
		exit
	elif [[ $DISK_UTILIZATION > $THRESHOLD ]] || [[ $DISK_UTILIZATION == 100 ]]; then
		echo "WARNING!!! Disk utilization is at $DISK_UTILIZATION%, over the $THRESHOLD% threshold"
	else
		echo "Disk utilization is $DISK_UTILIZATION%"
	fi
}

#Main body
echo "This script has $# command line arguments"
#Checking the first condition - zero command line argument
if (( $# == 0 )); then
	echo -e "Which function would you like to call? \nbackup\ndiskcheck" 
	read -p "Enter function: " function
	#Checking if the backup function is called	
	if [[ $function == "backup" ]]; then
		echo
		echo "Calling the backup function"
		read -p "Enter the second command line argument: " src
		read -p "Enter the third command line argument: " dest
		read -p "Enter the fourth command line argument: " RUNNER

		destination=$dest/$RUNNER/$TS
		echo
		echo "You entered $src, $dest and $RUNNER as the second, third and fourth command line arguments respectively"
		backup_f_d $src $destination $RUNNER
	#Checking if the disk utilization function is called
	elif [[ $function == "diskcheck" ]]; then
		echo
		echo "Calling the disk utilization function"
		read -p "Enter the second command line argument: " THRESHOLD
		read -p "Enter the third command line argument: " DISK
		echo
		echo "You entered $THRESHOLD and $DISK as your second and third command line arguments"
		disk_util $THRESHOLD $DISK
	else
		echo "You entered an invalid function"
	fi

elif [[ $1 == "backup" ]]; then
	if (( $# == 4 )); then
		echo "Calling backup function"
		#Calling the backup function if the right number of command line argument is entered 
		src=$2
		dest=$3
		RUNNER=$4
		destination=$dest/$RUNNER/$TS
		backup_f_d $src $destination $RUNNER
	else
		#Stating the usage if the number of command line argument is wrong
		echo "USAGE: Enter 4 command line arguments, e.g.,"
		echo "./testargs.sh backup /home/oracle/scripts/practicedir_abi_sep23/file1.txt /home/oracle/scripts/practicedir_abi_sep23/backup1.10 ABIB"
		exit
	fi
elif [[ $1 == "diskcheck" ]]; then
	if (( $# == 3 )); then
		echo "Calling disk utilization function"
		#Calling the disk utilization function if the right number of command line argument is entered
		THRESHOLD=$2
		DISK=$3
		disk_util $THRESHOLD $DISK
	else
		#Stating the usage if the number of command line argument is wrong
		echo "USAGE: Enter 3 command line arguments, e.g.,"
		echo "./testargs.sh diskcheck 50 /u01"
		exit
 	fi
fi
