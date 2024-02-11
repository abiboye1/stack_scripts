#!/usr/bin/python

import stack_modules_v1_3 as sm, sys 

def stack_modules_function():
	decision_no = sys.argv[1]
	if decision_no == "1":
		source=sys.argv[2]
		destination=sys.argv[3]
		bk_type=sys.argv[4]
		sm.backup_function(source, destination, bk_type)

	elif decision_no == "2":
		sm.database_backup_function()

if __name__ == '__main__':
	stack_modules_function()
