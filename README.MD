Sample project for getting up and running quicker with Helix Education Application Integration

# Overview
Helix Education leverages a 2-way integration with partners through Amazon SQS for the purpose
of exchanging Application information and Admissions Decisions. By leveraging AWS SQS, we can take
advantage of the high availability of AWS infrastructure, as well as the 
[AWS SDK](https://aws.amazon.com/tools/) and numerous code samples available online.

## Integration
This integration currently includes the transmission of Completed Applications from:
` Helix => AWS SQS => Partner`
and Admissions Decisions from:
`Partner => AWS SQS => Helix`
