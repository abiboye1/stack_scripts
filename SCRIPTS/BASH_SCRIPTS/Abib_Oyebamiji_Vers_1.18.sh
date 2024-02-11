#!/bin/bash

TS=`date "+%m%d%y%H%M%S"`
#Functions Definition
secure_copy()
{
   #Checking if destination server is a cloud server
	if ( grep "$destination_server" /home/oracle/scripts/practicedir_abi_sep23/cloud_servers.txt ); then
		echo "Destination server is a cloud server"
      #Running the scp command to send file/directory to a cloud server
      #scp -r -i $private_key $source_path $destination_server:$destination_path
		scp -r -i MyEC2KeyPair.pem /home/oracle/scripts/practicedir_abi_sep23/backup ec2-54-84-2-5.compute-1.amazonaws.com:/home/oracle/scripts/practicedir_abi_sep23
   else
      #Running the scp command to send file/directory to an on-prem server
      echo "Destination server is NOT a cloud server"
      scp -r $source_path $destination_server:$destination_path
   fi
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
		#Checking failed exit status in order to send failure email
		if (( $? != 0 )); then
		   echo "Copy command failed"
			echo "Copy command failed! Backup function call was unsuccessful" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
			exit
		else
			echo "Backup to on-prem backup location was successful"
			echo "Backup to on-prem backup location was successful" | mailx -s "Abib's Directory Backup - Email sent!" stackcloud11@mkitconsulting.net
			#List destination directory if copy command succeeds
			ls -ltr $destination
			tar -cvf $destination/$tar_file_$TS.tar * --remove-files
				if (( $? == 0 )); then
					echo "Backup zip successfull"
				fi
			scp -r -i $private_key $destination/$tar_file_$TS.tar $destination_server:$destination_path
				if (( $? == 0 )); then
   				echo "Zipped backup to cloud server was successfull"
					echo "Zipped backup to cloud server was successfull" | mailx -s "Abib's Zip Backup - Email sent!" stackcloud11@mkitconsulting.net
				fi
			#find $dest -name "*$RUNNER*" -mtime 0 -exec ls -ltr *ABIB* {} \;
		fi
}

disk_util()
{
	DISK_UTILIZATION=`df -h | grep $DISK | awk '{print $4}' | sed 's/%//g'`
	disk_util_status=$?
	
	disks="/backup /u01 /u02 /u03 /u04 /u05"
	disk_exist=false

	for disk in $disks
	do
		if [[ $DISK == $disk ]]; then
			disk_exist=true
			echo "Disk exists"
			break
		fi
	done

	if [[ $disk_util_status == 0 && $disk_exist == true ]]; then
		if [[ $DISK_UTILIZATION > $THRESHOLD ]]; then
  			echo "WARNING!!! Disk utilization is at $DISK_UTILIZATION%, over the $THRESHOLD% threshold"
		else
  			echo "Disk utilization is $DISK_UTILIZATION%"
		fi
		echo "Disk utilization function call was successful"
		echo "Disk utilization function call was successful" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	elif (( $disk_util_status != 0 )); then
		echo "Disk utilization function call failed"
		echo "Disk utilization function call failed" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	elif [[ $disk_exist == false ]]; then
		echo "Invalid disk entry! Disk utilization function call failed"
		echo "Invalid disk entry! Disk utilization function call failed" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	fi
}

