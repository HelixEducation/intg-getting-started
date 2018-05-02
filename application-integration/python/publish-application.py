#!/usr/bin/env python
# Helper script to publish sample message to SQS queue
import yaml
import boto3
import sys

if len(sys.argv) < 2:
	print 'usage: publish-application.py {filename}'
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
filename = sys.argv[1]
sqs_url = config['sqs_url']

print ('Sending to [%s] from filename: %s' %(sqs_url, filename))

# Read the app.json payload from the specified file
with open(filename, 'r') as applicationfile:
    application_json=applicationfile.read().replace('\n', '')

# Create SQS client
client = boto3.client(
    'sqs',
    aws_access_key_id=config['aws_access_key_id'],
    aws_secret_access_key=config['aws_secret_access_key'])

# Publish
client.send_message(
    QueueUrl=sqs_url,
    MessageBody=application_json,
    MessageAttributes={
        'string': {
            'StringValue': 'string',
            'DataType': 'String'
            }
        }
    )
