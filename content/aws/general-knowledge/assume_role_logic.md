---
author: Nick Frichette
title: Assume Role Logic
description: How Assume Role functionality works cross account and in the same account.
---

To allow an entity to temporarily elevate their access to a different role, AWS provides the [AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) action in STS. This returns an access key ID, secret key, and a session token for the specified ARN.

As a Penetration Tester or Red Teamer, Assume Role can be an excellent vector to escalate privileges or move to other AWS accounts in the organization. It is worth noting however that the logic/requirements to perform Assume Role differ if you are assuming a role in the same account versus assuming a role in a different account.

## Same Account

In order to assume a role, there are typically two requirements: 1) The target role has a trust relationship with the entity attempting to assume the role and 2) the role attempting to perform the assumption has the [sts:AssumeRole](https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html) privilege. When attempting to assume a role in the same account, these requirements are slightly relaxed.

When assuming a role in the same account, the trust relationship for the target role may be tied to a specific role (via an ARN). In this situation that role does NOT need to have AssumeRole privilege. If, however, the trust relationship is tied to the ARN of the account itself that role DOES need to have AssumeRole privilege.

Here is an example of each situation.

### Trust Relationship with Account
You DO need AssumeRole privilege on the base role.
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
```

### Trust Relationship with Role
You DO NOT need AssumeRole privilege on the base role. Do note: having that privilege does not hinder you in any way.
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/specific-role"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    }
  ]
}
```

### Advice for Same Account
When looking for privilege escalation vectors in an AWS account, first look for roles that explicitly define a role ARN in their Trust Relationship and paths to get there. The relaxed requirement around having AssumeRole privileges helps because you are only reliant on the trust relationship, not additional privileges. Additionally, because of the different requirements between same and cross account role assumption, some administrators may be under the impression the base role requires AssumeRole privileges and as such may not be aware of the security considerations around this.

## Cross Account
When assuming a role across accounts the base role must have AssumeRole privileges, regardless of if the Trust Relationship specifies an account or a specific role.
