#!/usr/bin/python

import boto3, botocore, sys, shutil as sh, time as t, os, psutil, gzip, pathlib as pl, tarfile, smtplib as s, cx_Oracle as cx, subprocess as sp, datetime as dt
from botocore.exceptions import ClientError

# Variable declaration
timestring=t.localtime()
TS=t.strftime('%m%d%Y%H%M%S', timestring)
current_time=t.time()
microseconds = "{:06d}".format(int((current_time - int(current_time)) * 1e6))

#Function declaration
def create_sts():
	#Create an STS service client
	sts_connection = boto3.client('sts')

	#Request for temporary credentials through STS using the role ARN
	assumed_role_object = sts_connection.assume_role(
	 RoleArn="arn:aws:iam::730335195244:role/Engineer",
	 RoleSessionName="Dev_Engineer")	
	
	#Get the credentials from the response
	credentials = assumed_role_object["Credentials"]

#	s3_client = boto3.client('s3', aws_access_key_id=credentials['AccessKeyId'],
	cloudtrail_client = boto3.client('cloudtrail', aws_access_key_id=credentials['AccessKeyId'],
	aws_secret_access_key=credentials['SecretAccessKey'], aws_session_token=credentials['SessionToken'])
#	return s3_client
	return cloudtrail_client


#Enabling Object Level Logging
def object_level_log(**kwargs):
	#Calling create STS function
	cloudtrail_client = create_sts()

	bucket_name = kwargs['bucket']
	trailname = kwargs['trail_name']
	try:
		session = boto3.session.Session()
	#	client = boto3.client('cloudtrail')
		response = cloudtrail_client.create_trail(
			Name=trailname,
			S3BucketName=bucket_name,
			IncludeGlobalServiceEvents=True,
			IsMultiRegionTrail=False,
			EnableLogFileValidation=True
			)
		print(response)
	except ClientError as error:
		print(error.response)

	try:
	#	client = boto3.client('cloudtrail')
		response = cloudtrail_client.put_event_selectors(
			TrailName=trailname,
			EventSelectors=[
				{
					'ReadWriteType': 'All',
					'IncludeManagementEvents': True,
					'DataResources': [
						{
							'Type': 'AWS::S3::Object',
							'Values': [
								'arn:aws:s3:::%s/'%(bucket_name)]
						}
					]
				}
			])
		print("The Object Level Logging for Bucket(%s) was enabled successfully...."%(bucket_name))
    #except TrailNotFoundException as error:
    #except ClientError as error:
       #print(error.response)
	except NameError as er:
		print("Name Error Exception is Caught", er)


def server_access_log(**kwargs):
	try:
		#Calling create STS function
		s3_client = create_sts()
		
		session = boto3.session.Session()
		bucket_name = kwargs['bucket']
		response = s3_client.put_bucket_logging(
			Bucket=bucket_name,
			BucketLoggingStatus={
				'LoggingEnabled': {
					'TargetBucket': kwargs['target_bucket'],
					'TargetPrefix': 'MyBucketLogs/'}})
		print("\n" + str(response))
	except ClientError as error:
		print(error.response)
		print("\n" + str(error.response['Error']['Message']))


def set_encryption(**kwargs):
	try:
		#Calling create STS function
		s3_client = create_sts()

		session = boto3.session.Session()
		bucket_name= kwargs['bucket']
		encrypt_status = kwargs['status']
		if encrypt_status == 'enable_kms':
			response = s3_client.put_bucket_encryption(
		    Bucket=bucket_name, ServerSideEncryptionConfiguration={
        		'Rules': [
            	{
               	 'ApplyServerSideEncryptionByDefault': {
                  	'SSEAlgorithm': 'aws:kms',
							'KMSMasterKeyID': kwargs['kms_key']}}]})
			get_response = s3_client.get_bucket_encryption(Bucket=bucket_name)
			print("\n" + str(response))
			print("\n\n" + str(get_response))
		elif encrypt_status == 'default':
			response = s3_client.delete_bucket_encryption(Bucket=bucket_name)
			get_response = s3_client.get_bucket_encryption(Bucket=bucket_name)
			print("\n" + str(response))
			print("\n\n" + str(get_response))
	except ClientError as error:
		print(error.response)


