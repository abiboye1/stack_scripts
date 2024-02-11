#!/bin/bash

#This script adds a third variable, RUNNER that is included in the path created for the backed directory or file.
#Declaring Variables
source=/home/oracle/scripts/practicedir_abi_sep23/file1.txt
dest=/home/oracle/scripts/practicedir_abi_sep23/backup
TS=`date "+%m%d%y%H%S"`
RUNNER=ABIB
destination=${dest}/${RUNNER}/${TS}


#Creating the backup directory
echo "This will create a backup directory called ${dest}"
mkdir -p ${destination}


#Copying file into the backup directory
echo "This will copy ${source} to the backup, ${dest}"
cp -r ${source} ${destination}

#Listing the content of the backup directory
ls -ltr ${destination}
