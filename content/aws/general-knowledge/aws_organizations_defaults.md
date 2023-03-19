---
author_name: Nick Frichette & Scott
title: AWS Organizations Defaults & Pivoting
description: AWS Organizations is a common service to run into in AWS environments. It's default behavior can make it a target for attackers, and it offers numerous routes to pivot beyond the default behavior.
---

Almost all mid-to-large sized AWS environments make use of [multi-account](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html) architecture. Using multiple AWS accounts offers a number of [benefits](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/benefits-of-using-multiple-aws-accounts.html) and is considered a best practice. To help organize and manage those accounts, AWS offers a service called [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html).

Due to the ubiquity of AWS Organizations, it is important for Penetration Testers and Red Teamers to familiarize themselves with its default configuration. 

When an account creates an organization it becomes the management account of that organization. Each organization has one management account, and this account effectively "owns" the organization.

## Creating Member Accounts: Default OrganizationAccountAccessRole

When an account is created through AWS Organizations, it is considered a member of the organization (hence, member account). As a part of this account creation process, AWS Organizations will create a role in the member account called `OrganizationAccountAccessRole`. This role is created in [each member account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access.html).

By default, the `OrganizationAccountAccessRole` has the `AdministratorAccess` policy attached to it, giving the role complete control over the member account. In addition, the default trust policy on the role is as shown below where `000000000000` is the account ID of the management account.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::000000000000:root"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

These things combined mean that, should an attacker compromise the management account, the default behavior of AWS Organizations provides a path to compromise every account in the organization as an administrator **assuming that the member account was created through AWS organizations (as opposed to invited)**. **For offensive security professionals, identifying paths into the management account can be an incredibly fruitful exercise, and may result in an entire organization compromise.**

For defensive security teams, it would be a good idea to ensure no infrastructure is deployed into the management account to reduce attack surface. Additionally, carefully controlling who has access to it and monitoring that access would also help to reduce risk.

## Inviting a Pre-Existing AWS Account: Trusted Access, Delegated Administration, IAM Access Analyzer, IAM Identity Center

Scott ([@WebbinRoot](https://twitter.com/WebbinRoot)) at [NetSPI](https://www.netspi.com/) has performed research on how to pivot within AWS accounts if the OrganizationAccountAccessRole is not present as listed above. He covers: 
- AWS Organizations basics
- the OrganizationAccountAccessRole role covered above
- trusted access & delegated administration fundamentals 
- Leveraging IAM Access Analyzer to indirectly access member accounts
- Leveraging IAM Identity Center to directly sign into member accounts as admin
- A new security feature added to AWS Orgs in late 2022. 

His resarch is encapsulated in the following two blog articles:
- https://www.netspi.com/blog/technical/cloud-penetration-testing/pivoting-clouds-aws-organizations-part-1/
- https://www.netspi.com/blog/technical/cloud-penetration-testing/pivoting-clouds-aws-organizations-part-2/

## Pacu Support

[@WebbinRoot](https://twitter.com/WebbinRoot) added AWS Organizations support to [Pacu](https://github.com/RhinoSecurityLabs/pacu) and created an enumeration module for AWS Organizations specifically. See the following pulls that have been merged into the official Pacu repository:
- https://github.com/RhinoSecurityLabs/pacu/pull/326
- https://github.com/RhinoSecurityLabs/pacu/pull/335

```
# Run Module
Pacu (Session: Keys) > run organizations__enum

# See Data Collected/Enumerated
Pacu (Session: Keys) > data organizations
```
