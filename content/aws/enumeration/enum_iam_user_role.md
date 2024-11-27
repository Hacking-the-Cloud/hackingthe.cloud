---
author_name: Nick Frichette, Wes Ladd (@righteousgambit), and skdg
title: Unauthenticated Enumeration of IAM Users and Roles
description: Discover how to exploit cross-account behaviors to enumerate IAM users and roles in another AWS account without authentication.
hide:
  - toc
---

# Unauthenticated Enumeration of IAM Users and Roles  

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="https://www.youtube.com/watch?v=8ZXRw4Ry3mQlink">Hacking AWS end-to-end - remastered</a> by <a href="https://twitter.com/dagrz">Daniel Grzelak</a></p>
    <p><img src="/images/researchers/daniel_grzelak.jpg" alt="Daniel Grzelak" style="width:44px;height:44px;margin:5px;border-radius:100%;max-width:unset"></img></p>
    </aside>

-   :material-book:{ .lg .middle } __Additional Resources__

    ---

    Reference: [Unauthenticated AWS Role Enumeration (IAM Revisited)](https://rhinosecuritylabs.com/aws/aws-role-enumeration-iam-p2/)

-   :material-tools:{ .lg .middle } __Tools mentioned in this article__

    ---

    - [quiet-riot](https://github.com/righteousgambit/quiet-riot)  
    - [enumerate_iam_using_bucket_policy](https://github.com/Frichetten/enumate_iam_using_bucket_policy)
    - [pacu:iam_enum_roles](https://github.com/RhinoSecurityLabs/pacu/tree/master/pacu/modules/iam__enum_roles)
</div>

You can enumerate AWS Account IDs, Root User account e-mail addresses, IAM roles, IAM users, and gain insights to enabled AWS and third-party services by abusing [Resource-Based Policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_resource-based), even in accounts for which you have no access. [Quiet Riot](https://github.com/righteousgambitresearch/quiet-riot) offers a scalable method for enumerating each of these items with configurable wordlists per item type. Furthermore - it also allows you to enumerate Azure Active Directory and Google Workspace valid email addresses - which can then be used to test for valid Root User accounts in AWS, assuming that the email address is the same.

Ultimately, if you want to perform these techniques at scale - Quiet Riot is your best bet, but if you want to do it manually, you can a number of ways to do so. Another way to enumerate IAM principals would be to use S3 Bucket Policies. Take the following example:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Example permissions",
            "Effect": "Deny",
            "Principal": {
                "AWS": "arn:aws:iam::123456789123:role/role_name"
            },
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::*bucket you own*"
        }
    ]
}
```

You would apply this policy to a bucket <ins>you</ins> own. By specifying a principal in the target account (123456789123), you can determine if that principals exists. If setting the bucket policy succeeds you know the role exists. If it fails you know the role does not.

There are a few ways to do this, for example, Pacu's module will attempt to change the AssumeRole policy of a role in <ins>your</ins> account and specify a role in another account. If the role exists, the policy will be updated and no error will be returned. If the role does not exist, the policy will not be updated and instead return an error.

!!! Warning
    Doing either of these techniques will generate a lot of CloudTrail events, specifically UpdateAssumeRolePolicy or PutBucketPolicy in your account. If your intention is to be stealthy it is not advised (or required) to use a target's credentials. Instead you should use your **own** account (the CloudTrail events will be generated there).
    
!!! Note
    While this works for both IAM users and roles, this will also work with [service-linked roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html). This will allow you to enumerate various services the account uses, such as GuardDuty or Organizations.

Another method uses the AWS Console. Based on error responses from the AWS Console it is possible to determine if a given email address belongs to the root user of an AWS account.

From the [AWS Console](https://console.aws.amazon.com/), ensure the `Root user` radio button is selected and enter an email address that you suspect owns an AWS account. 

If that email address is valid, you will be prompted to enter a password. If that email address is invalid, you will receive an error message:

```
There was an error - An AWS account with that sign-in information does not exist. Try again or create a new account.
```
