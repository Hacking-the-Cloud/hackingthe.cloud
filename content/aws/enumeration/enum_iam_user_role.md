---
author_name: Nick Frichette
title: Unauthenticated Enumeration of IAM Users and Roles
description: Leverage cross account behaviors to enumerate IAM users and roles in a different AWS account without authentication.
hide:
  - toc
---

# Unauthenticated Enumeration of IAM Users and Roles

Original Research: [Daniel Grzelak](https://twitter.com/dagrz) - [Remastered Talk by Scott Piper](https://www.youtube.com/watch?v=8ZXRw4Ry3mQ)  
Additional Reading: [Rhino Security](https://rhinosecuritylabs.com/aws/aws-role-enumeration-iam-p2/)  
Link to Quiet Riot: [Github](https://github.com/righteousgambitresearch/quiet-riot)  
Link to Tool: [GitHub](https://github.com/Frichetten/enumate_iam_using_bucket_policy)  
Link to Pacu Module: [GitHub](https://github.com/RhinoSecurityLabs/pacu/tree/master/pacu/modules/iam__enum_roles)  

You can enumerate Account IDs, root account e-mail addresses, IAM roles, IAM users, and a partial account footprint by abusing [Resource-Based Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_resource-based).

There are a few ways to do this, for example, Pacu's module will attempt to change the AssumeRole policy of a role in <ins>your</ins> account and specify a role in another account. [Quiet Riot](https://github.com/righteousgambitresearch/quiet-riot) offers a scalable method for enumerating each of these items with configurable wordlists per item type.

Another way would be to use S3 Bucket Policies. Take the following example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Example permissions",
            "Effect": "Deny",
            "Principal": {
                "AWS": "arn:aws:iam::123456789123:role/role_name"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::*bucket you own*"
        }
    ]
}
```

You would apply this policy to a bucket <ins>you</ins> own. By specifying a principal in the target account (123456789123), you can determine if that principals exists. If setting the bucket policy succeeds you know the role exists. If it fails you know the role does not.

!!! Warning
    Doing either of these techniques will generate a lot of CloudTrail events, specifically UpdateAssumeRolePolicy or PutBucketPolicy in your account. If your intention is to be stealthy it is not advised (or required) to use a target's credentials. Instead you should use your own account (the CloudTrail events will be generated there).

!!! Note
    While this works for both IAM users and roles, this will also work with [service-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html). This will allow you to enumerate various services the account uses, such as GuardDuty or Organizations.

To automate this process you can use the [Pacu Module](https://github.com/RhinoSecurityLabs/pacu/tree/master/pacu/modules/iam__enum_roles) or [this](https://github.com/Frichetten/enumate_iam_using_bucket_policy) which will attempt to brute force it for you.

```
usage: main.py [-h] --id ID --my_bucket MY_BUCKET [--wordlist WORDLIST] (--role | --user)

Enumerate IAM/Users of an AWS account. You must provide your OWN AWS account and bucket

optional arguments:
  -h, --help            show this help message and exit
  --id ID               The account id of the target account
  --my_bucket MY_BUCKET
                        The bucket used for testing (belongs to you)
  --wordlist WORDLIST   Wordlist containers user/role names
  --role                Search for a IAM Role
  --user                Search for a IAM User
```
