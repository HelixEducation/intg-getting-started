#
# Helix Education. July 2017.
#
#  PowerShell consumer for Amazon Simple Queue Service (SQS).
#  See README.md for prerequisites and usage instructions.
#

## Amazon SQS Configuration
$msgCount = 10
$poll = $true
$region = 'us-west-2'
$profile = '<profile>'
$queueUrl = 'https://sqs.us-west-2.amazonaws.com/320984030376/mmu-applications-dev'

## Message Delivery Configuration
$doEmail = $true
$doFile = $true

## Output File Configuration
$fileDir = 'C:\' # must include the ending \
$fileName = 'application.csv'

## SMTP Configuration
$email = 'XXXXX@gmail.com' #sender of the application email
$to = 'XXXXX@helixeducation.com' #recipient of the application email
$subject = 'New Student Application Received'
$smtpServer = 'smtp.gmail.com'
$smtpPort = '587'
$password = 'XXXXX'

# based on polling settings above will either process the queue once, or continue polling
Do {
 # Poll Amazon SQS queue for up-to the above configured number of messages
 $appMsgs = Receive-SQSMessage -QueueUrl $queueUrl -Region $region -ProfileName $profile -MessageCount $msgCount

 # process each application message individually
 foreach ($msg In $appMsgs) {
    # grab the receipt handle for use in delete call after processing
    $receiptHandle = $msg.ReceiptHandle

    # the application JSON is contained in AWSMessage.Body.Message
    $body = $msg.Body
    $jsonBody = ConvertFrom-JSON -InputObject $body
    $jsonMsg = ConvertFrom-JSON -InputObject $jsonBody.Message

    # send the application messge to an Admissions recipient via email
    if($doEmail) {
      # spin-up email client
      $smtp = New-Object System.Net.Mail.SmtpClient($SMTPServer,$SMTPPort);
      $smtp.EnableSSL = $true # set to $false if using Port 25 without encryption
      $smtp.Credentials = New-Object System.Net.NetworkCredential($email,$password);
      # send email
      $emailMsg = ConvertTo-JSON -InputObject $jsonMsg
      $smtp.Send($email,$to,$subject,$emailMsg)
    }

    # write the message out to file
    if($doFile) {
      # write CSV header
      $header = "helixStudentId,firstname"
      Out-File -FilePath "$fileDir$fileName" -InputObject $header
      # write the application record
      $record = $jsonMsg.helixStudentId + "," + $jsonMsg.personalInfo.firstname
      Out-File -FilePath "$fileDir$fileName" -Append -InputObject $record
    }

    # after processing delete the message off the queue
    $del = Remove-SQSMessage -QueueUrl $queueUrl -Region $region -ProfileName $profile -ReceiptHandle $receiptHandle -Force
 }
}
While ($poll)
