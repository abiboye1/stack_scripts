#!/usr/bin/python

import gzip, shutil, pathlib, sys, tarfile

#test_file = '/home/oracle/scripts/practicedir_abi_sep23/stack_temp_ABIB_01092024054016.dmp'
#test_dir = '/home/oracle/scripts/practicedir_abi_sep23/CONTROL_SCRIPTS_1.1_backup'
source_path = pathlib.Path(sys.argv[1])
output_gzip = sys.argv[2]

if source_path.is_file():
	with open("%s"%source_path, 'rb') as my_input:
		with gzip.open('test_file.gzip', 'wb') as my_output:
			shutil.copyfileobj(my_input, my_output)
elif source_path.is_dir():
	folder = pathlib.Path(source_path)
	for file in folder.iterdir():
		print(file.name)

	#tar_filename = '"{}".format(source_path.name).tar'
	tar_filename = '{}.tar'.format(source_path.name)
	#print(tar_filename)	
	
	with tarfile.open(tar_filename, 'w') as tar:
		tar.add("%s"%source_path, arcname=source_path.name)

	with open(tar_filename, 'rb') as tar_file:
		with gzip.open("%s"%output_gzip, 'wb') as gzip_file:
			shutil.copyfileobj(tar_file, gzip_file)
	# Remove the temporary tar archive
	pathlib.Path(tar_filename).unlink()	
