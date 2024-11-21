---
author_name: Nick Frichette
title: Enumerate AWS Account ID from a Public S3 Bucket
description: Knowing only the name of a public S3 bucket, you can ascertain the account ID it resides in.
---

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="https://cloudar.be/awsblog/finding-the-account-id-of-any-public-s3-bucket/">Finding the Account ID of any public S3 bucket</a> by <a href="https://twitter.com/benbridts">Ben Bridts</a></p>
    <p><img src="/images/researchers/ben_bridts.jpg" alt="Ben Bridts" style="width:44px;height:44px;margin:5px;border-radius:100%;max-width:unset"></img></p>
    </aside>

-   :material-tools:{ .lg .middle } __Tools mentioned in this article__

    ---

    [s3-account-search](https://github.com/WeAreCloudar/s3-account-search): A tool to find the account ID an S3 bucket belongs to.

</div>

!!! Note
    When you install a version <0.2.0 using [pip](https://pip.pypa.io/en/stable/), the executable is named `s3-account-search`.

By leveraging the s3:ResourceAccount policy condition, we can identify the AWS account ID associated with a public S3 bucket. This is possible because it supports wildcards (*). With this, we can sequentially enumerate the account ID.

To test this, you can use [Grayhat Warfare's](https://buckets.grayhatwarfare.com/random/buckets) list of public S3 buckets.

You will need a role with `s3:getObject` and `s3:ListBucket` permissions, and you can specify the target bucket as the resource for your policy. Alternatively, you can set a resource of '*' to quickly test multiple buckets.

## Installation

The tool can be installed with the following command:

```
python3 -m pip install s3-account-search
```

## Setup

To use the tool, there is some setup on your end. You will need your own AWS account with a role you can assume with the `s3:GetObject` or `s3:ListBucket` permissions. s3-account-finder will assume this role so make sure the credentials you're using can do this.

## Usage

```
s3-account-search arn:aws:iam::123456789123:role/s3-searcher <bucket name>
Starting search (this can take a while)
found: 1
found: 12
*** snip ***
found: 123456789123
```

!!! Warning  "Operational Security Tip"

    As of 2022's announcement, any new buckets are created without the Public Access policy and specifically without any ACLs. The removal of the ACLs means that the `GetObject`, instead you *must* enable the AWS ACLs that make S3 Buckets readable in addition to having GetBucket in the IAM Policy. Here is a terraform block to enable this abuse which use to be the default pre-2022. 

        ```
        resource "aws_s3_bucket_ownership_controls" "example" {
            bucket = aws_s3_bucket.example.id
            rule {
                object_ownership = "BucketOwnerPreferred"
            }
        }

        resource "aws_s3_bucket_public_access_block" "example" {
            bucket = aws_s3_bucket.example.id

            block_public_acls       = false
            block_public_policy     = false
            ignore_public_acls      = false
            restrict_public_buckets = false
        }

        resource "aws_s3_bucket_acl" "example" {
            bucket = aws_s3_bucket.example.id
            acl    = "public-read"

            depends_on = [
                aws_s3_bucket_ownership_controls.example,
                aws_s3_bucket_public_access_block.example
            ]
        }
        ```

!!! Tip
    Pair this with [Unauthenticated Enumeration of IAM Users and Roles](https://hackingthe.cloud/aws/enumeration/enum_iam_user_role/)!