def set_versioning(**kwargs):
	try:	
		#Calling create STS function
		s3_client = create_sts()

		session = boto3.session.Session()
		bucket_name= kwargs['bucket']
		bucket_status = kwargs['status']
		if bucket_status == 'enable':
			response = s3_client.put_bucket_versioning(
    		Bucket=bucket_name, VersioningConfiguration={'Status': 'Enabled'})
		elif bucket_status == 'disable':
			response = s3_client.put_bucket_versioning(
			Bucket=bucket_name, VersioningConfiguration={'Status': 'Suspended'})
		print(response)
	except ClientError as error:
		print(error.response)
	

def list_bucket_content(**kwargs):
	try:	
		#Calling create STS function
		s3_client = create_sts()

		session = boto3.session.Session()
		bucket_name = kwargs['bucket']
		response = s3_client.list_objects(Bucket=bucket_name)
		print(response['Contents'][0]['Key'])
		object_list = []
		#Looping through 'response' to fetch a list of objects
		for obj in response['Contents']:
			if 'Key' in obj:
				object_list.append(obj['Key'])
		print(object_list)
	except ClientError as error:
		print(error.response)


def empty_bucket_content(**kwargs):
	try:
		#Calling create STS function
		s3_client = create_sts()
	
		session = boto3.session.Session()
		bucket_name = kwargs['bucket']
		response = s3_client.delete_objects(Bucket=bucket_name, Delete={'Objects':[{'Key': kwargs['object1']}, {'Key': kwargs['object2']}, {'Key': kwargs['object3']}]})
		print(response)
		deleted_objects = []
		#Looping through 'response' to fetch a list of deleted objects
		for obj in response['Deleted']:
			if 'Key' in obj:
				deleted_objects.append(obj['Key'])
		print("\n\n\nThe following objects were deleted: %s"%s(deleted_objects))
	except ClientError as error:
		print(error.response)

	
def upload_s3_bucket(**kwargs):
	#Calling create STS function
	s3_client = create_sts()

	session=boto3.session.Session()
	#Calling create bucket function
	bucket_name = create_s3_bucket(**kwargs)
	directory = kwargs['directory_name']
	folder = "/home/oracle/scripts/practicedir_iji_sep23/%s"%(directory)
	files = os.listdir(folder)

	#Looping through the folder to fetch files for upload
	for doc in files:
		file_path = os.path.join(folder, doc)
   	#Upload each file to the specified bucket
		response = s3_client.upload_file(file_path, bucket_name, doc)
		print("\n" + str(response))


def delete_s3_bucket(**kwargs):
   #Calling create STS function
	s3_client = create_sts()
	
	session=boto3.session.Session()
	bucket_name = kwargs['bucket']
	bucket_response = s3_client.delete_bucket(Bucket=bucket_name)
	print(bucket_response)
	if response['ResponseMetadata']['HTTPStatusCode'] == 204:
		print("%s was deleted successfully"%(kwargs['bucket']))


def create_s3_bucket(**kwargs):
	s3_client = create_sts()
	session=boto3.session.Session()
	bucket_name = kwargs['bucket']
	current_region = session.region_name
	if current_region == 'us-east-1':
		bucket_response = s3_client.create_bucket(Bucket=bucket_name)
	else:
		bucket_response = s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': current_region})
	print(bucket_response)
	print()
	print(bucket_name, current_region)
	return bucket_name, current_region
	

