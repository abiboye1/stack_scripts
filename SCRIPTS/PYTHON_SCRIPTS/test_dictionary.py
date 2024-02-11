#!/usr/bin/python

import sys, stack_modules2 as s

hostname=sys.argv[1]
def new_func():
	call_func=s.get_server_dictionary()
	"""
	#if call_func["Hosts"]["MKIT-DEV-OEM"] == hostname:
	if call_func["Hosts"][hostname] == "MKIT-DEV-OEM":
		print("It is an on-prem server")
	#elif call_func["Hosts"]["STACKCLOUD"] == hostname:
	elif call_func["Hosts"][hostname] == "STACKCLOUD":
		print("It is a cloud server")
	"""
	if hostname in call_func["Hosts"]:
		server_type = call_func["Hosts"][hostname]
		if server_type == "ON-PREM":
			print("It is an on-prem server")
		elif server_type == "CLOUD":
			print("It is a cloud server")			

	else:
		print("Hostname not found in dictionary")
if __name__ == "__main__":
	new_func()
