#!/usr/bin/python

import sys as s, demo_calc as d

#Variable declaration 
x=int(s.argv[1])
y=int(s.argv[2])
func=s.argv[3]

#Function declaration
def calculator(x,y):
	d.add_func(x,y)
	d.sub_func(x,y)
	d.mult_func(x,y)

if __name__ == "__main__":
	if func == "add":
		z=d.add_func(x,y) 
		print("{} plus {} is {}".format(x,y,z))
	elif func == "minus":
		z=d.sub_func(x,y)
		print("%s minus %s is %s"%(x,y,z))
	elif func == "times":
		z=d.mult_func(x,y)
		print(str(x) + " multiplied by " + str(y) + " is " + str(z))
	else:
		print("Invalid function entered")

calculator(x,y)