def read_db_create_grp(**kwargs):
	try:
		#Calling db_conections function
		db_connection(**kwargs)
	
		users = []
		#Connecting to Oracle database
		connection = cx.connect(user='STACK_ABI_SEP23', password='stackinc', dsn='MKIT-DEV-OEM/APEXDB')
		cursor = connection.cursor()
		cursor.execute("""select username from all_users where username like '%SEP23'""")
		rows = cursor.fetchall()
		#Looping through the rows to create users list
		for row in rows:
			users.append(row[0])
		print(users)

		#Calling create IAM Group function
		aws_create_group(**kwargs)

		#Looping through users list to create users and add each user to group
		for user in users:
			#Creating IAM users for username in list 
			aws_create_users(user=user, **kwargs)

			#Adding users to Group
	#	#iam = boto3.client(kwargs['service'])
	#	#response = iam.add_user_to_group(GroupName=kwargs['group'], UserName=user)
			response = aws_add_user_to_group(user=user, **kwargs) 
			print()
			print(response)
			print()
			# Creating login profile for User
	#	response_profile = iam.create_login_profile(UserName=user, Password=kwargs['password'], PasswordResetRequired=True)
			print()
	#	print(response_profile)
			print()
			#Checking exit statuses of create group 
	#	if response['ResponseMetadata']['HTTPStatusCode'] == 200 and response_profile['ResponseMetadata']['HTTPStatusCode'] == 200:
			if response['ResponseMetadata']['HTTPStatusCode'] == 200:
				print("{} added to {} user group successfully and login profile created successfully".format(user, kwargs['group']))
				#Calling db_conections function
				kwargs['STATUS']='Completed'
				db_connection(**kwargs)
			else:
				#Calling db_conections function for failed status
				kwargs['STATUS']='Error'
				db_connection(**kwargs)
	except Exception as e:
		print("Export failed! Error: %s"%(str(e)))

def aws_add_user_to_group(**kwargs):
	try:
		# Adding IAM User to Group
		iam = boto3.client(kwargs['service'])
		response = iam.add_user_to_group(GroupName=kwargs['group'], UserName=kwargs['user'])
		print()
		print(response)

		# Creating login profile for User
		response_profile = iam.create_login_profile(UserName=kwargs['user'], Password=kwargs['password'], PasswordResetRequired=True)
		print()
		print(response_profile)
		return response_profile
		print()
 		#Checking exit statuses of create group and add user to group
		if response['ResponseMetadata']['HTTPStatusCode'] == 200 and response_profile['ResponseMetadata']['HTTPStatusCode'] == 200:
			print()
			print("{} added to {} successfully and login profile created successfully".format(kwargs['user'], kwargs['group']))

			#Calling db_conections function
			kwargs['STATUS']='Completed'
			db_connection(**kwargs)
	except ClientError as error:
		print(error.response)
		print(error.response_profile)
		if error.response['Error']['Code'] == "NoSuchEntity":
			print('Group does not exist...Create new group?')
			#Calling db_conections function
			kwargs['STATUS']='Error'
			db_connection(**kwargs)			

			val = input('Enter (y or n): ')
			if val == 'n':
				print('You want to use the same group')
				pass
			else:
				print('You want to create a new group')
				# Creating a new group
				new_group = input('Enter group name: ')
				response = iam.create_group(GroupName=new_group)
				print(response)
				# Adding User to Group
				response_adduser = iam.add_user_to_group(GroupName=new_group, UserName=kwargs['user'])	
				print()
				print(response_adduser)
				print()
		elif error.response_profile['Error']['Code'] == "EntityAlreadyExists":
			print('User already exists in Group...Add the same user?')
			#Calling db_conections function
			kwargs['STATUS']='Error'
			db_connection(**kwargs)

			val = input("Enter (y or n): ")
			if val == 'y':
				print('You want to add the same user')
				pass
			else:
				print('You want to add a new user')
				new_user=input("Enter User Name: ")
				response= iam.add_user_to_group(GroupName=kwargs['group'], UserName=new_user)
				print(response)
		elif error.response_profile['Error']['Code'] == "PasswordPolicyViolation":
			print("There is a password policy violation...Enter a new password?")
			complex_password = input("Enter a complex password: ")
			# Re-creating login profile for user
			response_profile = iam.create_login_profile(UserName=kwargs['user'], Password=complex_password, PasswordResetRequired=False)
			print(response_profile)
		else:
			print('Unexpected error occured while adding user to group... exiting from here', error)
			return 'User could not be added to Group', error	
			#Calling db_conections function					
			kwargs['STATUS']='Error'
			db_connection(**kwargs)

