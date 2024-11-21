---
author_name: Nick Frichette
title: Prevent Expensive AWS API Actions with SCPs
description: Avoid AWS bill surprises by blocking known-expensive API calls with an SCP.
---

# Prevent Expensive AWS API Actions with SCPs

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="https://gist.github.com/iann0036/b473bbb3097c5f4c656ed3d07b4d2222"> List of expensive / long-term effect AWS IAM actions</a> by <a href="https://x.com/iann0036">Ian McKay</a></p>
    <p><img src="/images/researchers/ian_mckay.jpg" alt="Ian McKay" style="width:44px;height:44px;margin:5px;border-radius:100%;max-width:unset"></img></p>
    </aside>

-   :material-book:{ .lg .middle } __Additional Resources__

    ---

    - [Service Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) (SCPs)
    - [Attaching and detaching service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_attach.html)
</div>

An ever-present danger when using AWS is accidentally making an API call that could cost you thousands of dollars. Speaking from experience, this can be a remarkably stressful time. To mitigate this risk, implementing guardrails on your account is essential. One way to do this is to block API operations which are known to be expensive. Operations like signing up for certain AWS services or creating non-deletable resources can lead to high costs.

## Understanding Service Control Policies

To help prevent billing headaches when learning about AWS security or conducting research we can use a [Service Control Policy](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) (SCP). An SCP is a type of organizational policy which restricts what API calls can be made by member accounts in an [AWS Organization](../../aws/general-knowledge/aws_organizations_defaults.md). Thanks to the work of [Ian McKay](https://x.com/iann0036), and other community members, we have a list of AWS API operations which are prohibitively expensive and should be avoided. 

To implement the policy below, refer to the AWS [documentation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_attach.html) for detailed instructions on attaching and managing SCPs.

!!! Warning
    While this SCP provides a significant safeguard, it is not entirely foolproof. You can still incur high charges if not careful. This policy only blocks known problematic API calls. Always exercise caution when creating or configuring resources in AWS.

## Safeguard SCP

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Statement1",
      "Effect": "Deny",
      "Action": [
        "route53domains:RegisterDomain",
        "route53domains:RenewDomain",
        "route53domains:TransferDomain",
        "ec2:ModifyReservedInstances",
        "ec2:PurchaseHostReservation",
        "ec2:PurchaseReservedInstancesOffering",
        "ec2:PurchaseScheduledInstances",
        "rds:PurchaseReservedDBInstancesOffering",
        "dynamodb:PurchaseReservedCapacityOfferings",
        "s3:PutObjectRetention",
        "s3:PutObjectLegalHold",
        "s3:BypassGovernanceRetention",
        "s3:PutBucketObjectLockConfiguration",
        "elasticache:PurchaseReservedCacheNodesOffering",
        "redshift:PurchaseReservedNodeOffering",
        "savingsplans:CreateSavingsPlan",
        "aws-marketplace:AcceptAgreementApprovalRequest",
        "aws-marketplace:Subscribe",
        "shield:CreateSubscription",
        "acm-pca:CreateCertificateAuthority",
        "es:PurchaseReservedElasticsearchInstanceOffering",
        "outposts:CreateOutpost",
        "snowball:CreateCluster",
        "s3-object-lambda:PutObjectLegalHold",
        "s3-object-lambda:PutObjectRetention",
        "glacier:InitiateVaultLock",
        "glacier:CompleteVaultLock",
        "es:PurchaseReservedInstanceOffering",
        "backup:PutBackupVaultLockConfiguration",
        "bedrock:CreateProvisionedModelThroughput",
        "bedrock:UpdateProvisionedModelThroughput"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```
