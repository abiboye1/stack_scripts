#!/usr/bin/python

#Declaring function
"""
def add_func(a,b):
	z=a+b
	return z

def subtract_func(a,b):
	z=a-b
	return z

def multiply_func(a,b):
	z=a*b
	return z
"""
def test_dict():
	servers={
    "Hosts":{"MKIT-DEV-OEM":"ON-PREM", "STACKCLOUD":"CLOUD"},
    "Disks":["/u01", "/u02", "/u03", "/u04", "/u05", "/backup"],
    "Transient_directory_path": [{"/u01":"/u01/app/oracle/admin/APEXDB/adump"}, {"/backup":"/backup/AWSJUL22/RAMSEY/FILE"}]
}
	return servers

if __name__ == "__main__":
	test_dict()
"""
	add_func()
	subtract_func()
	multiply_func()
"""
