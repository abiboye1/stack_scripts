#!/usr/bin/python

import os, time
timestring=time.localtime()
TS=time.strftime("%d%m%Y%H%M%S", timestring)

backup_base="/backup/AWSSEP23/APEXDB/"
RUNNER="ABIB"
backup_dir=os.path.join(backup_base,RUNNER)

#Declaring function
def get_server_dictionary():
	"""
	servers={
    "Hosts":[{"MKIT-DEV-OEM":"ON-PREM"}, {"STACKCLOUD":"CLOUD"}],
    "Disks":["/u01", "/u02", "/u03", "/u04", "/u05", "/backup"],
    "Transient_directory_path": [{"/u01":"/u01/app/oracle/admin/APEXDB/adump"}, {"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
}
	return servers
	"""
	servers={
    "Hosts":{"MKIT-DEV-OEM":"ON-PREM", "STACKCLOUD":"CLOUD"},
    "Disks":["/u01","/u02","/u03","/u04","/u05","/backup"],
    "Transient_directory_paths":[{"/u01":"/u01/app/oracle/admin/APEXDB/adump"},{"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
    }
	return servers


def database_backup():
	try:
		with open ('/home/oracle/scripts/practicedir_abi_sep23/test_{}.par'.format(TS), mode='w') as my_test_file:
			my_test_file.write('userid="/ as sysdba"\nschemas=stack_temp\ndumpfile=stack_temp_ABIB_{x}.dmp\nlogfile=stack_temp_ABIB_{x}.log\ndirectory=DATA_PUMP_DIR'.format(x=TS))
    	#my_test_file.close()
		print("Is {} closed? {} ".format(my_test_file.name,my_test_file.closed))

		my_test_file= open ('test.par', mode='r')
		output=my_test_file.read()
		my_test_file.close()
		print("Is {} closed? {} ".format(my_test_file.name,my_test_file.closed))

		export=open ('/home/oracle/scripts/practicedir_abi_sep23/export.sh', mode='w+')
		export.write(". /home/oracle/scripts/oracle_env_APEXDB.sh\nexpdp parfile=test_{}.par".format(TS))
		export.close()
		export_content='/home/oracle/scripts/practicedir_abi_sep23/export.sh'

		file_name="test_{}.par".format(TS)
		file_path=os.path.join(os.getcwd(),"{}".format(file_name))

		if os.path.isfile(file_path):
			print("Par file exists")

		backup_path=os.path.join(backup_dir,TS)
		print(backup_path)
		os.popen("mkdir -p {}".format(backup_path))
		os.popen("chmod 744 {}".format(export_content))
		os.popen("{}".format(export_content))
		#os.mkdir(backup_path)
		#if os.path.isdir(backup_path):
		#  print("Timestamped backup path exists!")

	except:
		print("Export failed")
	


if __name__ == "__main__":
	get_server_dictionary()
