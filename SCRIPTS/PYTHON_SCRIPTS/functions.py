#!/usr/bin/python
import sys


def myfirstfunction(a,b,c):
	print("My family memebers are %s, %s, %s"%(a,b,c))

#Main body below "If running this script, line 9 below runs, if the module is called by a different code, line 9 and below will not run"
if __name__=="__main__":
	x,y,z=sys.argv[1],sys.argv[2],sys.argv[3]
	
	count_args=len(sys.argv) -1
	print("The number of command line argument is %s" %(count_args))
	myfirstfunction(x,y,z)



	
