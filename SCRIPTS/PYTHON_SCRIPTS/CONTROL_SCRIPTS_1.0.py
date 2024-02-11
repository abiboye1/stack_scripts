#!/usr/bin/python

import shutil
import subprocess

file_source='/home/oracle/scripts/practicedir_abi_sep23/file1.txt'
file_dest='/home/oracle/scripts/practicedir_abi_sep23/python_dir'

dir_source='/home/oracle/scripts/practicedir_abi_sep23/python_dir'
dir_dest='/home/oracle/scripts/practicedir_abi_sep23/newbackup/python_dir'


shutil.copy(file_source, file_dest)
shutil.copytree(dir_source, dir_dest)

print("Successfully copied %s to %s" %(file_source, file_dest))
print("Successfully copied {} to {}".format(dir_source, dir_dest))


"""

source = '/home/oracle/scripts/practicedir_abi_sep23/python_dir'
destination = '/home/oracle/scripts/practicedir_abi_sep23/new_backup'

shutil.copytree(source, destination)
ls_command = f'ls -ltr {destination}'
result = subprocess.run(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


#print(ls_command)

if result.returncode == 0:
    print("Listing files in destination folder:")
    print(result.stdout)
else:
    print(f"Error: {result.stderr}")
"""
