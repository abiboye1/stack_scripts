#!/usr/bin/python

import stack_modules_v1_11 as sm, sys


def stack_modules_function():
	# Decision number indicates the function the user decides to call.
	# 1 --> Backup function
	# 2 --> Database backup function
	# 3 --> Disk utilization function
	# 4 --> Gzip function
	# 5 --> Unzipp function
	# 6 --> Database import function	

	# Checking if no command line arguments are called
	if len(sys.argv) - 1 == 0:
		print("You entered {} arguments".format(len(sys.argv) - 1))
		print("This script requires you to pass at least one command line argument. Enter:")
		print("\n1 for Backup function\n2 for Database backup function\n3 for Disk utilization function\n4 for Gzip function")
		exit()
	decision_no = sys.argv[1]

	# CALLING THE BACKUP FUNCTION
	#Checking decision for backup function call
	if decision_no == "1": # Backup function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			print("You chose to call the backup function")
			source = input("Enter backup source: ")
			destination = input("Enter backup destination: ")
			bk_type = input("Enter backup type: ")
			TO_EMAIL = input("Enter recipient email: ")
			SUBJECT = input("Enter email subject: ")
			BODY = "Backup Successful!!!"
			try:
				sm.backup_function(source, destination, bk_type)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Backup failed!!!"
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Backup failed!!!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 6:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 6 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 1 /home/oracle/scripts/practicedir_abi_sep23/file1.txt /home/oracle/scripts/practicedir_abi_sep23/backup_location f")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 6:
			source=sys.argv[2]
			destination=sys.argv[3]
			bk_type=sys.argv[4]
			TO_EMAIL=sys.argv[5]
			SUBJECT = sys.argv[6]
			BODY = "Backup Successful!!!"
			try:
				sm.backup_function(source, destination, bk_type)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Backup failed!!! Failed to copy {} to {}".format(source, destination)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Backup failed!!!")

	# CALLING THE DATABASE BACKUP FUNCTION
	#Checking decision for database backup function call
	elif decision_no == "2": # Database backup function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			practicedir = input("Enter the practicedir: ")
			backup_location = input("Enter the backup_location: ")
			RUNNER = input("Enter the runner name: ")
			schemas = input("Enter the schema name(s): ")
			TO_EMAIL = input("Enter recipient email: ")
			SUBJECT = input("Enter email subject: ")
			BODY = "Database backup successful!!!"	
			try:
				sm.database_backup_function(practicedir, backup_location, RUNNER, schemas)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Export failed!!! Failed to export {} schema".format(schemas)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Export failed!!!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 7:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 7 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 2 /home/oracle/scripts/practicedir_abi_sep23 /backup/AWSSEP23/APEXDB ABIB stack_temp") 
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 7:
			practicedir=sys.argv[2]
			backup_location=sys.argv[3]
			RUNNER=sys.argv[4]
			schemas=sys.argv[5]
			TO_EMAIL=sys.argv[6]
			SUBJECT = sys.argv[7]
			BODY = "Database backup Successful!!!"
			try:
				sm.database_backup_function(practicedir, backup_location, RUNNER, schemas)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Export failed!!! Failed to export {} schema".format(schemas)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Export failed!!!")

	# CALLING THE DISK UTILIZATION FUNCTION
	#Checking decision for disk utilization function call
	elif decision_no == "3": # Disk utilization function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			disk = input("Enter the disk you'd like to check: ")
			threshold = input("Specify the disk utilization threshold: ")
			TO_EMAIL = input("Enter recipient email: ")
			SUBJECT = input("Enter email subject: ")
			BODY = "Disk check successful!!!\nDisk utilization is {}%  and threshold is {}%".format(disk_utilization, threshold)
			try:
				sm.disk_maintenance_check_on_prem(disk, threshold)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Disk check failed!!! Failed to check threshold against disk usage"
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Disk utilization check error!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 5:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.7 3 /u01 50")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 5:
			disk = sys.argv[2]
			threshold = sys.argv[3]
			TO_EMAIL = sys.argv[4]
			SUBJECT = sys.argv[5]
			#BODY = "Disk check successful!!!\nDisk utilization is {}% and threshold is {}%".format(disk_utilization, threshold)
			BODY = "Disk check successful!!!"
			try:
				sm.disk_maintenance_check_on_prem(disk, threshold)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Disk check failed!!! Failed to check threshold against disk usage"
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Disk utilization check error!")

	# CALLING THE GZIP FUNCTION
	#Checking decision for Gzip function call
	elif decision_no == "4": # Gzip function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			source_path = input("Enter the path of the file or directory you want to compress: ")
			output_gzip = input("Enter the path for the compressed output: ")
			TO_EMAIL = input("Enter recipient email: ")
			SUBJECT = input("Enter email subject: ")
			BODY = "Gzip successful!!!\n{} was successfully zipped and renamed {}".format(source_path, output_gzip)
			try:
				sm.G_Zipp(source_path, output_gzip)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				###sm.G_Zipp(source_path, output_gzip=output_gzip_TS)
			except:
				BODY = "Gzip failed!\nFailed to zip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to zip {}".format(source_path))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 5:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT _DRIVER_V1.5 4 'file or directory' output.gzip, TO_EMAIL, SUBJECT")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 5:
			source_path = sys.argv[2]
			output_gzip = sys.argv[3]
			TO_EMAIL = sys.argv[4]
			SUBJECT = sys.argv[5]
			BODY = "Gzip successful!!!\n{} was successfully zipped and renamed {}".format(source_path, output_gzip)
			try:
				sm.G_Zipp(source_path, output_gzip)
				#sm.G_Zipp(source_path, output_gzip=output_gzip_TS)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Gzip failed!\nFailed to zip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to zip {}".format(source_path))

	# CALLING THE UNZIP FUNCTION
	#Checking decision for Gzip function call
	elif decision_no == "5": # Unzip function
   	#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			source_path = input("Enter the path of the file or directory you want to unzip: ")
			output_f_d = input("Enter the path for the unzipped output: ")
			zip_type = input("Enter if the zipped file contains file or directory: ")
			TO_EMAIL = input("Enter recipient email: ")
			SUBJECT = input("Enter email subject: ")
			BODY = "Unzip successful!!!\n{} was successfully unzipped and renamed {}".format(source_path, output_f_d)
			try:
				sm.Unzipp(source_path, output_f_d, zip_type)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Unzip failed!\nFailed to unzip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to unzip {}".format(source_path))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 6:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 6 arguments and should be ran like this:\npython CONTROL_SCRIPT _DRIVER_V1.9 5 'file or directory' output.unzip, zip_type")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 6:
			source_path = sys.argv[2]
			output_f_d = sys.argv[3]
			zip_type = sys.argv[4]
			TO_EMAIL = sys.argv[5]
			SUBJECT = sys.argv[6]
			BODY = "Unzip successful!!!\n{} was successfully unzipped and renamed {}".format(source_path, output_f_d)
			try:
				sm.Unzipp(source_path, output_f_d, zip_type)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Unzip failed!\nFailed to unzip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to unzip {}".format(source_path))

	# CALLING THE IMPORT FUNCTION
	#Checking decision for Import function call
	elif decision_no == "6": # Import function
   	#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			source_path = input("Enter the zipped dumpfile: ")
			output_f_d = input("Enter the name/path of the unzipped dumpfile: ")
			schemas = input("Enter the schema name: ")
			RUNNER = input("Enter the runner name: ")
			datapump_dir = input("Enter the datapump directory: ")
			import_DB = input("Enter the DB name for the import: ")
			practicedir = input("Enter the practicedir: ")
			TO_EMAIL = input("Enter recipient email: ")
			SUBJECT = input("Enter email subject: ")
			BODY = "Import successful!!!\n{} schema was successfully imported to {}".format(schemas, import_DB)	
			try:
				sm.database_import(source_path, output_f_d, schemas, RUNNER, datapump_dir, import_DB, practicedir)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Import failed!!!\n{} schema import to {} failed".format(schemas, import_DB)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to import {} to {}".format(schemas, import_DB))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 10:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 10 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.10 6 source_path output_f_d schemas RUNNER datapump_dir import_DB practicedir")
      #Checking if the right number of command line argument is passed		
		elif len(sys.argv) - 1 == 10:
			source_path = sys.argv[2]
			output_f_d = sys.argv[3]
			schemas = sys.argv[4]
			RUNNER = sys.argv[5]
			datapump_dir = sys.argv[6]
			import_DB = sys.argv[7]
			practicedir = sys.argv[8]
			TO_EMAIL = sys.argv[9]
			SUBJECT = sys.argv[10]
			BODY = "Import successful!!!\n{} schema was successfully imported to {}".format(schemas, import_DB)
			try: 	
				sm.database_import(source_path, output_f_d, schemas, RUNNER, datapump_dir, import_DB, practicedir)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
			except:
				BODY = "Import failed!!!\n{} schema import to {} failed".format(schemas, import_DB)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to import {} to {}".format(schemas, import_DB))
	else:
		print("Invalid decision entered!")
		exit()

# Main body
if __name__ == '__main__':
	stack_modules_function()