database_backup()
{
   #Running database environment variable script
   . /home/oracle/scripts/oracle_env_APEXDB.sh
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
	#Taking user inputs for schemas
#	read -p "Enter the list of schemas that you'd like to backup: " SCHEMAS
	schemas=$SCHEMAS
	for x in $schemas
	do
		#Creating a par file 
		echo "userid='/ as sysdba'">export_${x}_${RUNNER}.par
		echo "schemas=${x}">>export_${x}_${RUNNER}.par
		echo "dumpfile=${x}_${RUNNER}_${TS}.dmp">>export_${x}_${RUNNER}.par
		echo "logfile=${x}_${RUNNER}_${TS}.log">> export_${x}_${RUNNER}.par
		echo "directory=${par_directory}">>export_${x}_${RUNNER}.par
		expdp parfile=export_${x}_${RUNNER}.par
		sleep 10
			#Checking exit status for running parameter file
			if (( $? == 0 )); then
				echo "Parameter file ran successfully"
			fi
		#Checking to ensure that schema backup taken is successful
		if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${x}_${RUNNER}_${TS}.log ); then
			echo "Backup completed successfully"
			echo "Backup completed successfully" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
		else
			echo "Backup failed"
		fi
		echo
		echo -e "What else do you want to do: \nzip_backup\nretention_policy\nexit"
		read -p "Enter action: " ACTION
		#Cheking input to know which action to take
		case $ACTION in
			zip_backup)
				echo "Calling tar function"
				#Taking user inputs
				read -p "Enter files path: " path
				read -p "Enter schema name: " SCHEMA_NAME
				read -p "Enter runner: " RUNNER
				#Zipping *abib* files in the backup location
				tar -cvf $path/${SCHEMA_NAME}_${RUNNER}_$TS.tar *abib* 
			;;
			retention_policy)
				echo "Calling retention policy function"
				read -p "Enter files path: " path
				read -p "Enter files name: " NAME
				#Look for files that exceed the rentention period of two days
				echo "The files below are more than two days old"
				find $path -name "*$NAME*" -mtime +2 -exec ls -ltr {} \;
				#Check if user would like to delete the older files
				read -p "Would you like to delete files older than 2 days? Y/N: " INPUT
				if [[ $INPUT == 'Y' ]]; then
				   echo "Deleting older files"
				   find $path -name "*$NAME*" -mtime +2 -exec rm -rf {} \;
  				   #Listing newer files left in the backup directory
				   ls -ltr $path | grep "$NAME"
				else
  				 	exit
				fi		
			;;
			*)
				exit
			;;
		esac
		if [[ $ACTION == "zip_backup" ]]; then 
			echo "Zipping backups"
			zip_backup $path $SCHEMA_NAME $RUNNER
		elif [[ $ACTION == "retention_policy" ]]; then
			echo "Implementing retention policy"
			retention_policy $path $NAME
		else
			echo "Finish and exit"
			exit
		fi
	done
}

#Main body
#Check the function called
if (( $# == 0 )); then
   echo -e "What function would you like to call? \nsecure_copy\ndatabase_backup\nbackup_f_d\ndisk_util"
	read -p "Enter function: " FUNCTION
	case $FUNCTION in
		secure_copy)
			if [[ $FUNCTION == "secure_copy" ]]; then
				echo "Calling secure copy function"
				#Checking if destination server is a cloud server
				read -p "Enter the destination server: " destination_server
				if ( grep "$destination_server" /home/oracle/scripts/practicedir_abi_sep23/cloud_servers.txt ); then
				   echo "Destination server is a cloud server"
   				read -p "Enter the private key: " private_key
   				read -p "Enter the source path: " source_path
   				read -p "Enter the destination path: " destination_path
					secure_copy
				else
   				#Running the scp command to send file/directory to an on-prem server
   				echo "Destination server is NOT a cloud server"
   				read -p "Enter the source path: " source_path
   				read -p "Enter the destination path: " destination_path
   				scp -r $source_path $destination_server:$destination_path
				fi
			fi
		;;
		database_backup)
			if [[ $FUNCTION == "database_backup" ]]; then
				echo "Calling the database_backup function"
				#Prompting users for parameters at runtime
				read -p "Enter the schemas: " SCHEMAS
				read -p "Enter the directory: " par_directory
				read -p "Enter the runner: " RUNNER
				database_backup $SCHEMAS $par_directory $RUNNER
			fi
		;;
		backup_f_d)
			if [[ $FUNCTION == "backup_f_d" ]]; then
				echo "Calling backup function"
				#Prompting users for parameters at runtime
				read -p "Enter backup source e.g. /home/oracle/scripts/practicedir_abi_sep23: " src
				read -p "Enter backup destination e.g. /backup/AWSSEP23/FILE_DIRECTORY_BACKUP: " dest
				read -p "Enter runner: " RUNNER
				read -p "Enter tar file i.e. practicedir_abi_sep23: " tar_file
				read -p "Enter private key e.g. /home/oracle/scripts/MyEC2KeyPair.pem: " private_key
				read -p "Enter destination server e.g. ec2-54-84-2-5.compute-1.amazonaws.com: " destination_server
				read -p "Enter destination path e.g. /home/oracle/scripts/practicedir_abi_sep23: " destination_path
				destination=$dest/$RUNNER/$TS
				backup_f_d $src $destination $RUNNER
			fi
		;;
		disk_util)
			if [[ $FUNCTION == "disk_util" ]]; then
				echo "Calling disk utilization function"
				#Prompting users for parameters at runtime
				read -p "Enter threshold: " THRESHOLD
				read -p "Enter disk: " DISK
				disk_util $THRESHOLD $DISK
			fi
		;;
		*)
			echo "Invalid function called"
		;;
	esac