def aws_create_group(**kwargs):
	#Calling db_conections function
#	db_connection(**kwargs) -- To be edited after IAM row is created in the DB
	try:
		# Creating IAM Group
		iam = boto3.client(kwargs['service'])
		response = iam.create_group(GroupName=kwargs['group'])
		print(response)
		
		# Attaching admin policy to Group
		response_policy = iam.attach_group_policy(
			GroupName=kwargs['group'],
			PolicyArn=kwargs['policy_arn'])
		print()
		print(response_policy)
		print()
		if response['ResponseMetadata']['HTTPStatusCode'] == 200 and response_policy['ResponseMetadata']['HTTPStatusCode'] == 200:
			print()
			print("{} created successfully and policy attached successfully".format(kwargs['group']))
			#Calling db_conections function
			kwargs['STATUS']='Completed'
#			db_connection(**kwargs) -- To be edited after IAM row is created in the DB

	except ClientError as error:
		print(error.response)
		if error.response['Error']['Code'] == "EntityAlreadyExists":
			print('Group already exists...Use the same group?')

			#Calling db_conections function
			kwargs['STATUS']='Error'
#			db_connection(**kwargs)  #-- To be edited after IAM row is created in the DB

			val = input('Enter (y or n): ')
			if val == 'y':
				print('You want to use the same group')
				pass
			else:
				print('You want to create a new group')
				new_group = input('Enter group name: ')
				response = iam.create_group(GroupName=new_group)
				print(response)
		else:
			print('Unexpected error occured while creating group... exiting from here', error)
			return 'Group could not be created', error
			#Calling db_conections function
			kwargs['STATUS']='Error'
			db_connection(**kwargs)  #-- To be edited after IAM row is created in the DB


def aws_create_users(**kwargs):
	#Calling db_conections function
	db_connection(**kwargs)
	try:
		iam= boto3.client(kwargs['service'])
		response= iam.create_user(UserName=kwargs['user'])
		print(response)
		if response['ResponseMetadata']['HTTPStatusCode'] == 200:
			print()
			print("{} was successfully created".format(kwargs['user']))
			#Calling db_conections function
			kwargs['STATUS']='Completed'
			db_connection(**kwargs)
			
	except ClientError as error:
		print(error.response)
		if error.response['Error']['Code'] == "EntityAlreadyExists":
			print('User already exists...Use the same user?')
			#Calling db_conections function
			kwargs['STATUS']='Error'
			db_connection(**kwargs)

			val = input("Enter (y or n): ")
			if val == 'y':
				print('You want to use the same user')
				pass
			else:
				print('You want to create a new user')
				new_user=input("Enter User Name: ")
				response= iam.create_user(UserName=new_user)
				print(response)
		else:
			print('Unexpected error occured while creating user... exiting from here', error)
			return 'User could not be created', error
			#Calling db_conections function
			kwkwargs['STATUS']='Error'
			db_connection(**kwargs)


def db_connection(**kwargs):
	# Connecting to Oracle database
	connection = cx.connect(user='STACK_ABI_SEP23', password='stackinc', dsn='MKIT-DEV-OEM/APEXDB')
	print(connection.version)
	cursor = connection.cursor()
	op_name = kwargs['op_name']
	#Reading OP_ID from PROD_OPERATIONS table
	cursor.execute("""select OP_ID from PROD_OPERATIONS where OP_NAME = :OP_NAME_INS""", OP_NAME_INS = op_name)
	#Extracting OP_ID from the "select" statement
	read_op_id = cursor.fetchone()[0]
	print("PROD_OPERATIONS table OP_ID is %s"%(read_op_id))

	#Reading MONITORING_EMAIL from PROD_OPERATIONS table
	cursor.execute("""select MONITORING_EMAIL from PROD_OPERATIONS where OP_NAME = :OP_NAME_INS""", OP_NAME_INS = op_name)
	#Extracting MONITORING_EMAIL from the "select" statement
	read_monitoring_email = cursor.fetchone()[0]
	print("PROD_OPERATIONS table MONITORING_EMAIL is %s"%(read_monitoring_email))

