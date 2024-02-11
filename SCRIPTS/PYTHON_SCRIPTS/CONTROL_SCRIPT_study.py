#!/usr/bin/python

import sys, stack_modules as s, socket

HN = socket.gethostname()

def new_func():
	call_func=s.test_dict()
	server = call_func["Hosts"]['{}'.format(HN)]	
	#if call_func["Hosts"]['{}'.format(HN)] == "ON-PREM":
	if server == "ON-PREM":
		print("The hostname is {} and is an {} server".format(HN, server))
	elif server == "CLOUD":
		print("The hostname is {} and is a {} server".format(HN, server))
	
if __name__ == "__main__":
	new_func()
