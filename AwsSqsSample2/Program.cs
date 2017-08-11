/*******************************************************************************
* Copyright 2009-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
* 
* Licensed under the Apache License, Version 2.0 (the "License"). You may
* not use this file except in compliance with the License. A copy of the
* License is located at
* 
* http://aws.amazon.com/apache2.0/
* 
* or in the "license" file accompanying this file. This file is
* distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
* KIND, either express or implied. See the License for the specific
* language governing permissions and limitations under the License.
*******************************************************************************/

using System;
using Amazon.SQS;
using Amazon.SQS.Model;

namespace AwsSqsSample2
{
    class Program
    {
        public static void Main(string[] args)
        {
            var sqs = new AmazonSQSClient();

            try
            {
                Console.WriteLine("===========================================");
                Console.WriteLine("Consuming Messages from Amazon SQS");
                Console.WriteLine("===========================================\n");

                // Our test Queue ... should read from Config because this will be different endpoint in Production
                string appQueueUrl = "https://sqs.us-west-2.amazonaws.com/320984030376/mmu-applications-dev";

                //Confirming the queue exists and list all queues
                // TODO Can delete this
                Console.WriteLine("Printing list of Amazon SQS queues.\n");
                var listQueuesRequest = new ListQueuesRequest();
                var listQueuesResponse = sqs.ListQueues(listQueuesRequest);

                if (listQueuesResponse.QueueUrls != null)
                {
                    foreach (String queueUrl in listQueuesResponse.QueueUrls)
                    {
                        Console.WriteLine("  QueueUrl: {0}", queueUrl);
                    }
                }
                Console.WriteLine();


                // Recieve a message
                // TODO: Maybe put this in a loop to clear the queue ... ?
                var receiveMessageRequest = new ReceiveMessageRequest { QueueUrl = appQueueUrl };
                var receiveMessageResponse = sqs.ReceiveMessage(receiveMessageRequest);
                if (receiveMessageResponse.Messages != null)
                {
                    Console.WriteLine("Printing received message.\n");
                    foreach (var message in receiveMessageResponse.Messages)
                    {
                        // Echo pieces of the message
                        Console.WriteLine("  Message");
                        if (!string.IsNullOrEmpty(message.MessageId))
                        {
                            Console.WriteLine("    MessageId: {0}", message.MessageId);
                        }
                        if (!string.IsNullOrEmpty(message.ReceiptHandle))
                        {
                            Console.WriteLine("    ReceiptHandle: {0}", message.ReceiptHandle);
                        }
                        if (!string.IsNullOrEmpty(message.MD5OfBody))
                        {
                            Console.WriteLine("    MD5OfBody: {0}", message.MD5OfBody);
                        }

                        // Here's the interesting part
                        if (!string.IsNullOrEmpty(message.Body))
                        {
                            // Deserialize the JSON String using Newtonsoft
                            Object application = Newtonsoft.Json.JsonConvert.DeserializeObject(message.Body);
                            Console.WriteLine(" Message Payload :\n" + application.ToString());

                            //TODO: Do stuff with Application JSON here
                            // 1. Insert into database

                            // 2. Download file artifacts from S3 and store locally

                            // 3. Save file links so advisors can access

                            // 4. Send email to notify that there is a new application?
                        }

                        // TODO: Can delete
                        foreach (string attributeKey in message.Attributes.Keys)
                        {
                            Console.WriteLine("  Attribute");
                            Console.WriteLine("    Name: {0}", attributeKey);
                            var value = message.Attributes[attributeKey];
                            Console.WriteLine("    Value: {0}", string.IsNullOrEmpty(value) ? "(no value)" : value);
                        }
                    }


                    // Deleting a message
                    // TODO: Once all message processing is completed, then we can delete the message.
                    // For testing purposes, we are not deleting messages yet (to keep the queue full of messages to test against)
                    /*
                    Console.WriteLine("Deleting the message.\n");
                    var messageRecieptHandle = receiveMessageResponse.Messages[0].ReceiptHandle;
                    var deleteRequest = new DeleteMessageRequest { QueueUrl = appQueueUrl, ReceiptHandle = messageRecieptHandle };
                    sqs.DeleteMessage(deleteRequest);
                    */
                }

            }
            catch (AmazonSQSException ex)
            {
                Console.WriteLine("Caught Exception: " + ex.Message);
                Console.WriteLine("Response Status Code: " + ex.StatusCode);
                Console.WriteLine("Error Code: " + ex.ErrorCode);
                Console.WriteLine("Error Type: " + ex.ErrorType);
                Console.WriteLine("Request ID: " + ex.RequestId);
            }

            Console.WriteLine("Press Enter to continue...");
            Console.Read();
        }
    }
}