#	try:
	if kwargs['STATUS'] == 'Running':
		# Variable Declaration
		timestring = dt.datetime.now()
		current_time= timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		starttime = current_time.upper()
		OP_STARTTIME = starttime
		endtime = current_time.upper()
		OP_ENDTIME = endtime
		print()
		print(starttime)
		print()

		#Inserting into the PROD_ACTIVITIES table
		cursor.execute("""insert into PROD_ACTIVITIES values (:OP_ID_INS, :OP_STARTTIME_INS, :OP_ENDTIME_INS, :RUNNER_INS, :STATUS_INS, :MON_EMAIL_INS)""",
		OP_ID_INS = read_op_id,
		OP_STARTTIME_INS = OP_STARTTIME,
		OP_ENDTIME_INS = OP_ENDTIME,
		RUNNER_INS = kwargs['RUNNER'],
		STATUS_INS = kwargs['STATUS'],
		MON_EMAIL_INS = read_monitoring_email)

		connection.commit()
		cursor.close()
		connection.close()

	elif kwargs['STATUS'] == 'Completed':
		timestring2 = dt.datetime.now()
		current_time2= timestring2.strftime("%d-%b-%y %I.%M.%S.%f %p")
		endtime2 = current_time2.upper()
		OP_ENDTIME=endtime2
		STATUS='Completed'
		#op_name = kwargs['op_name']
		connection = cx.connect(user='STACK_ABI_SEP23', password='stackinc', dsn='MKIT-DEV-OEM/APEXDB')
		cursor = connection.cursor()
		cursor.execute("""update PROD_ACTIVITIES set OP_ENDTIME = :OP_ENDTIME_INS, STATUS = :STATUS_INS where OP_ID = :OP_ID_INS""", OP_ID_INS = read_op_id, OP_ENDTIME_INS = OP_ENDTIME, STATUS_INS = STATUS)

		#Using a "SELECT...JOIN" to print out an ouput
		cursor.execute("""select a.OP_ID, a.OP_NAME, a.OP_TYPE, b.OP_STARTTIME, b.OP_ENDTIME, b.MON_EMAIL from PROD_OPERATIONS A FULL join PROD_ACTIVITIES B on a.OP_ID=b.OP_ID where a.OP_NAME = :OP_NAME_INS and b.RUNNER = :RUNNER_INS""",OP_NAME_INS = op_name, RUNNER_INS=kwargs['RUNNER'])

		results = cursor.fetchall()
		"""
		for row in results:
			print("OP_ID: {}, OP_NAME: {}, OP_TYPE: {}, OP_STARTTIME: {}, OP_ENDTIME: {}, MON_EMAIL: {}".format(row[0], row[1], row[2], row[3], row[4], row[5])) 
		"""
		connection.commit()
		cursor.close()
		connection.close()
	
	else:
		kwargs['STATUS'] = 'Error'
		timestring = dt.datetime.now()
		current_time= timestring.strftime("%d-%b-%y %I.%M.%S.%f %p")
		OP_STARTTIME = current_time.upper()
		OP_ENDTIME = current_time.upper()
		connection = cx.connect(user='STACK_ABI_SEP23', password='stackinc', dsn='MKIT-DEV-OEM/APEXDB')
		cursor = connection.cursor()
		cursor.execute("""insert into PROD_ACTIVITIES values (:OP_ID_INS, :OP_STARTTIME_INS, :OP_ENDTIME_INS, :RUNNER_INS, :STATUS_INS, :MON_EMAIL_INS)""", OP_ID_INS = read_op_id, OP_STARTTIME_INS = OP_STARTTIME, OP_ENDTIME_INS = OP_ENDTIME, RUNNER_INS = kwargs['RUNNER'], STATUS_INS = kwargs['STATUS'], MON_EMAIL_INS = read_monitoring_email)
		connection.commit()
		cursor.close()
		connection.close()
		exit()
