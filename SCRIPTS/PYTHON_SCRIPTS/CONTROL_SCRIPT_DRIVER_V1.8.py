#!/usr/bin/python

import stack_modules_v1_8 as sm, sys 

def stack_modules_function():
	decision_no = sys.argv[1]
	#Checking decision for backup function call
	if decision_no == "1":
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			source = input("Enter backup source: ")
			destination = input("Enter backup destination: ")
			bk_type = input("Enter backup type: ")
			try:
				sm.backup_function(source, destination, bk_type)
			except:
				print("Backup failed!!!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 4:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 4 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 1 /home/oracle/scripts/practicedir_abi_sep23/file1.txt /home/oracle/scripts/practicedir_abi_sep23/backup_location f")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 4:
			source=sys.argv[2]
			destination=sys.argv[3]
			bk_type=sys.argv[4]
			try:
				sm.backup_function(source, destination, bk_type)
			except:
				print("Backup failed!!!")

	#Checking decision for database backup function call
	elif decision_no == "2":
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			practicedir = input("Enter the practicedir: ")
			backup_location = input("Enter the backup_location: ")
			RUNNER = input("Enter the runner name: ")
			schemas = input("Enter the schema name(s): ")
			try:
				sm.database_backup_function(practicedir, backup_location, RUNNER, schemas)
			except:
				print("Export failed!!!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 5:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 2 /home/oracle/scripts/practicedir_abi_sep23 /backup/AWSSEP23/APEXDB ABIB stack_temp") 
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 5:
			practicedir=sys.argv[2]
			backup_location=sys.argv[3]
			RUNNER=sys.argv[4]
			schemas=sys.argv[5]
			try:
				sm.database_backup_function(practicedir, backup_location, RUNNER, schemas)
			except:
				print("Export failed!!!")

	#Checking decision for disk utilization function call
	elif decision_no == "3":
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			disk = input("Enter the disk you'd like to check: ")
			threshold = input("Specify the disk utilization threshold: ")
			try:
				sm.disk_maintenance_check_on_prem(disk, threshold)
			except:
				print("Disk utilization check error!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 3:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 3 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.7 3 /u01 50")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 3:
			disk = sys.argv[2]
			threshold = sys.argv[3]
			try:
				sm.disk_maintenance_check_on_prem(disk, threshold)
			except:
				print("Disk utilization check error!")

	elif decision_no == "4":
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			source_path = input("Enter the path of the file or directory you want to compress: ")
			output_gzip = input("Enter the path for the compressed output: ")
			try:
				sm.G_Zipp(source_path, output_gzip)
				###sm.G_Zipp(source_path, output_gzip=output_gzip_TS)
			except:
				print("Error! Failed to zip {}".format(source_path))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 3:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 3 arguments and should be ran like this:\npython CONTROL_SCRIPT _DRIVER_V1.8 'file or directory' output.gzip")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 3:
			source_path = sys.argv[2]
			output_gzip = sys.argv[3]
			#try:
			sm.G_Zipp(source_path, output_gzip)
				#sm.G_Zipp(source_path, output_gzip=output_gzip_TS)
			#except:
			#	print("Error! Failed to zip {}".format(source_path))
	else:
		print("Invalid decision entered!")
		exit()
if __name__ == '__main__':
	stack_modules_function()
