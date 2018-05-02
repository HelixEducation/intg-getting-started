#!/usr/bin/env python
# Helper script to publish sample message to SQS queue
import yaml
import boto3
import sys

if len(sys.argv) < 2:
	print 'usage: publish-application.py {filename}}'
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

with open(filename, 'r') as applicationfile:
    data=applicationfile.read().replace('\n', '')

session = boto3.Session(profile_name='default')
client = session.client('sqs').send_message(
    QueueUrl=sqs_url,
    MessageBody=data,
    MessageAttributes={
        'string': {
            'StringValue': 'string',
            'DataType': 'String'
        }
    }
)
