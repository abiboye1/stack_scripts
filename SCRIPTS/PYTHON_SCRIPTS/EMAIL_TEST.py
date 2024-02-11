#!/usr/bin/python

import smtplib as s

# Variables
TO_EMAIL = 'stackcloud11@mkitconsulting.net'
SUBJECT = 'Test Email Abib'
BODY = "This is a test email"
FROM='oracle@MKIT-DEV_OEM.localdomain'

MSG = ("\n".join(("From: %s" %FROM, "To: %s" %TO_EMAIL, "Subject: %s:\n" %SUBJECT, "%s" %BODY)))

with s.SMTP('localhost') as my_server:
	my_server.sendmail(FROM, TO_EMAIL, MSG)
	print("Email sent successfully to %s" %TO_EMAIL)