#	except Exception as e:
#		print("Error writing into the database! Error: %s"%(str(e)))
#		exit()

def STACK_EMAIL(**kwargs):
   # Variables
	FROM='oracle@MKIT-DEV-OEM.localdomain'
	BODY=""
	MSG = ("\n".join(("From: %s" %FROM, "To: %s" %(kwargs['TO_EMAIL']), "Subject: %s:\n" %(kwargs['SUBJECT']), "%s" %BODY)))
	with s.SMTP('localhost') as my_server:
		my_server.sendmail(FROM, kwargs['TO_EMAIL'], MSG)
		print("Email sent successfully to %s" %(kwargs['TO_EMAIL']))


def database_backup_function(**kwargs):
	# Calling the db_connection() function
#	op_name = "Export"
	db_connection(**kwargs)

   #Database backup function variable declaration
	backup_dir = os.path.join(kwargs['backup_location'], kwargs['RUNNER'], TS)
	os.makedirs(backup_dir)
	OP_STARTTIME_INS = t.strftime('%d-%b-%y %I.%M.%S', timestring) + ".{} %p".format(microseconds)
	try:
      #Writing into .par file
		with open('%s/export_%s_%s.par'%(kwargs['practicedir'], kwargs['RUNNER'], TS), 'w+') as pf:
			pf.write('userid="/ as sysdba"\n''schemas=stack_temp\n''logfile={x}_{y}_{z}.log\n''dumpfile={x}_{y}_{z}.dmp\n''directory=DATA_PUMP_DIR'.format(x=kwargs['schemas'], y=kwargs['RUNNER'], z=TS))
		print("Is {} closed? {}".format(pf.name, pf.closed))

      #Reading from .par file
		with open('export_%s_%s.par'%(kwargs['RUNNER'], TS), 'r+') as pf:
			output = pf.read()
		print("Is {} closed? {}".format(pf.name, pf.closed))

      #Creating script for export
		with open('{}/export_script.sh'.format(kwargs['practicedir']), 'w+') as export:
			export.write('. /home/oracle/scripts/oracle_env_APEXDB.sh\n''expdp parfile=%s/export_%s_%s.par'%(kwargs['practicedir'], kwargs['RUNNER'], TS))
		print("Is {} closed? {}".format(export.name, export.closed))
		export_command='{}/export_script.sh'.format(kwargs['practicedir'])
		os.popen("chmod 700 {}".format(export_command))
      #Running expdp command to initiate database export
		export_result = os.popen('%s'%export_command).read()

		#Creating a variable for logfile path 
		logfile_path = "{}/{}_{}_{}.log".format(kwargs['backup_location'], kwargs['schemas'], kwargs['RUNNER'], TS)
		
		#Checking logfile for success message
		with open(logfile_path, 'r') as lfp:
			output = lfp.read()
			if "successfully completed" in output:
				print("Database export was successful")
				kwargs['STATUS']='Completed'		

			# Calling the db_connection() function
			db_connection(**kwargs)
	except Exception as e:
		print("Export failed! Error: %s"%(str(e)))


def G_Zipp(**kwargs):
	# Checking if user wants to compress a file or directory
	if os.path.isfile(kwargs['source_path']):
		with open(kwargs['source_path'], 'rb') as my_input:
			with gzip.open(kwargs['output_gzip'], 'wb') as my_output: ##### Changes
				sh.copyfileobj(my_input, my_output)
				print("Successfully zipped file %s to %s"%(kwargs['source_path'], kwargs['output_gzip']))
	elif os.path.isdir(kwargs['source_path']):
		# Creating a temporary tar archive name
		tar_filename = '{}.tar'.format(kwargs['source_path'])
		# Opening the temporary tar archive for writing
		with tarfile.open(tar_filename, 'w') as tar:
			# Adding the entire content of the source directory to the tar archive. The arcname parameter ensures that the files in the archive have the same names as they do in the original directory.
			tar.add('%s'%(kwargs['source_path']))
		#Opening the temporary tar archive file for reading in binary mode (rb)
		with open(tar_filename, 'rb') as my_input_tar_file:
			# Opening the target gzip file for writing in binary mode (wb). This is where the compressed data will be written.
			with gzip.open('%s'%(kwargs['output_gzip']), 'wb') as my_output_gzip_file:  ### Changes
				sh.copyfileobj(my_input_tar_file, my_output_gzip_file)
				print("Successfully zipped directory %s to %s"%(kwargs['source_path'], kwargs['output_gzip']))
		# Removing the temporary tar archive
		#p.Path(tar_filename).unlink()
	else:
		print("Error! {} is neither a file nor directory".format(kwargs['source_path']))


