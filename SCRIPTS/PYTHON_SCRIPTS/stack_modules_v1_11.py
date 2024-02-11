#!/usr/bin/python

import sys, shutil as sh, time as t, os, psutil, gzip, pathlib as pl, tarfile, smtplib as s

# Variable declaration
timestring=t.localtime()
TS=t.strftime('%m%d%Y%H%M%S', timestring)

#Function declaration
def STACK_EMAIL(TO_EMAIL, SUBJECT, BODY):
   # Variables
	FROM='oracle@MKIT-DEV-OEM.localdomain'

	MSG = ("\n".join(("From: %s" %FROM, "To: %s" %TO_EMAIL, "Subject: %s:\n" %SUBJECT, "%s" %BODY)))

	with s.SMTP('localhost') as my_server:
		my_server.sendmail(FROM, TO_EMAIL, MSG)
		print("Email sent successfully to %s" %TO_EMAIL)


def database_backup_function(practicedir, backup_location, RUNNER, schemas):
   #Database backup function variable declaration
	backup_dir = os.path.join(backup_location, RUNNER, TS)
   #print(backup_dir)
	os.makedirs(backup_dir)

	try:
      #Writing into .par file
		with open('%s/export_%s_%s.par'%(practicedir, RUNNER, TS), 'w+') as pf:
			pf.write('userid="/ as sysdba"\n''schemas=stack_temp\n''logfile={x}_{y}_{z}.log\n''dumpfile={x}_{y}_{z}.dmp\n''directory=DATA_PUMP_DIR'.format(x=schemas, y=RUNNER, z=TS))
		print("Is {} closed? {}".format(pf.name, pf.closed))

      #Reading from .par file
		with open('export_%s_%s.par'%(RUNNER, TS), 'r+') as pf:
			output = pf.read()
		print("Is {} closed? {}".format(pf.name, pf.closed))

      #Creating script for export
		with open('{}/export_script.sh'.format(practicedir), 'w+') as export:
			export.write('. /home/oracle/scripts/oracle_env_APEXDB.sh\n''expdp parfile=%s/export_%s_%s.par'%(practicedir, RUNNER, TS))
		print("Is {} closed? {}".format(export.name, export.closed))
		export_command='{}/export_script.sh'.format(practicedir)
		os.popen("chmod 700 {}".format(export_command))
      #Running expdp command to initiate database export
		os.popen('%s'%export_command)

	except:
		print("Export failed!")


def G_Zipp(source_path, output_gzip):
	#output_gzip_TS = os.path.join(output_gzip, TS)
	###output_gzip_TS = os.path.join(output_gzip,"{}_{}".format(os.path.basename(source_path), TS))
	# Checking if user wants to compress a file or directory
	if os.path.isfile(source_path):
		#with open('%s'%source_path, 'rb') as my_input:
		with open(source_path, 'rb') as my_input:
		###with open(source_path, 'rb') as my_input:
			#with gzip.open('%s'%output_gzip, 'wb') as my_output:
			with gzip.open(output_gzip, 'wb') as my_output:
			###with gzip.open('%s'%(output_gzip_TS), 'wb') as my_output:
				sh.copyfileobj(my_input, my_output)
				print("Successfully zipped file %s to %s"%(source_path, output_gzip))
				###print("Successfully zipped file %s to %s"%(source_path, output_gzip_TS))
	elif os.path.isdir(source_path):
		# Creating a temporary tar archive name
		#tar_filename = '{}.tar'.format(source_path.name)
		tar_filename = '{}.tar'.format(source_path)
		# Opening the temporary tar archive for writing
		with tarfile.open(tar_filename, 'w') as tar:
			# Adding the entire content of the source directory to the tar archive. The arcname parameter ensures that the files in the archive have the same names as they do in the original directory.
			#tar.add('%s'%source_path, arcname=source_path.name)
			tar.add('%s'%source_path)
		#Opening the temporary tar archive file for reading in binary mode (rb)
		with open(tar_filename, 'rb') as my_input_tar_file:
			# Opening the target gzip file for writing in binary mode (wb). This is where the compressed data will be written.
			with gzip.open('%s'%output_gzip, 'wb') as my_output_gzip_file:
			###with gzip.open('%s'%(output_gzip_TS), 'wb') as my_output_gzip_file:
				sh.copyfileobj(my_input_tar_file, my_output_gzip_file)
				print("Successfully zipped directory %s to %s"%(source_path, output_gzip))
		# Removing the temporary tar archive
		#p.Path(tar_filename).unlink()
	else:
		print("Error! {} is neither a file nor directory".format(source_path))


