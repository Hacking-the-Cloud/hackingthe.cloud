---
author: Nick Frichette
title: Introduction to User Data
description: An introduction to EC2 User Data and how to access it.
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/main/content
---
[Instance user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-add-user-data.html) is used to run commands when an EC2 instance is first started or after it is rebooted (with some [configuration](https://aws.amazon.com/premiumsupport/knowledge-center/execute-user-data-ec2/)). Because this script is typically used to install software and configure the instance, this can be an excellent source of information for us as attackers. After gaining access to an EC2 instance you should immediately grab the user data script to gain information on the environment.

### How to Access EC2 User Data

User data can be accessed at `http://169.254.169.254/latest/user-data/` from the EC2 instance.

#### IMDSv2

Version two of the metadata service has added protections against SSRF and requires the user to create and use a token. You can access it via the following.

```
user@host:~$ TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
user@host:~$ curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/user-data/
```

### API
Another option to gather user data is via the API. If you escalate privileges in an account, or simply compromise a user/role with sufficient permissions, you can query the AWS API to view the user data of specific EC2 instances. This requires you to know the instance-id of the target EC2 instance. To query the user data we will use the [describe-instance-attribute](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instance-attribute.html) action. The result will be base64 encoded.

```
user@host:~$ aws ec2 describe-instance-attribute --instance-id i-abc123... --attribute userData
```