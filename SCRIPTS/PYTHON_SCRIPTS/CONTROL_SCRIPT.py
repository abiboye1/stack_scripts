#!/usr/bin/python

import sys, stack_modules2 as t, socket as s

#Variable declaration
hostname = s.gethostname()

def check_dictionary():
	dict_output=t.get_server_dictionary()
	server = dict_output["Hosts"]["%s"%(hostname)]
	if server == "ON-PREM":
		print("The hostname is %s and is an %s server"%(hostname, server))
	elif server == "CLOUD":
		print("The hostname is %s and is a %s server"%(hostname, server))

def call_db_backup():
	t.database_backup()


if __name__ == "__main__":
	"""
	calculator()
	
	dict_output=t.get_server_dictionary()
	print(dict_output)
	"""
	check_dictionary()