def Unzipp(source_path, output_f_d, zip_type):
	# Checking if user wants to unzip a file or directory
	#try:
	if zip_type == 'f': # Zipped file
		# Reading the content of the gzipped file
		with gzip.open(source_path, 'rb') as f:
			file_content = f.read()
			#print(file_content)
			# Writing unzipped file content into an output file in my cwd
			with open(output_f_d, 'wb') as wf:
				wf.write(file_content)
			print("Unzipped content has been written to %s"%output_f_d)
	elif zip_type == "d": # Zipped directory
		# Open the compressed directory
		with gzip.open(source_path, 'rb') as com_dir:
   		# Open the tar archive
			with tarfile.open(fileobj = com_dir, mode = 'r') as tar:
				tar.extractall(output_f_d)
		# This assigns the Path object created from output_f_d to the variable target_path.
		target_path = pl.Path(output_f_d)
		target_path_TS = os.path.join(str(target_path), TS) # Adding a timestamp
		# Create location where the zipped directory will be extracted
		os.popen("mkdir -p {}".format(target_path_TS))
	
	#except:
	#	print("Failed to unzip!")


def disk_maintenance_check_on_prem(disk, threshold):
	partition = psutil.disk_usage(disk)
	disk_utilization = partition.percent
	# Checking if disk utilization exceeds threshold or is at 100% usage
	if disk_utilization > float(threshold) or disk_utilization == 100:
		print("Warning!!! Disk utilization is at {}%, over {}% threshold".format(disk_utilization, threshold))
	else:
		print("Disk utilization is at %s"%disk_utilization)
	

def backup_function(source, destination, bk_type):
	#Backup type check
	if bk_type == 'f':
		sh.copy(source, destination)
		print("Successfully copied from {} to {}".format(source, destination))
	elif bk_type == 'd':
		sh.copytree(source, destination)
		print("Successfully copied from %s to %s" %(source, destination))

"""
def database_backup_function(practicedir, backup_location, RUNNER, schemas):
	#Database backup function variable declaration
	backup_dir = os.path.join(backup_location, RUNNER, TS)
	#print(backup_dir)
	os.makedirs(backup_dir)

	try:
   	#Writing into .par file
		with open('%s/export_%s_%s.par'%(practicedir, RUNNER, TS), 'w+') as pf:
			pf.write('userid="/ as sysdba"\n''schemas=stack_temp\n''logfile={x}_{y}_{z}.log\n''dumpfile={x}_{y}_{z}.dmp\n''directory=DATA_PUMP_DIR'.format(x=schemas, y=RUNNER, z=TS))
		print("Is {} closed? {}".format(pf.name, pf.closed))

   	#Reading from .par file
		with open('export_%s_%s.par'%(RUNNER, TS), 'r+') as pf:
			output = pf.read()
		print("Is {} closed? {}".format(pf.name, pf.closed))

   	#Creating script for export
		with open('{}/export_script.sh'.format(practicedir), 'w+') as export:
			export.write('. /home/oracle/scripts/oracle_env_APEXDB.sh\n''expdp parfile=%s/export_%s_%s.par'%(practicedir, RUNNER, TS))
		print("Is {} closed? {}".format(export.name, export.closed))
		export_command='{}/export_script.sh'.format(practicedir)
		os.popen("chmod 700 {}".format(export_command))
   	#Running expdp command to initiate database export
		os.popen('%s'%export_command)


	except:
		print("Export failed!")
"""

