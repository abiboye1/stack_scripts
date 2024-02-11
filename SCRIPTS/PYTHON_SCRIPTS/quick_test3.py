#!/usr/bin/python

import sys, stack_modules2 as s

#Variable declaration
hostname=sys.argv[1]

def new_func():
	call_funct=s.get_server_dictionary()
	if hostname in call_funct["Hosts"]:
		server_type=call_funct["Hosts"][hostname]

		if server_type == "ON-PREM":
			print("This is an on-prem server")
		elif server_type == "CLOUD":
			print("This is a cloud server")

if __name__ == "__main__":
	new_func()
	
