#!/usr/bin/python

import stack_modules_v1_4 as sm, sys 

def stack_modules_function():
	# Decision number indicates the function the user decides to call.
	# 1 --> Backup function
	# 2 --> Database backup function
	
	# Checking if no command line arguments are called
	if len(sys.argv) - 1 == 0:
		print("You entered {} arguments".format(len(sys.argv) - 1))
		print("This script requires you to pass at least one command line argument. Enter:")
		print("\n1 for Backup function\n2 for Database backup function")
		exit()	

	decision_no = sys.argv[1]
	#Checking decision for backup function call
	if decision_no == "1": # Backup function
		#Checking if only one argument is passed and taking inputs if true
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
	elif decision_no == "2": # Database backup function
		#Checking if only one argument is passed and taking inputs if true
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
	
	else:
		print("Invalid decision entered!")
		exit()

# Main body
if __name__ == '__main__':
	stack_modules_function()
