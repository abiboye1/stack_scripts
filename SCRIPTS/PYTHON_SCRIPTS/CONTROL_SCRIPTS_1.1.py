#!/usr/bin/python

import shutil, sys, os

file_source=sys.argv[1]
file_dest=sys.argv[2]

os.popen("mkdir -p %s"%file_dest)

dir_source=file_dest
dir_dest=sys.argv[3]
shutil.copy(file_source, file_dest)
shutil.copytree(dir_source, dir_dest)

print("Successfully copied {} to {}" .format(file_source, file_dest))
print("Successfully copied %s to %s" %(dir_source, dir_dest))

