# Python helper scripts
These scripts are useful for test integration purposes and require [Python 2.7](https://www.python.org/downloads/)

## Required Libraries
Run the following 2 commands from the command line to install the required libraries:
```
pip install yml
pip install boto3
```
## Configuration
This script requires a file in the same directory titled `config.yml` that includes the following info:
```
aws_region: us-west-2
aws_access_key_id: {access key with permission to publish to SQS queue}
aws_secret_access_key: {your secret}
sqs_url: {fully qualified URL of the SQS queue, e.g. https://sqs.us-west-2.amazonaws.com/{account_id}/{queue_name}
```

## Usage
### Submitting a sample to the queue
For publishing a sample message to the SQS queue, this script reads the payload
from the specified file.
```
./submit-application.py {application.json}
```

### Purging the queue
This script completely wipes the queue clean
```
./purge-queue.py
```
