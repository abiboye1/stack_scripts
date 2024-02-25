#!/usr/bin/python

import stack_modules_v1_23 as sm, sys

def stack_modules_function():
	# Decision number indicates the function the user decides to call.
	# 1 --> Backup function
	# 2 --> Database backup function
	# 3 --> Disk utilization function
	# 4 --> Gzip function
	# 5 --> Unzipp function
	# 6 --> Database import function	
	# 7 --> Data Migration function
	# 8 --> Create IAM Users
	# 9 --> Create IAM Group
	# 10 --> Add User to Group
	# 11 --> Read Users from DB and Create Users in AWS IAM GROUP
	# 12 --> Delete Users
	# 13 --> Create Bucket

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
			try:
				sm.backup_function(source=input("Enter backup source: "), destination=input("Enter backup destination: "))
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Backup Successful!!!")
			except Exception as e:
				BODY = "Backup failed!!!"
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Backup failed!!! Error: {}".format(str(e)))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 8:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 1 /home/oracle/scripts/practicedir_abi_sep23/file1.txt /home/oracle/scripts/practicedir_abi_sep23/backup_location f")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 8:
			try:
#				sm.backup_function(source=sys.argv[2], destination=sys.argv[3], OP_ID=sys.argv[4], OP_NAME=sys.argv[5], STATUS=sys.argv[6], OP_TYPE=sys.argv[7], RUNNER=sys.argv[8])
				sm.backup_function(source=sys.argv[2], destination=sys.argv[3], op_name=sys.argv[4], STATUS=sys.argv[5], RUNNER=sys.argv[6])
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[7], SUBJECT=sys.argv[8], BODY="Backup Successful!!!")
			except:
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[7], SUBJECT=sys.argv[8], BODY="Backup failed!!! Failed to copy {} to {}".format(source, destination))
				print("Backup failed!!!")

	# CALLING THE DATABASE BACKUP FUNCTION
	#Checking decision for database backup function call
	elif decision_no == "2": # Database backup function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			try:
				sm.database_backup_function(practicedir=input("Enter the practicedir: "), backup_location=input("Enter the backup_location: "), RUNNER=input("Enter the runner name: "), schemas=input("Enter the schema name(s): "))
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Database backup successful!!!")
			except:
				#BODY = "Export failed!!! Failed to export {} schema".format(schemas)
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY= "Export failed!!! Failed to export {} schema".format(kwargs['schemas']))
				print("Export failed!!!")
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 9:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 7 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 2 /home/oracle/scripts/practicedir_abi_sep23 /backup/AWSSEP23/APEXDB ABIB stack_temp") 
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 9:
			try:
				sm.database_backup_function(practicedir=sys.argv[2], backup_location=sys.argv[3], RUNNER=sys.argv[4], schemas=sys.argv[5], STATUS=sys.argv[6], op_name=sys.argv[7])
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[8], SUBJECT=sys.argv[9], BODY="Database backup Successful!!!")
			except Exception as e:
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[8], SUBJECT=sys.argv[9], BODY="Export failed!!!")
				print("Export failed!!! Error: %s"%(str(e)))


	# CALLING THE DISK UTILIZATION FUNCTION
	#Checking decision for disk utilization function call
	elif decision_no == "3": # Disk utilization function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			try:
				sm.disk_maintenance_check_on_prem(disk=input("Enter the disk you'd like to check: "), warning_threshold=input("Enter disk utiliazation warning threshold"), critical_threshold=input("Enter disk utilization critical threshold"), TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "))
			except Exception as e:
				print("Disk utilization check error! Error: {}".format(str(e)))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 9:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.7 3 /u01 50")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 9:
			try:
				sm.disk_maintenance_check_on_prem(disk=sys.argv[2],warning_threshold=sys.argv[3], critical_threshold=sys.argv[4], TO_EMAIL=sys.argv[5], SUBJECT=sys.argv[6], op_name=sys.argv[7], RUNNER=sys.argv[8], STATUS=sys.argv[9])
			except Exception as e:
				print("Disk utilization check error! Error {}".format(str(e)))


	# CALLING THE GZIP FUNCTION
	#Checking decision for Gzip function call
	elif decision_no == "4": # Gzip function
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			try:
				sm.G_Zipp(source_path=input("Enter the path of the file or directory you want to compress: "), output_gzip=input("Enter the path for the compressed output: "))
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Gzip successful!!!")
			except:
				#BODY = "Gzip failed!\nFailed to zip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Gzip failed!\nFailed to zip {}".format(source_path=input("Enter the path of the file or directory you want to compress: ")))
				print("Error! Failed to zip {}".format(source_path=input("Enter the path of the file or directory you want to compress: ")))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 5:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT _DRIVER_V1.5 4 'file or directory' output.gzip, TO_EMAIL, SUBJECT")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 5:
			try:
				sm.G_Zipp(source_path=sys.argv[2], output_gzip=sys.argv[3])
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[4], SUBJECT=sys.argv[5], BODY="Gzip successful!!!")
			except:
				#BODY = "Gzip failed!\nFailed to zip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[4], SUBJECT=sys.argv[5], BODY="Gzip failed!\nFailed to zip {}".format(source_path=sys.argv[2]))
				print("Error! Failed to zip {}".format(source_path=sys.argv[2]))


	# CALLING THE UNZIP FUNCTION
	#Checking decision for Gzip function call
	elif decision_no == "5": # Unzip function
   	#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			try:
				sm.Unzipp(source_path=input("Enter the path of the file or directory you want to unzip: "), output_f_d=input("Enter the path for the unzipped output: "), zip_type=input("Enter if the zipped file contains file or directory: "))
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Unzip successful!!!")
			except:
				#BODY = "Unzip failed!\nFailed to unzip {}".format(source_path)
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Unzip failed!")
				print("Error! Failed to unzip {}".format(source_path))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 6:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 6 arguments and should be ran like this:\npython CONTROL_SCRIPT _DRIVER_V1.9 5 'file or directory' output.unzip, zip_type")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 6:
			try:
				sm.Unzipp(source_path=sys.argv[2], output_f_d=sys.argv[3], zip_type=sys.argv[4])
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[5], SUBJECT=sys.argv[6], BODY="Unzip successful!!!")
			except:
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[5], SUBJECT=sys.argv[6], BODY="Unzip failed!")
				print("Error! Failed to unzip {}".format(source_path=sys.argv[2]))


	# CALLING THE IMPORT FUNCTION
	#Checking decision for Import function call
	elif decision_no == "6": # Import function
   	#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			try:
				#sm.database_import(source_path, output_f_d, schemas, RUNNER, datapump_dir, import_DB, practicedir)
				sm.database_import(schemas=input("Enter the schema name: "), RUNNER=input("Enter the runner name: "), datapump_dir=input("Enter the datapump directory: "), import_DB=input("Enter the DB name for the import: "), practicedir=input("Enter the practicedir: ")) 
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Import successful!!!\n{} schema was successfully imported to {}".format(kwargs['schemas'], kwargs['import_DB']))
			except:
				#BODY = "Import failed!!!\n{} schema import to {} failed".format(schemas, import_DB)
				sm.STACK_EMAIL(TO_EMAIL, SUBJECT, BODY)
				print("Error! Failed to import {} to {}".format(schemas, import_DB))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 11:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 10 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.10 6 source_path output_f_d schemas RUNNER datapump_dir import_DB practicedir")
      #Checking if the right number of command line argument is passed		
		elif len(sys.argv) - 1 == 11:
			#try: 
			sm.database_import(source_path=sys.argv[2], output_f_d=sys.argv[3], schemas=sys.argv[4], RUNNER=sys.argv[5], datapump_dir=sys.argv[6], import_DB=sys.argv[7], practicedir=sys.argv[8], backup_location=sys.argv[9])
				#sm.database_import(schemas=sys.argv[2], RUNNER=sys.argv[3], datapump_dir=sys.argv[4], import_DB=sys.argv[5], practicedir=sys.argv[6])
			sm.STACK_EMAIL(TO_EMAIL=sys.argv[10], SUBJECT=sys.argv[11], BODY="Import successful!!!")
			#except Exception as e:
			#	sm.STACK_EMAIL(TO_EMAIL=sys.argv[9], SUBJECT=sys.argv[10], BODY="Import failed!")
			#	print("Import Failed! Error: {}".format(str(e)))

		
	# CALLING DATA MIGRATION FUNCTION
	#Checking decision for Data Migration function call
	elif decision_no == "7": # DATA MIGRATION
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			try:
				sm.DATA_MIGRATION(schemas=input("Enter the schema name: "), RUNNER=input("Enter the runner name: "), datapump_dir=input("Enter the datapump directory: "), import_DB=input("Enter the DB name for the import: "), practicedir=input("Enter the practicedir: "), backup_location=input("Enter backup location: "), OP_ID=input("Enter OP_ID: "), OP_NAME=input("Enter OP_NAME: "), STATUS=input("Enter status: "), OP_TYPE=input("Enter OP_TYPE: "))
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Data Migration Successful!\n{} schema was successfully migrated to {}".format(kwargs['schemas'], kwargs['import_DB']))
			except Exception as e:
				sm.STACK_EMAIL(TO_EMAIL=input("Enter recipient email: "), SUBJECT=input("Enter email subject: "), BODY="Data Migration Failed")
				print("Data Migration Failed! Error: {}".format(str(e)))
		#Checking if arguments passed exceed or is less than the required argument and spilling usage
		elif len(sys.argv) - 1 != 11:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 8 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.13 7 schemas RUNNER datapump_dir import_DB practicedir TO_EMAIL SUBJECT")
		#Checking if the right number of command line argument is passed
		elif len(sys.argv) - 1 == 11:
			try:
				sm.DATA_MIGRATION(schemas=sys.argv[2], RUNNER=sys.argv[3], datapump_dir=sys.argv[4], import_DB=sys.argv[5], practicedir=sys.argv[6], backup_location=sys.argv[7], op_name=sys.argv[8], STATUS=sys.argv[9])
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[10], SUBJECT=sys.argv[11], BODY="Data Migration Successful!")
			except Exception as e:
				sm.STACK_EMAIL(TO_EMAIL=sys.argv[10], SUBJECT=sys.argv[11], BODY="Data Migration Failed!")
				print("Data Migration Failed! Error: {}".format(str(e)))

		
		# CALLING CREATE IAM FUNCTION
	elif decision_no == "8": # CREATE IAM USER
   	#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.aws_create_users(service=input("Enter AWS service name: "), user=input("Enter username: "))
		elif len(sys.argv) - 1 != 5:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.20.py 8 iam stack_usr_aut IAM ABIB Running")
		elif len(sys.argv) - 1 == 5:
			sm.aws_create_users(service=sys.argv[1], user=sys.argv[2], op_name=sys.argv[3], RUNNER=sys.argv[4], STATUS=sys.argv[5])


		# CALLING CREATE GROUP FUNCTION
	elif decision_no == "9": # CREATE IAM GROUP
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.aws_create_group(service=input("Enter AWS service name: "), group=input("Enter group name: "), policy_arn=input("Enter policy arn: "))
		elif len(sys.argv) - 1 != 7:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 7 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.18.py 9 iam stack_adm_grp_atm arn:aws:iam::aws:policy/AdministratorAccess")
		elif len(sys.argv) - 1 == 7:
			sm.aws_create_group(service=sys.argv[2], group=sys.argv[3], policy_arn=sys.argv[4], op_name=sys.argv[5], RUNNER=sys.argv[6], STATUS=sys.argv[7])
	

       # CALLING ADD USER TO GROUP FUNCTION
	elif decision_no == "10": # ADD IAM USER TO GROUP
       #Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.aws_add_user_to_group(service=input("Enter AWS service name: "), group=input("Enter group name: "), user=input("Enter IAM user: "), password=input("Enter password: "))
		elif len(sys.argv) - 1 != 8:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 8 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.18.py 9 iam stack_adm_grp_atm iam_user iam_password")
		elif len(sys.argv) - 1 == 8:
			sm.aws_add_user_to_group(service=sys.argv[2], group=sys.argv[3], user=sys.argv[4], password=sys.argv[5], op_name=sys.argv[6], RUNNER=sys.argv[7], STATUS=sys.argv[8])


		# CALLING READ USERS FROM DB AND	ADD USER TO AWS IAM GROUP FUNCTION
	elif decision_no == "11": # READ USERS FROM DB AND ADD USER TO AWS IAM GROUP
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.read_db_create_grp(service=input("Enter AWS service name: "), group=input("Enter group name: "), policy_arn=input("Enter policy arn: "), password=input("Enter password: "))
		elif len(sys.argv) - 1 != 8:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function cal requires 4 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.21.py 11 iam GROUP_ENG arn:aws:iam::aws:policy/AdministratorAccess")
		elif len(sys.argv) - 1 == 8:		
			sm.read_db_create_grp(service=sys.argv[2], group=sys.argv[3], policy_arn=sys.argv[4], password=sys.argv[5], op_name=sys.argv[6], RUNNER=sys.argv[7], STATUS=sys.argv[8])


		# CALLING DELETE USERS FUNCTION
	elif decision_no == "12": # DELETE IAM USERS
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.delete_users(service=input("Enter AWS service name: "), user=input("Enter username: "),  group=input("Enter group name: "), policy_arn=input("Enter policy arn: "), access_key=input("Enter access key: "), serial_num=input("Enter MFA device serial number: "), policy_name=input("Enter policy name: "), op_name=input("Enter op_name: "), RUNNER=input("Enter runner: "), STATUS=input("Enter status: "))
		elif len(sys.argv) - 1 != 11:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 10 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.18.py 9 iam stack_adm_grp_atm iam_user iam_password")
		elif len(sys.argv) - 1 == 11:
			sm.delete_users(service=sys.argv[2], user=sys.argv[3], group=sys.argv[4], policy_arn=sys.argv[5], access_key=sys.argv[6], serial_num=sys.argv[7], policy_name=sys.argv[8], op_name=sys.argv[9], RUNNER=sys.argv[10], STATUS=sys.argv[11])

	
		# CALLING CREATE BUCKET FUNCTION
	elif decision_no == "13": # CREATE S3 BUCKET
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.create_s3_bucket(bucket=input("Enter bucket name: "))
		elif len(sys.argv) - 1 != 2:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 2 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.22.py 13 S3 bucket_name")
		elif len(sys.argv) - 1 == 2:
			 sm.create_s3_bucket(bucket=sys.argv[2])


		# CALLING DELETE BUCKET FUNCTION
	elif decision_no == "14": # DELETE S3 BUCKET
		#Checking if only one argument is passed and taking inputs
		if len(sys.argv) - 1 == 1:
			sm.delete_s3_bucket(bucket=input("Enter bucket name: "))
		elif len(sys.argv) - 1 != 2:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 2 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER _V1.23.py 13 S3 bucket_name")
		elif len(sys.argv) - 1 == 2:
			sm.delete_s3_bucket(bucket=sys.argv[2])


	else:
		print("Invalid decision entered!")
		exit()
   		
# Main body
if __name__ == '__main__':
	stack_modules_function()
