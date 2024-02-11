#!/bin/bash

#This script backup directories as well as files to a backup location.
#Declaring Variables
TS=`date "+%m%d%y%H%S"`
source=/home/oracle/scripts/practicedir_abi_sep23/file1.txt
dest=/home/oracle/scripts/practicedir_abi_sep23/backup
destination=${dest}/${source}_${TS}


#Creating the backup directory
echo "This will create a backup directory called ${dest}"
mkdir -p ${destination}

#Copying file into the backup directory
echo "This will copy ${source} to the backup, ${dest}"
cp -r ${source} ${destination}

#Listing the content of the backup directory
ls -ltr ${destination}
