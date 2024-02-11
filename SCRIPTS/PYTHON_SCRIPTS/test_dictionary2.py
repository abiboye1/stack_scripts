#!/usr/bin/bash

import sys, stack_modules2 as s

hostname=sys.argv[1]

def new_func():
	call_func=s.get_server_dictionary()
	if hostname in call_func["Hosts"]:
		server_type=call_func["Hosts"][hostname]
		if server_type=="ON-PREM":
			print("This is an on-prem server")
		elif server_type=="CLOUD":
			print("This is a cloud server")
		else:
			print("Invalid server type")
	


if __name__ == "__main__":
	new_func()
