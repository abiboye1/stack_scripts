#!/usr/bin/python

import sys, shutil as sh, time as t, os, psutil, gzip, pathlib as pl, tarfile, smtplib as s

# Variable declaration
timestring=t.localtime()
TS=t.strftime('%m%d%Y%H%M%S', timestring)

#Function declaration
def STACK_EMAIL(**kwargs):
   # Variables
	FROM='oracle@MKIT-DEV-OEM.localdomain'
	BODY=""

	MSG = ("\n".join(("From: %s" %FROM, "To: %s" %(kwargs['TO_EMAIL']), "Subject: %s:\n" %(kwargs['SUBJECT']), "%s" %BODY)))

	with s.SMTP('localhost') as my_server:
		my_server.sendmail(FROM, kwargs['TO_EMAIL'], MSG)
		print("Email sent successfully to %s" %(kwargs['TO_EMAIL']))


def database_backup_function(**kwargs):
   #Database backup function variable declaration
	backup_dir = os.path.join(kwargs['backup_location'], kwargs['RUNNER'], TS)
	os.makedirs(backup_dir)
	try:
      #Writing into .par file
		with open('%s/export_%s_%s.par'%(kwargs['practicedir'], kwargs['RUNNER'], TS), 'w+') as pf:
			pf.write('userid="/ as sysdba"\n''schemas=stack_temp\n''logfile={x}_{y}_{z}.log\n''dumpfile={x}_{y}_{z}.dmp\n''directory=DATA_PUMP_DIR'.format(x=kwargs['schemas'], y=kwargs['RUNNER'], z=TS))
		print("Is {} closed? {}".format(pf.name, pf.closed))

      #Reading from .par file
		with open('export_%s_%s.par'%(kwargs['RUNNER'], TS), 'r+') as pf:
			output = pf.read()
		print("Is {} closed? {}".format(pf.name, pf.closed))

      #Creating script for export
		with open('{}/export_script.sh'.format(kwargs['practicedir']), 'w+') as export:
			export.write('. /home/oracle/scripts/oracle_env_APEXDB.sh\n''expdp parfile=%s/export_%s_%s.par'%(kwargs['practicedir'], kwargs['RUNNER'], TS))
		print("Is {} closed? {}".format(export.name, export.closed))
		export_command='{}/export_script.sh'.format(kwargs['practicedir'])
		os.popen("chmod 700 {}".format(export_command))
      #Running expdp command to initiate database export
		export_result = os.popen('%s'%export_command).read()

	except:
		print("Export failed!")


def G_Zipp(**kwargs):
	#output_gzip_TS = '{}_{}'.format(kwargs['output_gzip'], TS) - ### Temporarily changed for 1.13
	# Checking if user wants to compress a file or directory
	if os.path.isfile(kwargs['source_path']):
		with open(kwargs['source_path'], 'rb') as my_input:
			with gzip.open(kwargs['output_gzip'], 'wb') as my_output: ##### Changes
				sh.copyfileobj(my_input, my_output)
				print("Successfully zipped file %s to %s"%(kwargs['source_path'], kwargs['output_gzip']))
	elif os.path.isdir(kwargs['source_path']):
		# Creating a temporary tar archive name
		tar_filename = '{}.tar'.format(kwargs['source_path'])
		# Opening the temporary tar archive for writing
		with tarfile.open(tar_filename, 'w') as tar:
			# Adding the entire content of the source directory to the tar archive. The arcname parameter ensures that the files in the archive have the same names as they do in the original directory.
			tar.add('%s'%(kwargs['source_path']))
		#Opening the temporary tar archive file for reading in binary mode (rb)
		with open(tar_filename, 'rb') as my_input_tar_file:
			# Opening the target gzip file for writing in binary mode (wb). This is where the compressed data will be written.
			with gzip.open('%s'%(kwargs['output_gzip']), 'wb') as my_output_gzip_file:  ### Changes
				sh.copyfileobj(my_input_tar_file, my_output_gzip_file)
				print("Successfully zipped directory %s to %s"%(kwargs['source_path'], kwargs['output_gzip']))
		# Removing the temporary tar archive
		#p.Path(tar_filename).unlink()
	else:
		print("Error! {} is neither a file nor directory".format(kwargs['source_path']))


def Unzipp(**kwargs):
	# Checking if user wants to unzip a file or directory
	#try:
	if kwargs['zip_type'] == 'f': # Zipped file
		# Reading the content of the gzipped file
		with gzip.open(kwargs['source_path'], 'rb') as f:
			file_content = f.read()
			#print(file_content)
			# Writing unzipped file content into an output file in my cwd
			with open(kwargs['output_f_d'], 'wb') as wf:
				wf.write(file_content)
			print("Unzipped content has been written to %s"%(kwargs['output_f_d']))
	elif kwargs['zip_type'] == "d": # Zipped directory
		# Open the compressed directory
		with gzip.open(kwargs['source_path'], 'rb') as com_dir:
   		# Open the tar archive
			with tarfile.open(fileobj = com_dir, mode = 'r') as tar:
				tar.extractall(kwargs['output_f_d'])
		# This assigns the Path object created from output_f_d to the variable target_path.
		target_path = pl.Path(kwargs['output_f_d'])
		target_path_TS = os.path.join(str(target_path), TS) # Adding a timestamp
		# Create location where the zipped directory will be extracted
		os.popen("mkdir -p {}".format(target_path_TS))
	
	#except:
	#	print("Failed to unzip!")


