#!/usr/bin/python

import sys, shutil as sh, time as t, os

#Function declaration
def backup_function(source, destination, bk_type):
	#Backup function variable declaration
	if bk_type == 'f':
		sh.copy(source, destination)
		print("Successfully copied from {} to {}".format(source, destination))
	elif bk_type == 'd':
		sh.copytree(source, destination)
		print("Successfully copied from %s to %s" %(source, destination))

def database_backup_function():
	#Database backup function variable declaration
	timestring=t.localtime()
	TS=t.strftime('%m%d%Y%H%M%S', timestring)

	backup_location = '/backup/AWSSEP23/APEXDB'
	RUNNER = 'abib'
	backup_dir = os.path.join(backup_location, RUNNER, TS)
	#print(backup_dir)
	os.makedirs(backup_dir)
	practicedir='/home/oracle/scripts/practicedir_abi_sep23'
	schema="stack_temp"

	try:
   	#Writing into .par file
		with open('%s/export_%s_%s.par'%(practicedir, RUNNER, TS), 'w+') as pf:
			pf.write('userid="/ as sysdba"\nschemas=stack_temp\nlogfile={x}_{y}_{z}.log\ndumpfile={x}_{y}_{z}.dmp\ndirectory=DATA_PUMP_DIR'.format(x=schema, y=RUNNER, z=TS))
		print("Is {} closed? {}".format(pf.name, pf.closed))

   	#Reading from .par file
		with open('export_%s_%s.par'%(RUNNER, TS), 'r+') as pf:
			output = pf.read()
		print("Is {} closed? {}".format(pf.name, pf.closed))

   	#Creating script for export
		with open('{}/export_script.sh'.format(practicedir), 'w+') as export:
			export.write('. /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=%s/export_%s_%s.par'%(practicedir, RUNNER, TS))
		print("Is {} closed? {}".format(export.name, export.closed))
		export_command='{}/export_script.sh'.format(practicedir)
		os.popen("chmod 700 {}".format(export_command))
   	#Running expdp command to initiate database export
		os.popen('%s'%export_command)

	except:
		print("Export failed!")

if __name__ == '__main__':
	decision_no = sys.argv[1]
	if decision_no == "1":
		source=sys.argv[2]
		destination=sys.argv[3]
		bk_type=sys.argv[4]
		backup_function(source, destination, bk_type)

	elif decision_no == "2":
		database_backup_function()

