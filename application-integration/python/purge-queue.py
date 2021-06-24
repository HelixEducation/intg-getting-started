#!/usr/bin/env python3
# Helper script to publish sample message to SQS queue
import yaml
import boto3
import sys

if len(sys.argv) < 1:
	print ('usage: purge-queue.py')
	sys.exit(1)

# Reaffirm from command line
are_you_sure = input('Are you sure you want to do this (y/n)?')

if are_you_sure == 'y':
	# Load config file
	config = None
	with open("config.yml", "r") as stream:
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
