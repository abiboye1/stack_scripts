#!/bin/bash

#This script dynamically pass command line arguments for SOURCE, DESTINATION, and RUNNER, and backup a file to a unique timestamped path that includes a timestamp and runner name 
#Declaring Variables
source=$1
dest=$2
TS=`date "+%m%d%y%H%S"`
RUNNER=$3
destination=${dest}/${RUNNER}/${TS}


#Creating the backup directory
echo "This will create a backup directory called ${dest}"
mkdir -p ${destination}


#Copying file into the backup directory
echo "This will copy ${source} to the backup, ${dest}"
cp -r ${source} ${destination}

#Listing the content of the backup directory
ls -ltr ${destination}
