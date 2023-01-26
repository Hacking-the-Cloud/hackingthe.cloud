---
author_name: Phil Massyn
title: Enumerate AWS Account ID from an EC2 Instance
description: With access to an ec2 instance, you will be able to identify the AWS account it runs in.
---

With shell or command line access to an EC2 instance, you will be able to determine some key information about the AWS account.

## get-caller-identity

By using [get-caller-identity](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html), the EC2 instance may have an EC2 instance profile setup.

```
user@host:$ aws sts get-caller-identity
{
   "Account": "000000000000",
   "UserId": "AROAJIWIJQ5KCHMJX4EWI:i-00000000000000000",
   "Arn": "arn:aws:sts::000000000000:assumed-role/AmazonLightsailInstanceRole/i-00000000000000000"
}
```

## Metadata

By using the [metadata](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html) service, you will be able to retrieve additional information about the account, and more specifically for the EC2 instance being used.

```
TOKEN=`curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
curl -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/dynamic/instance-identity/document
```
The output will reveal additional information.
```
{
   "accountId" : "000000000000",
   "architecture" : "x86_64",
   "availabilityZone" : "ap-southeast-2a",
   "billingProducts" : null,
   "devpayProductCodes" : null,
   "marketplaceProductCodes" : null,
   "imageId" : "ami-042c4533fa25c105a",
   "instanceId" : "i-00000000000000000",
   "instanceType" : "t2.nano",
   "kernelId" : null,
   "pendingTime" : "2022-02-27T22:34:30Z",
   "privateIp" : "172.26.6.225",
   "ramdiskId" : null,
   "region" : "ap-southeast-2",
   "version" : "2017-09-30"
}
```
