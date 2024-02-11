#!/bin/bash

#This script statically backs up a file to a backup location.
#Declaring Variables
source=/home/oracle/scripts/practicedir_abi_sep23/file1.txt
dest=/home/oracle/scripts/practicedir_abi_sep23/backup
TS=`date "+%m%d%y%H%M%S"`
destination=${dest}/${TS}


#Creating the backup directory
echo "This will create a backup directory called ${dest}"
mkdir -p ${destination}


#Copying file into the backup directory
echo "This will copy ${source} to the backup, ${dest}"
cp ${source} ${destination}

#Listing the content of the backup directory
ls -ltr ${destination}
