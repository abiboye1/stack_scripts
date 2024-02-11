#!/bin/bash

TS=`date "+%m%d%y%H%S"`
#Functions Definition
secure_copy()
{
   if ( grep "$destination_server" /home/oracle/scripts/practicedir_abi_sep23/cloud_servers.txt ); then
      #Running the scp command to send file/directory to a cloud server
      scp -r -i $private_key $source_path $destination_server:$destination_path
   else
      #Running the scp command to send file/directory to an on-prem server
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
			#List destination directory if copy command succeeds
			ls -ltr $destination
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
		if [[ $DISK_UTILIZATION > $THRESHOLD ]] || [[ $DISK_UTILIZATION == 100 ]]; then
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
      echo "Database login failed"
      exit
   fi
	#Creating a par file 
	echo "userid='/ as sysdba'">export_${RUNNER}.par
	echo "schemas=${par_schema}">>export_${RUNNER}.par
	echo "dumpfile=${par_schema}_${RUNNER}_${TS}.dmp">>export_${RUNNER}.par
	echo "logfile=${par_schema}_${RUNNER}_${TS}.log">> export_${RUNNER}.par
	echo "directory=${par_directory}">>export_${RUNNER}.par
	expdp parfile=export_${RUNNER}.par
		#Checking exit status for running parameter file
		if (( $? == 0 )); then
			echo "Parameter file ran successfully"
		fi
	#Checking to ensure that schema backup taken is successful
	if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${par_schema}_${RUNNER}_${TS}.log ); then
		echo "Backup completed successfully"
		echo "Backup completed successfully" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	else
		echo "Backup failed"
	fi

	#Zipping *abib* files in the backup location
	tar -cvf /backup/AWSSEP23/APEXDB/${par_schema}_${RUNNER}_$TS.tar *abib*

	echo -e "What else do you want to do: \nretention_policy\nexit"
	read -p "Enter action: " ACTION
		if [[ $ACTION == "retention_policy" ]]; then
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
		else
   		echo "Finish and exit"
   		exit
		fi
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
				read -p "Enter the destination server: " destination_server
				#Checks if destination server is a cloud server by checking the cloud_servers.txt list
				if ( grep "$destination_server" /home/oracle/scripts/practicedir_abi_sep23/cloud_servers.txt ); then
   				echo "Destination server is a cloud server"
				   read -p "Enter the private key: " private_key
				   read -p "Enter the source path: " source_path
				   read -p "Enter the destination path: " destination_path
				else
   				echo "Destination server is NOT a cloud server"
				   read -p "Enter the source path: " source_path
				   read -p "Enter the destination path: " destination_path
				fi
				secure_copy
			fi
		;;
		database_backup)
			if [[ $FUNCTION == "database_backup" ]]; then
				echo "Calling the database_backup function"
				#Prompting users for parameters at runtime
				read -p "Enter the schema: " par_schema
				read -p "Enter the directory: " par_directory
				read -p "Enter the runner: " RUNNER
				database_backup $par_schema $par_directory $RUNNER
			fi
		;;
		backup_f_d)
			if [[ $FUNCTION == "backup_f_d" ]]; then
				echo "Calling backup function"
				#Prompting users for parameters at runtime
				read -p "Enter backup source: " src
				read -p "Enter backup destination: " destination
				read -p "Enter runner: " RUNNER
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
<<Comment
       if (( $# != 4 )) || (( $# != 5 )); then
          echo "This function has 4 or 5 command line argument(s)"
          echo "USAGE: Enter 5 command line arguments if your destination server is a cloud server, e.g.,"
         echo "./test.sh secure-copy MyEC2KeyPair.pem /home/oracle/scripts/practicedir_abi_sep23/file1.txt ec2-54-84-2-5.compute-1.amazonaws.com:/home/oracle/scripts/practicedir_abi_sep23"
          echo
          echo "USAGE: Enter 4 command line arguments if your destination server is an on-prem server, e.g.,"
          echo "./test.sh secure-copy /home/oracle/scripts/practicedir_abi_sep23/file1.txt ec2-54-84-2-5.compute-1.amazonaws.com:/home/oracle/scripts/practicedir_abi_sep23"
          exit
       fi
Comment
	secure_copy 
elif [[ $1 == "database_backup" ]]; then
	echo "Calling the database_backup function"
	par_schema=$2
	par_directory=$3
	RUNNER=$4
	database_backup ${par_schema} ${par_directory} ${RUNNER}
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

