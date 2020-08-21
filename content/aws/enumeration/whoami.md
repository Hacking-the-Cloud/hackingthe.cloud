---
author: Nick Frichette
title: Whoami - Get Principal Name From Keys
description: During an assessment you may find AWS IAM credentials. Use these tactics to identify the principal of the keys.
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/master/content
---
After finding or stealing IAM credentials during an assessment you will need to identify what they are used for, or if they are valid. The most common method for doing so would be to call the [get-caller-identity](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/get-caller-identity.html) API call. This is beneficial for a few reasons, in particular that it requires no special permissions to call.

Unfortunately, because it is so simple many defenders are monitoring for these API calls. As a result we need alternatives. The good news for us is that a lot of AWS services will disclose the calling role along with the account ID as a result of an error. The following is certainly not a comprehensive list, and note that the principal needs to **NOT** have IAM permissions to make this call to return the information as an error.

Not all API calls exhibit this behavior. Failed EC2 API calls, for example, will return a variant of the following.

```
An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to perform this operation.
```

### sdb list-domains
As found by [Spencer Gietzen](https://twitter.com/SpenGietz/status/1283843401008336896), the API call for [sdb list-domains](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sdb/list-domains.html) will return verify similar information to get-caller-identity.

```
user@host:$ aws sdb list-domains --region us-east-1

An error occurred (AuthorizationFailure) when calling the ListDomains operation: User (arn:aws:sts::123456789012:assumed-role/example_role/i-00000000000000000) does not have permission to perform (sdb:ListDomains) on resource (arn:aws:sdb:us-east-1:123456789012:domain/). Contact account owner.
```

{{< notice warning "Note" >}}
According to Andrew Certain as of August 15, 2020 these calls are now tracked in CloudTrail ([tweet](https://twitter.com/tacertain/status/1294726441850900480)).
{{< /notice >}}

### route53 get-account-limit
[route53 get-account-limit](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/route53/get-account-limit.html) will produce a similar result.

### logs associate-kms-key
[logs associate-kms-key](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/logs/associate-kms-key.html) will produce a similar result.