elif [[ $1 == "secure_copy" ]]; then
	echo "Calling secure copy function"
	destination_server=$4
	if ( grep "$destination_server" /home/oracle/scripts/practicedir_abi_sep23/cloud_servers.txt ); then
   	private_key=$2
   	source_path=$3
   	destination_path=$5
   	#secure_copy ${private_key} ${source_path} ${destination_server}:${destination_path}
   	secure_copy ${private_key} ${source_path} ${destination_server} ${destination_path}
	else
   	source_path=$2
   	destination_path=$3
   	secure_copy ${source_path} ${destination_server}:${destination_path}
	fi
	
	#Providing the runner with usage if the wrong number of command line arguments is provided
	if [[ $# != 4 || $# != 5 ]]; then
   	echo "USAGE: Enter 4 command line arguments if you are doing a secure copy to an on-prem server e.g. \n Enter 5 command line arguments if you are doing a secure copy to a cloud server"
   	echo "./testargs.sh database_backup schema_name directory"
   	exit
	fi
	echo "Calling secure copy function"
	secure_copy 
elif [[ $1 == "database_backup" ]]; then
	echo "Calling the database_backup function"
	SCHEMAS=$2
	par_directory=$3
	RUNNER=$4
	#Providing the runner with usage if the wrong number of command line arguments is provided
	if (( $# != 4 )); then
   	echo "USAGE: Enter 3 command line arguments, e.g.,"
   	echo "./testargs.sh database_backup schema_name directory RUNNER"
   	exit
	fi
	database_backup ${SCHEMAS} ${par_directory} ${RUNNER}
elif [[ $1 == "backup" ]]; then
	echo "Calling the backup function"
	src=$2
	dest=$3
	RUNNER=$4
	tar_file=$5
	private_key=$6
	destination_server=$7
	destination_path=$8
	destination=$dest/$RUNNER/$TS
	echo "This function has $# command line argument(s)"
	#Providing the runner with usage if the wrong number of command line arguments is provided
	if (( $# != 8 )); then
		echo "USAGE: Enter 4 command line arguments, e.g.,"
		echo "./testargs.sh backup /home/oracle/scripts/file2.txt /home/oracle/scripts/backup1.10 ABIB file.tar MyEC2KeyPair.pem ec2-54-84-2-5.compute-1.amazonaws.com /home/oracle/scripts"
		exit
	fi
	#The backup function when called with the right number of command line argument will run but provide usage if $# is not equal to 4
	backup_f_d $src $destination $RUNNER $tar_file $private_key $destination_server $destination_path
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