def database_import(source_path, output_f_d, schemas, RUNNER, datapump_dir, import_DB, practicedir):
	"""
	# Calling the database backup function
	database_backup_function(practicedir, backup_location, RUNNER, schemas)

	# Calling the gzipp function to compress the dump file
	#dumpfile = '{w}/{x}_{y}_{z}.dmp'.format(w=backup_location, x=schemas, y=RUNNER, z=TS)
	dumpfile = '{x}_{y}_{z}.dmp'.format(x=schemas, y=RUNNER, z=TS)
	#gzipped_dumpfile = '{w}/{x}_{y}_{z}.dmp.gzip'.format(w=backup_location, x=schemas, y=RUNNER, z=TS)
	gzipped_dumpfile = '{x}_{y}_{z}.dmp.gzip'.format(x=schemas, y=RUNNER, z=TS)
	G_Zipp(dumpfile, gzipped_dumpfile)
	"""

	# Calling the unzip function to unzip the dumpfile
	#Unzipp(os.path.join(backup_location, gzipped_dumpfile), unzip_dir, 'f')
	#Unzipp(gzipped_dumpfile, 'unzipped_dumpfile.dmp', 'f')
	Unzipp(source_path, output_f_d, 'f')
	# Copying unzipped dumpfile to SAMD directory
	"""
	unzipped_dumpfile = os.path.join('/backup/AWSSEP23/APEXDB', output_f_d)
	sh.copy(unzipped_dumpfile, '/backup/AWSSEP23/SAMD') 
	new_dumpfile = os.path.join('/backup/AWSSEP23/SAMD', unzipped_dumpfile)	
	"""
	sh.copy('/backup/AWSSEP23/APEXDB/{}'.format(output_f_d), '/backup/AWSSEP23/SAMD')
	#new_dumpfile = os.path.join('/backup/AWSSEP23/SAMD', output_f_d)
	#new_dumpfile = '/backup/AWSSEP23/SAMD/{}'.format(output_f_d)

	##Creating the impdp par file
	print("Creating the impdp par file")
	with open('impdp_%s_%s.par'%(schemas, RUNNER), 'w+') as pf:
		#pf.write('userid="/ as sysdba"\n''schemas={x}\n''remap_schema={x}:{x}_{y}_{z}\n''dumpfile={dumpfile}\n''logfile=impdp_{x}_{y}.log\n''directory={a}\n''table_exists_action=replace'.format(x=schemas, y=RUNNER, z=TS, a=datapump_dir, dumpfile='/backup/AWSSEP23/SAMD/{}'.format(output_f_d)))

		pf.write('userid="/ as sysdba"\n''schemas={x}\n''remap_schema={x}:{x}_{y}_{z}\n''dumpfile={dumpfile}\n''logfile=impdp_{x}_{y}.log\n''directory={a}\n''table_exists_action=replace'.format(x=schemas, y=RUNNER, z=TS, a=datapump_dir, dumpfile=output_f_d))
	"""
	# Read dumpfile content from export par file
	with open('%s/export_%s_%s.par'%(practicedir, RUNNER, TS), 'r') as export_pf:
		read_dumpfile_content = export_pf.read().split('dumpfile=')[1].split('\n')[0]
	"""
	#Creating the impdp script that will be used to run the import
	print("Creating impdp script that will be used to run the import")
	with open('import_{}.sh'.format(schemas), 'w+') as pf:
		#pf.write('. /backup/AWSSEP23/{}\n''impdp parfile={}/impdp_{}_{}.par'.format(import_DB, practicedir, schemas, RUNNER))
		pf.write('. /home/oracle/scripts/oracle_env_{}.sh\n''impdp parfile={}/impdp_{}_{}.par'.format(import_DB, practicedir, schemas, RUNNER))

	import_command = '{}/import_{}.sh'.format(practicedir, schemas)
	os.popen("chmod 744 {}".format(import_command))
	#Running impdp command to initiate database import
	os.popen("{}".format(import_command))		


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
