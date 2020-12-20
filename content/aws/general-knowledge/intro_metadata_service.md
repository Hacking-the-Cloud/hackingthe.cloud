---
author: Nick Frichette
title: Introduction to the Metadata Service
description: An Introduction to the Metadata Service and how we can use it.
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/master/content
---
Every EC2 instance has access to something called the instance metadata service (IMDS). This contains (surprise) metadata about that specific EC2 instance.

### How to Access the Metadata Service

The metadata service can be accessed at `http://169.254.169.254/latest/meta-data/` from the EC2 instance.

### IMDSv2

Version two of the metadata service has added protections against SSRF and requires the user to create and use a token. You can access it via the following.

```
user@host:~$ TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` \
&& curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/
```

### What does the Metadata Service Contain

The following information was pulled from [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-categories.html).

| Endpoint | Description |
| ----------------- | ----------- |
| ami-id            | The AMI ID used to launch the instance. |
| ami-launch-index  | If you started more than one instance at the same time, this value indicates the order in which the instance was launched. The value of the first instance launched is 0. |
| ami-manifest-path | The path to the AMI manifest file in Amazon S3. If you used an Amazon EBS-backed AMI to launch the instance, the returned result is unknown. |
| hostname          | The private IPv4 DNS hostname of the instance. In cases where multiple network interfaces are present, this refers to the eth0 device (the device for which the device number is 0). |
| iam/info          | If there is an IAM role associated with the instance, contains information about the last time the instance profile was updated, including the instance's LastUpdated date, InstanceProfileArn, and InstanceProfileId. Otherwise, not present. |
| iam/security-credentials/*role-name* | If there is an IAM role associated with the instance, role-name is the name of the role, and role-name contains the temporary security credentials associated with the role. Otherwise, not present. |
| identity-credentials/ec2/info | [Internal use only] Information about the credentials in identity-credentials/ec2/security-credentials/ec2-instance. These credentials are used by AWS features such as EC2 Instance Connect, and do not have any additional AWS API permissions or privileges beyond identifying the instance. |
| instance-id | The ID of this instance. |
| local-hostname | The private IPv4 DNS hostname of the instance. In cases where multiple network interfaces are present, this refers to the eth0 device (the device for which the device number is 0). |
| local-ipv4 | The private IPv4 address of the instance. In cases where multiple network interfaces are present, this refers to the eth0 device (the device for which the device number is 0). |
| public-hostname | The instance's public DNS. This category is only returned if the enableDnsHostnames attribute is set to true. |
| public-ipv4 | The public IPv4 address. If an Elastic IP address is associated with the instance, the value returned is the Elastic IP address. |
| public-keys/0/openssh-key |  	Public key. Only available if supplied at instance launch time. |
| security-groups | The names of the security groups applied to the instance. |
