#!/usr/bin/python

import stack_modules_v1_4 as sm, sys 

def stack_modules_function():
	decision_no = sys.argv[1]
	if decision_no == "1":
		if len(sys.argv) - 1 != 4:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 4 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 1 /home/oracle/scripts/practicedir_abi_sep23/file1.txt /home/oracle/scripts/practicedir_abi_sep23/backup_location f")
		elif len(sys.argv) - 1 == 4:
			source=sys.argv[2]
			destination=sys.argv[3]
			bk_type=sys.argv[4]
			try:
				sm.backup_function(source, destination, bk_type)
			except:
				print("Backup failed!!!")

	elif decision_no == "2":
		if len(sys.argv) - 1 != 5:
			print("Error!\nThere are {} arguments in this call".format(len(sys.argv) - 1))
			print("\nThis function call requires 5 arguments and should be ran like this:\npython CONTROL_SCRIPT_DRIVER_V1.5 2 /home/oracle/scripts/practicedir_abi_sep23 /backup/AWSSEP23/APEXDB ABIB stack_temp") 
		elif len(sys.argv) - 1 == 5:
			practicedir=sys.argv[2]
			backup_location=sys.argv[3]
			RUNNER=sys.argv[4]
			schemas=sys.argv[5]
			try:
				sm.database_backup_function(practicedir, backup_location, RUNNER, schemas)
			except:
				print("Export failed!!!")
if __name__ == '__main__':
	stack_modules_function()