def Unzipp(**kwargs):
	# Checking if user wants to unzip a file or directory
	#try:
	if kwargs['zip_type'] == 'f': # Zipped file
		# Reading the content of the gzipped file
		with gzip.open(kwargs['source_path'], 'rb') as f:
			file_content = f.read()
			#print(file_content)
			# Writing unzipped file content into an output file in my cwd
			with open(kwargs['output_f_d'], 'wb') as wf:
				wf.write(file_content)
			print("Unzipped content has been written to %s"%(kwargs['output_f_d']))
	elif kwargs['zip_type'] == "d": # Zipped directory
		# Open the compressed directory
		with gzip.open(kwargs['source_path'], 'rb') as com_dir:
   		# Open the tar archive
			with tarfile.open(fileobj = com_dir, mode = 'r') as tar:
				tar.extractall(kwargs['output_f_d'])
		# This assigns the Path object created from output_f_d to the variable target_path.
		target_path = pl.Path(kwargs['output_f_d'])
		target_path_TS = os.path.join(str(target_path), TS) # Adding a timestamp
		# Create location where the zipped directory will be extracted
		os.popen("mkdir -p {}".format(target_path_TS))
	
	#except:
	#	print("Failed to unzip!")


def disk_maintenance_check_on_prem(**kwargs):
	# Calling the db_connection() function
	db_connection(**kwargs) 
	while True:
		partition = psutil.disk_usage(kwargs['disk'])
		disk_utilization = partition.percent
		
		BODY=''
		print("Disk utilization is at %s"%disk_utilization)
		# Checking Critical Threshold
		if disk_utilization >= float(kwargs['critical_threshold']): 
			print("DANGER!!! Disk utilization is at {}%, over {}% threshold. Sending email alert in 1 minutes".format(disk_utilization, kwargs['critical_threshold']))
			body_content = "Danger!!! Disk utilization is at %s%%, over %s%% threshold."%(disk_utilization, kwargs['critical_threshold'])
			# Using the sleep function to enable the code wait before alerting
			t.sleep(60)
			STACK_EMAIL(TO_EMAIL=kwargs['TO_EMAIL'], SUBJECT=kwargs['SUBJECT'], BODY=body_content)
			
			# Check the exit status
			exit_status = 0

			if exit_status == 0:
				kwargs['STATUS']='Completed'

   			# Calling the db_connection() function
				db_connection(**kwargs)
		# Checking Warning Threshold
		if disk_utilization >= float(kwargs['warning_threshold']):
			print("Warning!!! Disk utilization is at {}%, over {}% threshold. Sending email alert in 5 minutes".format(disk_utilization, kwargs['warning_threshold']))
			body_content = "Warning!!! Disk utilization is at %s%%, over %s%% threshold."%(disk_utilization, kwargs['warning_threshold'])
         # Using the sleep function to enable the code wait before alerting
			t.sleep(60)
			STACK_EMAIL(TO_EMAIL=kwargs['TO_EMAIL'], SUBJECT=kwargs['SUBJECT'], BODY=body_content)		
			# Check the exit status
			exit_status = 0

			if exit_status == 0:
				kwargs['STATUS']='Completed'

   			# Calling the db_connection() function
				db_connection(**kwargs)


