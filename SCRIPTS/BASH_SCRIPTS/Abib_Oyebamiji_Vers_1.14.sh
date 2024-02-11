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
		echo "Disk utilization function call was successful" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	elif (( $disk_util_status != 0 )); then
		echo "Disk utilization function call failed"
		echo "Disk utilization function call failed" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	elif [[ $disk_exist == False ]]; then
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
      echo "Database login failed"
      exit
   fi
	#Creating a par file 
	echo "userid='/ as sysdba'">export1.14_abib.par
	echo "schemas=${par_schemas}">>export1.14_abib.par
	echo "dumpfile=${par_schemas}_abib_${TS}.dmp">>export1.14_abib.par
	echo "logfile=${par_schemas}_abib_${TS}.log">> export1.14_abib.par
	echo "directory=${par_directory}">>export1.14_abib.par
	expdp parfile=export1.14_abib.par
		#Checking exit status for running parameter file
		if (( $? == 0 )); then
			echo "Parameter file ran successfully"
		fi
	#Checking to ensure that schema backup taken is successful
	if ( grep "successfully completed" /backup/AWSSEP23/APEXDB/${par_schemas}_abib_${TS}.log ); then
		echo "Backup completed successfully"
		echo "Backup completed successfully" | mailx -s "Email sent!" stackcloud11@mkitconsulting.net
	else
		echo "Backup failed"
	fi
}

#Main body
#Check the function called
if (( $# == 0 )); then
	echo -e "What function would you like to call? \nsecure_copy\ndatabase_backup\nbackup_f_d\ndisk_util"
   read -p "Enter the function: " function
	#Checking if secure copy function is called
	if [[ $function == "secure_copy" ]]; then
   	echo "Calling secure copy function"
		read -p "Enter the destination server: " destination_server
		#Checks if destination server is a cloud server by checking the cloud_servers.txt list
		if ( grep "$destination_server" /home/oracle/scripts/practicedir_abi_sep23/cloud_servers.txt ); then
		#if ( grep "*amazonaws.com" $destination_server ); then
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
elif [[ $1 == "database_backup" ]]; then
	echo "Calling the database_backup function"
	par_schemas=$2
	par_directory=$3
	database_backup ${par_schemas} ${par_directory}
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

