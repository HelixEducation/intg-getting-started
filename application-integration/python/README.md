# Python helper scripts
These scripts are useful for test integration purposes and require [Python 2.7](https://www.python.org/downloads/)

## Required Libraries
Run the following 2 commands from the command line to install the required libraries:
```
pip install pyyaml
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
The following commands are run from the terminal after you change path to the appropriate directory.
For Windows users, substitute a '\' for the '/' on *nix.
### Submitting a sample to the queue
For publishing a sample message to the SQS queue, this script reads the payload
from the specified file. The specified file can live anywhere, and should contain a JSON string as it's
only content.
```
./publish-application.py {application.json}
```

### Purging the queue
This script completely wipes the queue clean
```
./purge-queue.py
```
