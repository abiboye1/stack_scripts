#!/usr/bin/python
import os
"""
user_entry=input("Please enter first name: ")
print(type(user_entry))
print("User entered : {}" .format(user_entry))

for x in range(2,10):
	print(x)

for x in range(2,10,2):
   print(x)
"""
"""
#Creating/Writing into a file
fo=open("/home/oracle/scripts/practicedir_abi_sep23/test_abib.par", "w+")
#print("The name of the file is {}" .format(fo.name))

#print("Is {} closed? {} ".format(fo.name,fo.closed))
fo.write("userid='/ as sysdba' \nschemas=stack_temp\ndumpfile=stack_temp_abib_112211.dmp \nlogfile=stack_temp_abib_112211.log \ndirectory=DATA_PUMP_DIR")
fo.close()
#print("Is {} closed? {} ".format(fo.name,fo.closed))

#Opening/Reading from a file
file_read=open("/home/oracle/scripts/practicedir_abi_sep23/test_abib.par", "r+")
file_content=file_read.read()
print(file_content)
file_read.close()
"""

dir_content=os.listdir('.')
print(dir_content)