def backup_function(**kwargs):
	try:
		# Calling the db_connection() function
		db_connection(**kwargs)	

		#Backup type check
		if os.path.isfile(kwargs['source']):
			sh.copy(kwargs['source'], kwargs['destination'])
			print("\nSuccessfully copied from {} to {}".format(kwargs['source'], kwargs['destination']))
		elif os.path.isdir(kwargs['source']):
			sh.copytree(kwargs['source'], kwargs['destination'])
			print("\nSuccessfully copied from %s to %s" %(kwargs['source'], kwargs['destination']))
	
		# Check the exit status
		exit_status = 0

		if exit_status == 0:
			kwargs['STATUS']='Completed'

			# Calling the db_connection() function
			db_connection(**kwargs)
	except Exception as e:
		print("Error: %s"%(str(e)))
		exit_status = 1
	

def database_import(**kwargs):

	# Calling the gzipp function to compress the dump file
	dumpfile = '{}/{}_{}_{}.dmp'.format(kwargs['backup_location'], kwargs['schemas'], kwargs['RUNNER'], TS)
	gzipped_dumpfile = '{}.gzip'.format(dumpfile)
	G_Zipp(source_path=dumpfile, output_gzip=gzipped_dumpfile) ###---Regular Call 1.13**

	# Calling the unzip function to unzip the dumpfile
	unzipped_dumpfile = gzipped_dumpfile.replace('.gzip', '')
	Unzipp(source_path=gzipped_dumpfile, output_f_d=unzipped_dumpfile, zip_type='f') ###---Regular Call 1.13**

	# Copying unzipped dumpfile to SAMD directory
	sh.copy(unzipped_dumpfile, '/backup/AWSSEP23/SAMD')  ###---Regular Call 1.13**
	new_dumpfile_path = os.path.join('/backup/AWSSEP23/SAMD', unzipped_dumpfile)  ###---Regular Call 1.13**
	new_dumpfile = os.path.basename(new_dumpfile_path)

	print()
	print(new_dumpfile)
	print()

	##Creating the impdp par file
	print("Creating the impdp par file")
	with open('impdp_%s_%s.par'%(kwargs['schemas'], kwargs['RUNNER']), 'w+') as pf:

		pf.write('userid="/ as sysdba"\n''schemas={x}\n''remap_schema={x}:{x}_{y}_{z}\n''dumpfile={dumpfile}\n''logfile=impdp_{x}_{y}.log\n''directory={a}\n''table_exists_action=replace'.format(x=kwargs['schemas'], y=kwargs['RUNNER'], z=TS, a=kwargs['datapump_dir'], dumpfile=new_dumpfile))

	#Creating the impdp script that will be used to run the import
	print("Creating impdp script that will be used to run the import")
	with open('import_{}.sh'.format(kwargs['schemas']), 'w+') as pf:
		pf.write('. /home/oracle/scripts/oracle_env_{}.sh\n''impdp parfile={}/impdp_{}_{}.par'.format(kwargs['import_DB'], kwargs['practicedir'], kwargs['schemas'], kwargs['RUNNER']))

	import_command = '{}/import_{}.sh'.format(kwargs['practicedir'], kwargs['schemas'])
	os.popen("chmod 744 {}".format(import_command))
	#Running impdp command to initiate database import
	import_result = os.popen("{}".format(import_command)).read()		


def DATA_MIGRATION(**kwargs):
	# Calling the database backup function
	database_backup_function(**kwargs)

	# Calling the database import function
	database_import(**kwargs)


# Main Body
if __name__ == '__main__':
	decision_no = sys.argv[1]
	if decision_no == "1":
		source=sys.argv[2]
		destination=sys.argv[3]
		bk_type=sys.argv[4]
		backup_function(source, destination, bk_type)

	elif decision_no == "2":
		database_backup_function()
	
	elif decision_no == "3":
		disk = sys.argv[2]
		threshold = sys.argv[3]
		disk_maintenance_check_on_prem(disk, threshold)	

	elif decision_no == "4":
		source_path = sys.argv[2]
		output_gzip = sys.argv[3]
		G_Zipp(source_path, output_gzip)	

	elif decision_no == "5":
		source_path = sys.argv[2]
		output_file = sys.argv[3]
		Unzipp(source_path, output_file)
