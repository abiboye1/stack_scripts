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
		#Checking failed exit status in order to send failure email
		if (( $? != 0 )); then
		   echo "Copy command failed"
			echo "Copy command failed! Backup function call was unsuccessful" | mailx -s "Abib: Email sent!" stackcloud11@mkitconsulting.net
			exit
		else
			echo "Copy command succeeded"
			echo "Copy command succeeded! Backup function call was unsuccessful" | mailx -s "Abib: Email sent!" stackcloud11@mkitconsulting.net 
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
	#Capture the exit status of disk utilization function
	disk_util_status=$?
	
	disks="/backup /u01 /u02 /u03 /u04 /u05"
	disk_exist=False

	for disk in $disks
	do
		if [[ $DISK == $disk ]]; then
			disk_exist=True
			echo "Disk utilization check successful"
			break
		fi
	done

	if (( $disk_util_status == 0 && $disk_exist )); then
		echo "Disk utilization function call was successful"
		echo "Disk utilization function call was successful" | mailx -s "Abib: Email sent!" stackcloud11@mkitconsulting.net
	elif (( $disk_util_status != 0 )); then
		echo "Disk utilization function call failed"
		echo "Disk utilization function call failed" | mailx -s "Abib: Email sent!" stackcloud11@mkitconsulting.net
	elif [[ $disk_exist == False ]]; then
		echo "Invalid disk entry! Disk utilization function call failed"
		echo "Invalid disk entry! Disk utilization function call failed" | mailx -s "Abib: Email sent!" stackcloud11@mkitconsulting.net
	fi
#Comment
}

database_backup()
{
   #Running database environment variable script
   . /home/oracle/scripts/oracle_env_APEXDB.sh
	TS=`date "+%m%d%y%H%S"`
   #Checking conditions to see that database instance is up
   if ( ps -ef |grep pmon |grep APEXDB ); then
      echo "Log into the APEXDB database if the conditions above are true"
      sqlplus stack_temp/stackinc@APEXDB<<EOF
      set echo on feedback on
      spool /home/oracle/scripts/practicedir_abi_sep23/db_status.log
      show user;
      select * from global_name;
      select status from v\$instance;
      spool off
EOF
			#Checking exit status for database login
			if (( $? == 0 )); then
   			echo "Database login was successful"
			fi
		if ( grep "OPEN" /home/oracle/scripts/practicedir_abi_sep23/db_status.log ); then
			echo "Database is open and login was successful"
		else
			echo "Database is not open"
			exit
		fi
   else
      echo "Database instance is NOT running"
      exit
   fi
	#Creating a par file 
	echo "userid='/ as sysdba'">export1.13_${RUNNER}.par
	echo "schemas=${par_schemas}">>export1.13_${RUNNER}.par
	echo "dumpfile=${par_schemas}_${RUNNER}_${TS}.dmp">>export1.13_${RUNNER}.par
	echo "logfile=${par_schemas}_${RUNNER}_${TS}.log">> export1.13_${RUNNER}.par
	echo "directory=${par_directory}">>export1.13_${RUNNER}.par
	expdp parfile=export1.13_${RUNNER}.par
		#Checking exit status for running parameter file
		if (( $? == 0 )); then
			echo "Parameter file ran successfully"
		fi
	#Checking to ensure that schema backup taken is successful
	if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${par_schemas}_${RUNNER}_${TS}.log ); then
		echo "Backup completed successfully"
		echo "Backup completed successfully" | mailx -s "Abib: Email sent!" stackcloud11@mkitconsulting.net
	else
		echo "Backup failed"
	fi
}

#Main body
#Check the function called
if (( $# == 0 )); then
	echo -e "Which function would you like to call? \ndatabase_backup\nbackup\ndiskcheck"
	read -p "Enter function here: " function
	#Checking if the database backup function is called
	if [[ $function == "database_backup" ]]; then
   	echo "Calling the backup function"
   	read -p "Enter the second command line argument: " par_schemas
   	read -p "Enter the third command line argument: " par_directory
   	read -p "Enter the fourth command line argument: " RUNNER
   	database_backup ${par_schemas} ${par_directory}
   #Checking if the backup function is called
   elif [[ $function == "backup" ]]; then
      echo "Calling the backup function"
      read -p "Enter the second command line argument: " src
      read -p "Enter the third command line argument: " dest
      read -p "Enter the fourth command line argument: " RUNNER

      TS=`date "+%m%d%y%H%S"`
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
	par_schemas=$2
	par_directory=$3
	RUNNER=$4
	#Providing the runner with usage if the wrong number of command line arguments is provided
	if (( $# != 4 )); then
   	echo "USAGE: Enter 4 command line arguments, e.g.,"
   	echo "./testargs.sh database_backup stack_temp DATA_PUMP_DIR ABIB"
   	exit
	fi
	#The database backup function when called with the right number of command line argument will run but provide usage if $# is not equal to 4
	database_backup ${par_schemas} ${par_directory} ${RUNNER}
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
	#Checking exit status of backup function to send success or failure email
	if (( $? == 0 )); then
		echo "Backup function was called successfully"
		echo "Backup function was called successfully" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	fi
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

