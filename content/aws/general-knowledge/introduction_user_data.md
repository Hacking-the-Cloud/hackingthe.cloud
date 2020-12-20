---
author: Nick Frichette
title: Introduction to User Data
description: An Introduction to User Data and how it is used.
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/master/content
---
[Instance user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-add-user-data.html) is used to run commands when an EC2 instance is started or rebooted. This can be an excellent source of information for us as attackers. It typically takes the form of a shell script that can be accessed from the EC2 instance.

### How to Access the User Data

User data can be accessed at `http://169.254.169.254/latest/user-data/` from the EC2 instance.

### IMDSv2

Version two of the user data service has added protections against SSRF and requires the user to create and use a token. You can access it via the following.

```
user@host:~$ TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
&& curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/user-data/
```