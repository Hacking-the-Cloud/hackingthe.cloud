---
author_name: biggie_linz (@biggie_linz)
title: Enumerate services via AWS Backup
description: Enumerate AWS services via AWS Backup
---
<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    [Enumeration via the AWS Backup service](https://acacialabs.net/enumeration-via-the-aws-backup-service/) by [biggie_linz](https://x.com/biggie_linz).
</div>

# Enumeration of services via AWS Backup
## Overview

An attacker with permissions of at least `backup:List*` or `backup:Describe*` permissions can enumerate the AWS Backup service to potentially find critical resources in an AWS account without needing to use traditional, well-monitored and heavily scrutinised reconnaissance commands for individual services.

The AWS Backup service supports the following resource types:

- Aurora
- AWS CloudFormation
- Amazon DocumentDB
- DynamoDB
- DynamoDB with AWS Backup advanced features
- Amazon EBS
- Amazon EC2
- Amazon EFS
- Amazon Redshift
- Redshift Serverless
- Amazon RDS

We can use the AWS CLI to enumerate the AWS Backup service to learn more about these services within a target account, should the target be utilising the AWS Backup service to perform backups of these services.

## Why do we care?

The AWS Backup service can reveal interesting information to attackers such as:

- **The resources that the target account really cares about (and those they don't really care about but backup anyway)** - the Backup service is not enabled by default, and as such, an administrator must specifically enable it and configure it. This means that the resources that are backed up are likely of importance and warrant further review.
- **Reveals strategies for tagging and resource naming** - e.g. is the target using tags like `Enviromnent=production` vs `Environment=Prod` or using something totally different like `Tier=Critical`
- **Mapping of resources** - when we query the Backup service we can see the breadth of services that the organisation is using.
- ***Timing information** - we can see when backups do run, and how long they are retained for.
- **We don't need to rely on calling heavily monitored enumeration commands for individual services.***

## Attack

### Enumerating backed up resources

**Viewing all resources that have been backed up**

`aws backup list-protected-resources`

**This one is probably the most interesting in this article** - this command returns an array of resources that have been successfully backed up by Backup, including the time the resource was saved, an Amazon Resource Name (ARN) of the resource, and a resource type.

```
{
    "Results": [
        {
            "ResourceArn": "arn:aws:rds:ap-southeast-2:[REDACTED]:db:database-1",
            "ResourceType": "RDS",
            "LastBackupTime": "2025-05-04T21:43:01.687000-07:00",
            "ResourceName": "database-1",
            "LastBackupVaultArn": "arn:aws:backup:ap-southeast-2:[REDACTED]:backup-vault:Default",
            "LastRecoveryPointArn": "arn:aws:rds:ap-southeast-2:[REDACTED]:snapshot:awsbackup:[REDACTED]"
        }
    ]
}
```

Note that this will only show resources that __have been backed up in the past, and not resources that are yet to be backed up__.

### Enumerating resources within Backup Plans

**Enumerating Backup Plans**

`aws backup list-backup-plans`

As the operation implies, this will list the Backup Plans for the account.

In the following snippet we can see some interesting details such as:

- `BackupPlanId` - more on this later,
- `BackupPlanName` - this may let on naming strategies used by the target.

```
{
    "BackupPlansList": [
        {
            "BackupPlanArn": "arn:aws:backup:ap-southeast-2:[REDACTED]:backup-plan:31[REDACTED]da",
            "BackupPlanId": "31[REDACTED]da",
            "CreationDate": "2025-05-04T21:16:24.813000-07:00",
            "VersionId": "OT[REDACTED]E4",
            "BackupPlanName": "prod-backups",
            "CreatorRequestId": "7e[REDACTED]99"
        }
    ]
}
```

**Enumerating the Backup Plan's details**

`aws backup get-backup-plan --backup-plan-id <BACKUP-PLAN-ID>`

where:

- `BACKUP-PLAN-ID` is the `BackupPlanId` from the previous command.

This command provides some more information on the specified Backup Plan.

Specifically, it provides insights in to:

- Timings - `ScheduleExpression`
- Retention policies - `Lifecycle`
- Naming schemes - `RuleName`, `TargetBackupVaultName`, `RecoveryPointTags`

```
aws backup get-backup-plan --backup-plan-id 31[REDACTED]da
{
    "BackupPlan": {
        "BackupPlanName": "prod-backups",
        "Rules": [
            {
                "RuleName": "DailyBackups",
                "TargetBackupVaultName": "Default",
                "ScheduleExpression": "cron(0 5 ? * * *)",
                "StartWindowMinutes": 480,
                "CompletionWindowMinutes": 10080,
                "Lifecycle": {
                    "DeleteAfterDays": 3
                },
                "RecoveryPointTags": {},
                "RuleId": "4c[REDACTED]43",
                "CopyActions": [],
                "ScheduleExpressionTimezone": "America/Los_Angeles"
            }
        ]
    },
    "BackupPlanId": "31[REDACTED]da",
    "BackupPlanArn": "arn:aws:backup:ap-southeast-2:[REDACTED]:backup-plan:31[REDACTED]da",
    "VersionId": "OT[REDACTED]E4",
    "CreatorRequestId": "7e[REDACTED]99",
    "CreationDate": "2025-05-04T21:16:24.813000-07:00"
}
```

**Enumerating resources targeted for backups in a given Backup Plan**

First, we must find the `SelectionId` of our Backup Plan:

`aws backup list-backup-selections --backup-plan-id 31[REDACTED]da`

```
{
    "BackupSelectionsList": [
        {
            "SelectionId": "e9[REDACTED]fc",
            "SelectionName": "rds-prod",
            "BackupPlanId": "31[REDACTED]da",
            "CreationDate": "2025-05-04T21:17:47.318000-07:00",
            "CreatorRequestId": "c0[REDACTED]53",
            "IamRoleArn": "arn:aws:iam::[REDACTED]:role/service-role/AWSBackupDefaultServiceRole"
        }
    ]
}
```

We can then use the `SelectionId` to find the resources that will be targeted as a part of this Backup Plan (note: this can be tag-based and/or ARNs). Note that even if the backup job has not yet run the resources will still be shown:

```
{
    "BackupSelection": {
        "SelectionName": "rds-prod",
        "IamRoleArn": "arn:aws:iam::[REDACTED]:role/service-role/AWSBackupDefaultServiceRole",
        "Resources": [
            "arn:aws:rds:ap-southeast-2:[REDACTED]:db:database-1"
        ],
        "ListOfTags": [],
        "NotResources": [],
        "Conditions": {
            "StringEquals": [],
            "StringNotEquals": [],
            "StringLike": [],
            "StringNotLike": []
        }
    },
    "SelectionId": "e9[REDACTED]fc",
    "BackupPlanId": "31[REDACTED]da",
    "CreationDate": "2025-05-04T21:17:47.318000-07:00",
    "CreatorRequestId": "c0[REDACTED]53"
```

In the above snippet we can see the potential existence of a likely production RDS instance, `database-1`, that we previously were not aware of.

## Detection strategy

**Calls to `ListProtectedResources`**

Organisations can flag calls to the `ListProtectedResources` event where it is:

- Invoked by IAM role/user not used for backup,
- Invoked outside backup windows, or
- From a new IP/geolocation.

**Enumeration burst patterns**

Look for bursts of calls to APIs to do with the Backup service, such as:

- `ListBackupVaults`
- `ListBackupPlans`
- `ListBackupSelections`
- `ListProtectedResources`
