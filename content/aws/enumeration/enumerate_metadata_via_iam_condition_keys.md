---
author_name: Raajhesh Kannaa Chidambaram
title: Enumerate AWS Metadata via IAM Condition Keys
description: Abuse IAM policy condition keys to enumerate account IDs, organization IDs, and resource tag values from accessible AWS resources.
---

# Enumerate AWS Metadata via IAM Condition Keys

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="https://cloudar.be/awsblog/finding-the-account-id-of-any-public-s3-bucket/">Finding the Account ID of any public S3 bucket</a> by <a href="https://twitter.com/benbridts">Ben Bridts</a></p>
    </aside>

    <aside style="display:flex">
    <p><a href="https://www.plerion.com/blog/conditional-love-for-aws-metadata-enumeration">Conditional Love for AWS Metadata Enumeration</a> by <a href="https://github.com/dagrz">Daniel Grzelak</a> (Plerion)</p>
    </aside>

-   :material-tools:{ .lg .middle } __Tools mentioned in this article__

    ---

    [conditional-love](https://github.com/plerionhq/conditional-love)

</div>

## Overview

AWS IAM policies support condition keys that are evaluated at request time. Some of these condition keys reference resource metadata like account IDs, organization IDs, and tag values. By crafting IAM policies with wildcard conditions and observing whether API calls succeed or fail, an attacker can extract this metadata character by character.

This technique was first demonstrated by [Ben Bridts](https://cloudar.be/awsblog/finding-the-account-id-of-any-public-s3-bucket/) in 2021 for extracting account IDs from public S3 buckets using the `s3:ResourceAccount` condition key. [Daniel Grzelak](https://www.plerion.com/blog/conditional-love-for-aws-metadata-enumeration) at Plerion generalized this approach and released [conditional-love](https://github.com/plerionhq/conditional-love), a tool that applies it across multiple AWS services and condition types.

## How It Works

The attack uses IAM policy evaluation as an oracle. The attacker controls their own IAM principal and can create or modify policies attached to it.

**Step 1:** The attacker creates a policy that allows access to a target resource, but only if a condition key matches a wildcard pattern:

```json
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::target-bucket/*",
        "Condition": {
            "StringLike": {
                "s3:ResourceAccount": "9*"
            }
        }
    }]
}
```

**Step 2:** The attacker makes an API call against the target resource. If the call succeeds, the account ID starts with `9`. If it fails with `AccessDenied`, it does not.

**Step 3:** Repeat with `90*`, `91*`, `92*`... narrowing down one character at a time until the full 12-digit account ID is recovered. This takes at most ~120 API calls (12 digits x 10 possibilities each).

The same approach works for any condition key that supports `StringLike` with wildcards.

## What Can Be Enumerated

| Condition Key | What It Reveals |
|---|---|
| `aws:ResourceAccount` / `s3:ResourceAccount` | Account ID of the resource owner |
| `aws:ResourceOrgID` | AWS Organization ID |
| `aws:ResourceOrgPaths` | Full organizational unit path |
| `aws:ResourceTag/{key}` | Tag values (if you know the tag key name) |
| `lambda:FunctionArn` | Lambda function ARN components |

## Supported Services

The [conditional-love](https://github.com/plerionhq/conditional-love) tool supports enumeration through:

- **S3** via `HeadObject`
- **Lambda Function URLs** (when using `AWS_IAM` auth mode)
- **API Gateway** (when using `AWS_IAM` auth mode)
- **STS** via `AssumeRole`
- **SQS** via `ReceiveMessage`
- **AWS Data Exchange** via `GetDataSet`

Any service where the attacker's principal has some access to the target resource and AWS evaluates condition keys can potentially be used.

## Using conditional-love

Install and run the tool:

```bash
git clone https://github.com/plerionhq/conditional-love.git
cd conditional-love
pip install -r requirements.txt
python conditional_love.py \
    --target-type s3 \
    --target-value my-target-bucket \
    --condition-key s3:ResourceAccount
```

The tool handles the binary search automatically and outputs the discovered value.

## Security Implications

The most dangerous application is **tag value exfiltration**. Organizations often store meaningful data in resource tags: cost center codes, owner email addresses, environment names, or project identifiers. If an attacker knows (or guesses) the tag key name, they can extract the value from any resource they can access.

Account IDs and organization IDs are also valuable for reconnaissance. Knowing the account ID enables further attacks like [enumerating IAM principals](../enumeration/enum_iam_user_role.md) or crafting targeted phishing with knowledge of the internal org structure.

## Mitigations

- **Never store sensitive information in resource tags.** AWS [explicitly discourages](https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html) using tags for confidential data.
- **Publish shared resources from isolated accounts.** If you share AMIs, Lambda layers, or S3 buckets publicly, use a purpose-built account separate from production.
- **Restrict resource policies to authorized principals.** The technique requires the attacker to have some level of access to the target resource.
- **Monitor for unusual IAM policy modifications.** Policies with `StringLike` conditions using wildcards against `ResourceAccount` or `ResourceTag` keys may indicate enumeration attempts.
