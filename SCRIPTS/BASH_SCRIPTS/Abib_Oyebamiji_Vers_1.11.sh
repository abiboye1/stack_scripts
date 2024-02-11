#!/bin/bash
TS=`date '+%m%d%y%H%M%S'`
database_backup()
{
	#Running database environment variable script
	. /home/oracle/scripts/oracle_env_APEXDB.sh
	cat<<EOF > expdp_stack_temp_abib.par
	userid='/ as sysdba'
	schemas=stack_temp
	dumpfile=stack_temp_abib_$TS.dmp	
	logfile=stack_temp_abib_$TS.log
	directory=DATA_PUMP_DIR
EOF
	#expdp parfile=expdp2_stack_temp.par
#	echo "mv /backup/AWSSEP23/APEXDB/stacktemp_dump_abib.log /backup/AWSSEP23/APEXDB/stacktemp_dump_abib_${TS}.log"
#	echo "mv /backup/AWSSEP23/APEXDB/stacktemp_dump_abib.dmp /backup/AWSSEP23/APEXDB/stacktemp_dump _abib_${TS}.dmp"
#	logfile="/backup/AWSSEP23/APEXDB/stacktemp_dump_abib.log"
#	dumpfile="/backup/AWSSEP23/APEXDB/stacktemp_dump_abib.dmp"
#	sed -i 's/stacktemp_dump_abib.log/stacktemp_dump_abib_$TS.log/g' /backup/AWSSEP23/APEXDB/*.log
#	sed -i 's/stacktemp_dump_abib.dmp/stacktemp_dump_abib_$TS.dmp/g' /backup/AWSSEP23/APEXDB/*.dmp
#	rename "stacktemp_dump_abib.dmp" "stacktemp_dump_abib_$TS.dmp" $directory/*.dmp
#	rename "stacktemp_dump_abib.log" "stacktemp_dump_abib_$TS.log" $directory/*.log
	#sed -i 's/"/backup/AWSSEP23/APEXDB/stacktemp_dump_abib.log"/"/backup/AWSSEP23/APEXDB/stacktemp_dump_abib_$TS.log"/g' expdp2_stack_temp.par
	#sed -i 's/"/backup/AWSSEP23/APEXDB/stacktemp_dump_abib.dmp"/"/backup/AWSSEP23/APEXDB/stacktemp_dump_abib_$TS.dmp"/g' expdp2_stack_temp.par
	expdp parfile=expdp_stack_temp_abib.par
}

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
#Check the function called
if (( $# == 0 )); then
	echo -e "Which function would you like to call? \ndatabase_backup\nbackup\ndiskcheck"
	read -p "Enter function: " function
	#Checking if the database backup function is called
	if [[ $function == "database_backup" ]]; then
   	echo "Calling the backup function"
		database_backup
   #Checking if the backup function is called
   elif [[ $function == "backup" ]]; then
      echo "Calling the backup function"
      read -p "Enter the second command line argument: " src
      read -p "Enter the third command line argument: " dest
      read -p "Enter the fourth command line argument: " RUNNER

      destination=$dest/$RUNNER/$TS
      echo "You entered $src, $dest and $RUNNER as the second, third and fourth command line arguments respectively"
      backup_f_d $src $destination $RUNNER
   #Checking if the disk utilization function is called
   elif [[ $function == "diskcheck" ]]; then
      echo
      echo "Calling the disk utilization function"
      read -p "Enter the second command line argument: " THRESHOLD
      read -p "Enter the third command line argument: " DISK
      echo "You entered $THRESHOLD and $DISK as your second and third command line arguments"
      disk_util $THRESHOLD $DISK
   else
      echo "You entered an invalid function"
   fi
elif [[ $1 == "database_backup" ]]; then
	echo "Calling the database_backup function"
	if (( $# != 1 )); then
   	echo "USAGE: Enter 1 command line argument, e.g.,"
   	echo "./testargs.sh database_backup"
   	exit
	fi
	database_backup
elif [[ $1 == "backup" ]]; then
	echo "Calling the backup function"
	src=$2
	dest=$3
	RUNNER=$4
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

