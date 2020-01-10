# Python helper scripts
These scripts are targeted for Python3 (as of January 2020).

## Required Libraries
Run the following 2 commands from the command line to install the required libraries:
```
pip3 install pyyaml
pip3 install boto3
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
For Windows users, substitute a '\\' for the '/' on *nix.
### Submitting a sample to the queue
For publishing a sample message to the SQS queue, this script reads the payload
from the specified file. The specified file can live anywhere, and should contain a JSON string as it's
only content.
```
./publish-application.py {application.json}
```

### Processing all queue messages
This script uses the `config.yml` file to connect to a remote AWS SQS and pull
(but not delete) all messages on the queue, as well as download all attached files
from AWDS SQS. This is a good starting spot for seeing what messages
are currently on the queue, and jumping off point for
processing the applications into your SIS.
```
./process-queue.py
```

### Purging the queue
This script completely wipes the queue clean
```
./purge-queue.py
```

### Tailing a queue
Polls the queue continuously and logs any messages it sees to stdout
```
./tail-queue.py
```
