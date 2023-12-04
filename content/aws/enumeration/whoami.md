---
author_name: Nick Frichette
title: Whoami - Get Principal Name From Keys
description: During an assessment you may find AWS IAM credentials. Use these tactics to identify the principal of the keys.
---

After finding or obtaining IAM credentials during an assessment you will need to identify what they are used for, or if they are valid. The most common method for doing so would be the [get-caller-identity](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/get-caller-identity.html) API call. This is beneficial for several reasons, particularly because it requires no special permissions to execute.

Unfortunately, although it is [unlikely](https://twitter.com/SpenGietz/status/1283846678194221057), there is the possibility that this API call may be monitored, especially for sensitive accounts. Additionally, if our goal is to remain as stealthy as possible, we might prefer not to use this method. As a result we need alternatives. Fortunately, many AWS services will disclose the calling role along with the account ID when an error is generated. It should be noted that the principal must lack IAM permissions for this call in order for the error to return the relevant information. 

Not all API calls exhibit this behavior. For example, failed EC2 API calls will return a message similar to the following:

```
An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to perform this operation.
```

## sqs:ListQueues

[sqs:ListQueues](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sqs/list-queues.html) is a quick API call which will return the calling identity's name and account ID without logging to CloudTrail. Note that the `ListQueues` action does not appear in the [documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-logging-using-cloudtrail.html) for SQS's compatibility with CloudTrail.

```
user@host:~$ aws sqs list-queues

An error occurred (AccessDenied) when calling the ListQueues operation: User: arn:aws:sts::123456789012:assumed-role/no_perms/no_perms is not authorized to perform: sqs:listqueues on resource: arn:aws:sqs:us-east-1:123456789012: because no identity-based policy allows the sqs:listqueues action
```
