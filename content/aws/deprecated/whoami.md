---
author_name: Nick Frichette
title: "[Deprecated] Whoami - Get Principal Name From Keys"
description: During an assessment you may find AWS IAM credentials. Use these tactics to identify the principal of the keys.
---

## sns publish

!!! Warning
    As of Q4 2023 these calls can optionally be tracked in CloudTrail by enabling [dataplane logging](https://docs.aws.amazon.com/sns/latest/dg/sns-logging-using-cloudtrail.html#data-plane-events-cloudtrail). While this will not be enabled for the overwhelming majority of AWS accounts, there is no reason to risk it when there are other methods available.

[sns:Publish](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sns/publish.html) would return the ARN of the calling user/role **without logging to CloudTrail**. To use this method, you had to provide a valid AWS account ID in the API call. This could be your own account id, or the account id of anyone else.

```
user@host:~$ aws sns publish --topic-arn arn:aws:sns:us-east-1:*account id*:aaa --message aaa
 
An error occurred (AuthorizationError) when calling the Publish operation: User: arn:aws:iam::123456789123:user/no-perm is not authorized to perform: SNS:Publish on resource: arn:aws:sns:us-east-1:*account id*:aaa because no resource-based policy allows the SNS:Publish action
```

## sdb list-domains

!!! Warning
    As of August 15, 2020 these calls are now tracked in CloudTrail ([tweet](https://twitter.com/tacertain/status/1294726441850900480)). This page is maintained for historical and inspiration purposes.

As found by [Spencer Gietzen](https://twitter.com/SpenGietz/status/1283843401008336896), the API call for [sdb list-domains](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sdb/list-domains.html) will return very similar information to get-caller-identity.

```
user@host:$ aws sdb list-domains --region us-east-1

An error occurred (AuthorizationFailure) when calling the ListDomains operation: User (arn:aws:sts::123456789012:assumed-role/example_role/i-00000000000000000) does not have permission to perform (sdb:ListDomains) on resource (arn:aws:sdb:us-east-1:123456789012:domain/). Contact account owner.
```