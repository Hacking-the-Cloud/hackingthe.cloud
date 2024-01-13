---
author_name: Nick Frichette
title: Get Account ID from AWS Access Keys
description: Techniques to enumerate the account ID associated with an AWS access key.
---

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    - [AWS Access Key ID Formats](https://awsteele.com/blog/2020/09/26/aws-access-key-format.html) by [Aidan Steele](https://twitter.com/__steele)
    - [A short note on AWS KEY ID](https://medium.com/@TalBeerySec/a-short-note-on-aws-key-id-f88cc4317489) by [Tal Be'ery](https://twitter.com/TalBeerySec)
</div>

While performing an assessment in AWS environments it is not uncommon to come across access keys and not know what account they are associated with. If your scope is defined by the AWS account ID, this may pose a problem as you'd likely not want to use them if they are out of scope.

To solve this problem, there are multiple ways to determine the account ID of IAM credentials.

## sts:GetAccessKeyInfo

Likely the most straightforward way is to use [sts:GetAccessKeyInfo](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetAccessKeyInfo.html) to return the account ID of the credentials. This action will only be logged to the account calling the action (which should be your account, not the target's).

```
user@host:~$ aws sts get-access-key-info --access-key-id=ASIA1234567890123456
{
    "Account": "123456789012"
}
```

## Decode the access key

As originally discovered by [Aidan Steele](https://awsteele.com/blog/2020/09/26/aws-access-key-format.html), and later improved upon by [Tal Be'ery](https://medium.com/@TalBeerySec/a-short-note-on-aws-key-id-f88cc4317489), the account ID is actually encoded into the access key itself. 

By decoding the access key using [Base32](https://en.wikipedia.org/wiki/Base32) and doing a little bit shifting, we can get the account ID. Tal wrote the handy Python script below to do this:

```python
import base64
import binascii

def AWSAccount_from_AWSKeyID(AWSKeyID):
    
    trimmed_AWSKeyID = AWSKeyID[4:] #remove KeyID prefix
    x = base64.b32decode(trimmed_AWSKeyID) #base32 decode
    y = x[0:6]
    
    z = int.from_bytes(y, byteorder='big', signed=False)
    mask = int.from_bytes(binascii.unhexlify(b'7fffffffff80'), byteorder='big', signed=False)
    
    e = (z & mask)>>7
    return (e)


print ("account id:" + "{:012d}".format(AWSAccount_from_AWSKeyID("ASIAQNZGKIQY56JQ7WML")))
```