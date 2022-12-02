---
author_name: Nick Frichette
title: Enumerate AWS Account ID from a Public S3 Bucket
description: Knowing only the name of a public S3 bucket, you can ascertain the account ID it resides in.
---

Discovered by [Ben Bridts](https://twitter.com/benbridts)  
Original Research: [link](https://www.cloudar.be/awsblog/finding-the-accountid-of-any-public-s3-bucket/)  
Link to Tool: [s3-account-search](https://github.com/WeAreCloudar/s3-account-search)

!!! Note
    The documentation and GitHub repository refer to this tool as `s3-account-search`, however when it is installed using [pip](https://pip.pypa.io/en/stable/), it is named `s3-account-finder`. Because of this, all the examples below will use the `s3-account-finder` name.

By leveraging the s3:ResourceAccount policy condition, we can identify the AWS account ID associated with a public S3 bucket. This is possible because it supports wildcards (*). With this, we can sequentially enumerate the account ID.

To test this, you can use [Grayhat Warfare's](https://buckets.grayhatwarfare.com/random/buckets) list of public S3 buckets.

You will need a role with `s3:getObject` and `s3:ListBucket` permissions, and you can specify the target bucket as the resource for your policy. Alternatively you can set a resource of '*' to quickly test multiple buckets.

## Installation

The tool can be installed with the following command:

```
python3 -m pip install s3-account-search
```

## Setup

To use the tool, there is some setup on your end. You will need your own AWS account with a role you can assume with the `s3:GetObject` or `s3:ListBucket` permissions. s3-account-finder will assume this role so make sure the credentials you're using can do this.

## Usage

```
s3-account-finder arn:aws:iam::123456789123:role/s3-searcher <bucket name>
Starting search (this can take a while)
found: 1
found: 12
*** snip ***
found: 123456789123
```

!!! Warning  "Operational Security Tip"
    The majority of this activity would only be logged to the calling account (the account you are running the tool with), however S3 data events and server access logging can be used to see the API activity. That being said, there is no immediate way to counter or prevent you from doing this. Additionally these requests could be spaced out over an extended period of time, further making it difficult to identify.

!!! Tip
    Pair this with [Unauthenticated Enumeration of IAM Users and Roles](/aws/enumeration/enum_iam_user_role/)!