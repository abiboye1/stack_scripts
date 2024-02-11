#!/usr/bin/python

import gzip, sys, shutil, tarfile, zipfile, pathlib as pl, os, time
timestring = time.localtime()
TS = time.strftime("%d%m%Y%H%M%S", timestring)
# !pip install zipfile

source = sys.argv[1]
output_f_d = sys.argv[2]
zip_type = sys.argv[3]
if zip_type == "f": # Zipped directory
#if source.endswith('.gz'):
	with gzip.open(source, 'rb') as f:
		file_content = f.read()
		print(file_content)
		with open(output_f_d, 'wb') as wf:
			wf.write(file_content)
	print("Unzipped content has been written to %s"%output_f_d)


elif zip_type == 'd': # Zipped file
#else:
	# Open the compressed directory
	with gzip.open(source, 'rb') as com_dir:
   	# Open the tar archive
		with tarfile.open(fileobj = com_dir, mode = 'r') as tar:
			tar.extractall(output_f_d)
	target_path = pl.Path(output_f_d)
	target_path_TS = os.path.join(str(target_path), TS)
	print(target_path_TS)

   #os.makedirs(target_path)
	os.popen("mkdir -p {}".format(target_path_TS))