def disk_maintenance_check_on_prem(**kwargs):
	while True:
		partition = psutil.disk_usage(kwargs['disk'])
		disk_utilization = partition.percent
		
		BODY=''
		if disk_utilization < float(kwargs['warning_threshold']):
			print("Disk utilization is at %s"%disk_utilization)
			exit()
		# Checking if disk utilization is above critical threshold
		if disk_utilization >= float(kwargs['critical_threshold']): 
			print("DANGER!!! Disk utilization is at {}%, over {}% threshold. Sending email alert in 1 minutes".format(disk_utilization, kwargs['critical_threshold']))
			body_content = "Danger!!! Disk utilization is at %s%%, over %s%% threshold."%(disk_utilization, kwargs['critical_threshold'])
			# Using the sleep function to enable the code wait before alerting
			t.sleep(60)
			STACK_EMAIL(TO_EMAIL=kwargs['TO_EMAIL'], SUBJECT=kwargs['SUBJECT'], BODY=body_content)

		# Checking if disk utilization is above warning threshold
		if disk_utilization >= float(kwargs['warning_threshold']):
			print("Warning!!! Disk utilization is at {}%, over {}% threshold. Sending email alert in 5 minutes".format(disk_utilization, kwargs['warning_threshold']))
			body_content = "Warning!!! Disk utilization is at %s%%, over %s%% threshold."%(disk_utilization, kwargs['warning_threshold'])
         # Using the sleep function to enable the code wait before alerting
			t.sleep(60)
			STACK_EMAIL(TO_EMAIL=kwargs['TO_EMAIL'], SUBJECT=kwargs['SUBJECT'], BODY=body_content)		

def backup_function(**kwargs):
	#Backup type check
	if kwargs['bk_type'] == 'f':
	#if bk_type == 'f':
		sh.copy(kwargs['source'], kwargs['destination'])
		print("\nSuccessfully copied from {} to {}".format(kwargs['source'], kwargs['destination']))
	#elif bk_type == 'd':
	elif kwargs['bk_type'] == 'd':
		sh.copytree(kwargs['source'], kwargs['destination'])
		print("\nSuccessfully copied from %s to %s" %(kwargs['source'], kwargs['destination']))


def database_import(**kwargs):

	# Calling the gzipp function to compress the dump file
	dumpfile = '{}/{}_{}_{}.dmp'.format(kwargs['backup_location'], kwargs['schemas'], kwargs['RUNNER'], TS)
	gzipped_dumpfile = '{}.gzip'.format(dumpfile)
	G_Zipp(source_path=dumpfile, output_gzip=gzipped_dumpfile) ###---Regular Call 1.13**

	# Calling the unzip function to unzip the dumpfile
	unzipped_dumpfile = gzipped_dumpfile.replace('.gzip', '')
	Unzipp(source_path=gzipped_dumpfile, output_f_d=unzipped_dumpfile, zip_type='f') ###---Regular Call 1.13**

	# Copying unzipped dumpfile to SAMD directory
	sh.copy(unzipped_dumpfile, '/backup/AWSSEP23/SAMD')  ###---Regular Call 1.13**
	new_dumpfile_path = os.path.join('/backup/AWSSEP23/SAMD', unzipped_dumpfile)  ###---Regular Call 1.13**
	new_dumpfile = os.path.basename(new_dumpfile_path)

	print()
	print(new_dumpfile)
	print()

	##Creating the impdp par file
	print("Creating the impdp par file")
	with open('impdp_%s_%s.par'%(kwargs['schemas'], kwargs['RUNNER']), 'w+') as pf:

		pf.write('userid="/ as sysdba"\n''schemas={x}\n''remap_schema={x}:{x}_{y}_{z}\n''dumpfile={dumpfile}\n''logfile=impdp_{x}_{y}.log\n''directory={a}\n''table_exists_action=replace'.format(x=kwargs['schemas'], y=kwargs['RUNNER'], z=TS, a=kwargs['datapump_dir'], dumpfile=new_dumpfile))

	#Creating the impdp script that will be used to run the import
	print("Creating impdp script that will be used to run the import")
	with open('import_{}.sh'.format(kwargs['schemas']), 'w+') as pf:
		pf.write('. /home/oracle/scripts/oracle_env_{}.sh\n''impdp parfile={}/impdp_{}_{}.par'.format(kwargs['import_DB'], kwargs['practicedir'], kwargs['schemas'], kwargs['RUNNER']))

	import_command = '{}/import_{}.sh'.format(kwargs['practicedir'], kwargs['schemas'])
	os.popen("chmod 744 {}".format(import_command))
	#Running impdp command to initiate database import
	import_result = os.popen("{}".format(import_command)).read()		


def DATA_MIGRATION(**kwargs):
	# Calling the database backup function
	database_backup_function(**kwargs)

	# Calling the database import function
	database_import(**kwargs)

# Main Body
if __name__ == '__main__':
	decision_no = sys.argv[1]
	if decision_no == "1":
		source=sys.argv[2]
		destination=sys.argv[3]
		bk_type=sys.argv[4]
		backup_function(source, destination, bk_type)

	elif decision_no == "2":
		database_backup_function()
	
	elif decision_no == "3":
		disk = sys.argv[2]
		threshold = sys.argv[3]
		disk_maintenance_check_on_prem(disk, threshold)	

	elif decision_no == "4":
		source_path = sys.argv[2]
		output_gzip = sys.argv[3]
		G_Zipp(source_path, output_gzip)	

	elif decision_no == "5":
		source_path = sys.argv[2]
		output_file = sys.argv[3]
		Unzipp(source_path, output_file)
