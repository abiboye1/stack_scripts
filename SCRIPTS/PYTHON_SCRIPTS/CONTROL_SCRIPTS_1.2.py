#!/usr/bin/python

import sys, shutil as sh

#Variable declaration

source=sys.argv[1]
destination=sys.argv[2]
bk_type=sys.argv[3]

#Function declaration
def copy_function():
	if bk_type == 'f':
		sh.copy(source, destination)
		print("Successfully copied from {} to {}".format(source, destination))
	elif bk_type == 'd':
		sh.copytree(source, destination)
		print("Successfully copied from %s to %s" %(source, destination))

if __name__ == '__main__':
	copy_function()




"""
SOURCE=sys.argv[1]
DESTINATION=sys.argv[2]
time_string=time.localtime()
print(time_string)
TS=time.strftime("%d%m%y%M%S",time_string)
DESTINATION_TS=('{}_{}'.format(DESTINATION,TS))
print("The first command line arg is {}".format(SOURCE))
print("The second command line arg is {}".format(DESTINATION))

#Function Defining

def f_d_copy():
   if os.path.isfile(SOURCE):
      print("Calling a file copy function")
      shutil.copy(SOURCE,DESTINATION_TS)
   else:
      os.path.isdir(SOURCE)
      print("Calling a directory copy function")
      shutil.copytree(SOURCE,DESTINATION_TS)
f_d_copy()

print("The source is: {}".format(SOURCE))
print("The destination is: {}".format(DESTINATION))

#Copy File
print("Starting to copy")
print("Source successfully copied")
"""

