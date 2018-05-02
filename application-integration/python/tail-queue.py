#!/usr/bin/env python
# Helper script to publish sample message to SQS queue
import yaml
import boto3
import sys

if len(sys.argv) < 1:
	print 'usage: tail-queue.py'
	sys.exit(1)

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

print ('Tailing SQS queue [%s]' %(sqs_url))

# Create SQS client
client = boto3.client(
    'sqs',
    aws_access_key_id=config['aws_access_key_id'],
    aws_secret_access_key=config['aws_secret_access_key'])

while True:
	# Purge
	response = client.receive_message(
		QueueUrl=sqs_url,
		AttributeNames= ['All'],
		MaxNumberOfMessages=5,
		WaitTimeSeconds=20
		)
	if "Messages" in response.keys():
		for message_payload in response['Messages']:
			print message_payload['Body']
