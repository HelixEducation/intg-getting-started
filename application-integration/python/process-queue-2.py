#!/usr/bin/env python3
# Helper script to publish sample message to SQS queue
import yaml
import boto3
import sys
import json
import os
import datetime


#print('*********************************')
#print("\n Default Date Object:", current_day, "\n")
#print('*********************************')


if len(sys.argv) < 1:
	print ('usage: process-queue.py')
	sys.exit(1)

# Load config file
config = None
with open(sys.argv[1], "r") as stream:
	try:
		config = list(yaml.load_all(stream))[0]
	except yaml.YAMLError as ex:
		print(ex)
		sys.exit(1)

# Variables
sqs_url = config['sqs_url']

print ('Tailing SQS queue [%s]' %(sqs_url))

# Create SQS client
sqs_client = boto3.client(
    'sqs',
    aws_access_key_id=config['aws_access_key_id'],
    aws_secret_access_key=config['aws_secret_access_key'])

s3_client = boto3.client(
	's3',
	aws_access_key_id=config['aws_access_key_id'],
    aws_secret_access_key=config['aws_secret_access_key'])

moreMessages = True

while moreMessages:
	# Purge
	response = sqs_client.receive_message(
		QueueUrl=sqs_url,
		AttributeNames= ['All'],
		MaxNumberOfMessages=5,
		WaitTimeSeconds=5
		)
	if "Messages" in response.keys():
		for message_payload in response['Messages']:
			# print message_payload['Body']

			# Create Python object from JSON string
			studentApplication = json.loads(message_payload['Body'])['events'][0]

			personalInfo = studentApplication['entity']['personalInformation']
			contactInfo = studentApplication['entity']['contactInformation']
			raceAndEthnicity = studentApplication['entity']['raceAndEthnicity']
			maritalInformation = studentApplication['entity']['maritalInformation']
			militaryService = studentApplication['entity']['militaryService']
			previousCollegeArray = studentApplication['entity']['previousCollege']
			employmentInformationArray = studentApplication['entity']['employmentInformation']
			documentsArray = studentApplication['entity']['documents']

			print ('Processing Student Application for: ' + personalInfo['firstname'] + ' ' + personalInfo['lastname'])
			#print (personalInfo['lastname'] + '.json')
			#print (personalInfo['firstname'] + personalInfo['lastname'] + '.json this is a test')
			print (message_payload['Body']) 

			#original_directory = os.getcwd()
			#directory = (personalInfo['firstname'] + '_' + personalInfo['lastname'])

			#os.mkdir(directory)

			#print (os.getcwd())
			#os.chdir(directory)
				
			birthdate = personalInfo['dateofBirth']

			birthdate_change = datetime.datetime.strptime(birthdate, '%m/%d/%Y').strftime('%d-%m-%Y')
			print (birthdate_change)

			converted_birthdate = (birthdate_change.replace("-",""))
			
			original_stdout = sys.stdout

			with open(personalInfo['firstname'] + '_' + personalInfo['lastname']  + '_' + converted_birthdate + '.json', 'w') as f:
				sys.stdout = f
				print (message_payload['Body']) 
				sys.stdout = original_stdout



			# TODO: Insert into SIS or other third-party system
			# Create Student in SIS
			# Create Enrollment in SIS
			# Etc.
			###### YOUR CODE HERE #######

			# Download all files from AWS S3
			for document in documentsArray:
				print (document['url'])
				url_components = document['url'].split('/')

				# Parse URL for the pieces I need
				bucket = url_components[2].split('.')[0]

				partner = url_components[3]
				student_id = url_components[4]

				# Need to URL Decode string name
				filename = url_components[5].replace('+', ' ')
				string_sequence = (partner, student_id, filename)
				#string_sequence = (partner, student_id)
				s3_file_key = '/'.join(string_sequence)

				personalInfo = studentApplication['entity']['personalInformation']
				print ('Pulling from bucket: ' + bucket + ' and s3 file key: ' + s3_file_key)
				#print ('Merging student name with filename: ' + personalInfo['firstname'] + '_' + personalInfo['lastname'] + '_' + filename)



				local_filename = (personalInfo['firstname'] + '_' + personalInfo['lastname'] + '_' + converted_birthdate + '_' + filename)
				#local_filename = filename

				# Download file to 'local_filename'
				s3_client.download_file(bucket, s3_file_key, local_filename)
				#s3_client.download_file(bucket, s3_file_key)

			#os.chdir(original_directory)

	else:
		moreMessages = False

if len(sys.argv) < 1:
	#print ('usage: purge-queue.py')
	sys.exit(1)

# Reaffirm from command line
are_you_sure = (sys.argv[2])

if are_you_sure == 'y':
	# Load config file
	config = None
	with open(sys.argv[1], "r") as stream:
		try:
			config = list(yaml.load_all(stream))[0]
		except yaml.YAMLError as ex:
			print(ex)
			sys.exit(1)

	# Variables
	sqs_url = config['sqs_url']

	print ('Purging SQS queue [%s]' %(sqs_url))

	# Create SQS client
	client = boto3.client(
	    'sqs',
	    aws_access_key_id=config['aws_access_key_id'],
	    aws_secret_access_key=config['aws_secret_access_key'])

	# Purge
	client.purge_queue(QueueUrl=sqs_url)
else:
	# Not sure
	print ('Ok. Good bye!')
	sys.exit(0)