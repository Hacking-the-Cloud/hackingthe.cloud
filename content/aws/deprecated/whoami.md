---
author_name: Nick Frichette
title: Whoami - Get Principal Name From Keys
description: During an assessment you may find AWS IAM credentials. Use these tactics to identify the principal of the keys.
hide:
  - toc
---

Original Research: [Spencer Gietzen](https://twitter.com/SpenGietz/status/1283843401008336896)

!!! Warning
    As of August 15, 2020 these calls are now tracked in CloudTrail ([tweet](https://twitter.com/tacertain/status/1294726441850900480)). This page is maintained for historical and inspiration purposes.

## sdb list-domains
As found by [Spencer Gietzen](https://twitter.com/SpenGietz/status/1283843401008336896), the API call for [sdb list-domains](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sdb/list-domains.html) will return very similar information to get-caller-identity.

```
user@host:$ aws sdb list-domains --region us-east-1

An error occurred (AuthorizationFailure) when calling the ListDomains operation: User (arn:aws:sts::123456789012:assumed-role/example_role/i-00000000000000000) does not have permission to perform (sdb:ListDomains) on resource (arn:aws:sdb:us-east-1:123456789012:domain/). Contact account owner.
```