#!/usr/bin/python
import sys, stack_modules as t

#Variable declaration

"""
x=int(sys.argv[1])
y=int(sys.argv[2])
func=sys.argv[3]
"""

x,y,func=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]

#Function declaration
def calculator():
	if func == 'add':
		g=t.add_func(x,y)
		print(g)
		print("The addition of %s and %s is %s"%(x,y,g))
	elif func == 'minus':
		g=t.subtract_func(x,y)
		print(g)
		print("The subtraction of {} from {} is {}" .format(y,x,g))
	elif func == 'mul':
		g=t.multiply_func(x,y)
		print(g)
		print("The multiplication of {} and {} is {}" .format(x,y,g))

if __name__ == "__main__":
	calculator()
