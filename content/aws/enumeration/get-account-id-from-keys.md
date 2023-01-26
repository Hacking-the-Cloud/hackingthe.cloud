---
author_name: Nick Frichette
title: Get Account ID from AWS Access Keys
description: During an assessment you may find AWS IAM credentials but not know what account they are associated with. Use this to get the account ID.
hide:
  - toc
---

# Get Account ID from AWS Access Keys

While performing an assessment in AWS it is not uncommon to come across access keys and not know what account they are associated with. If your scope is defined by the AWS account ID, this may pose a problem as you'd likely not want to use them if they are out of scope.

To solve this problem you can use [sts:GetAccessKeyInfo](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetAccessKeyInfo.html) to return the account ID of the credentials. This action will only be logged to the account calling the action (which should be your account, not the target's).

```
user@host:~$ aws sts get-access-key-info --access-key-id=ASIA1234567890123456
{
    "Account": "123456789012"
}
```