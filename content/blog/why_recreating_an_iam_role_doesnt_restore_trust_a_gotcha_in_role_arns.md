---
title: "Why Recreating an IAM Role Doesn't Restore Trust: A Gotcha in Role ARNs"
description: <A description of the page>
date: 2025-5-5T00:00:40-06:00
---
<aside markdown style="display:flex">
  <p><img src="https://avatars.githubusercontent.com/u/10386884?v=4" style="width:44px;height:44px;margin:5px;border-radius:100%"></img></p>

  <span>__Nick Frichette__ · @frichette_n · <a href="https://twitter.com/Frichette_n">:fontawesome-brands-twitter:{ .twitter }</a> <a href="https://fosstodon.org/@frichetten">:fontawesome-brands-mastodon:{ .mastodon }</a> <a href="https://bsky.app/profile/frichetten.com">:fontawesome-brands-bluesky:{ .bluesky }</a></span>
  <br>
  <span>
    :octicons-calendar-24: May 5, 2025
  </span>
</aside>
---

**TL;DR**: In AWS IAM, trust policies often reference other roles by their Amazon Resource Name (ARN). But if a referenced IAM role is deleted and recreated, even with the *same name*, the trust policy breaks. The new role may look identical, but AWS assigns it a different internal identity, and trust relationships no longer apply.

This subtle behavior can disrupt cross-account access, third-party integrations, and automation workflows.

## The Scenario
In cloud environments, identity and access management is both foundational and deceptively complex. One lesser-known nuance in AWS IAM is how trust relationships behave when a role is deleted and recreated.

Imagine you have a trust policy attached to a role named `Bobby` and that this trust policy permits the role named `Megan` to assume it as shown below.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::111111111111:role/Megan"
            },
            "Action": "sts:AssumeRole",
            "Condition": {}
        }
    ]
}
```

If the `Megan` role is deleted and then recreated, perhaps using automation or Terraform, users may expect this policy to continue working. After all, the ARN is the same, why wouldn't it work? Well, how about we delete the Megan role, recreate it, and see what happens to the trust policy?

## Deleting and Recreating the Role
Should we delete `Megan`, then recreate her role and check back in on `Bobby`'s trust policy we will find it now looks like this:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "AROAABCDEFGHIJKLMNOPQ"
            },
            "Action": "sts:AssumeRole",
            "Condition": {}
        }
    ]
}
```

What happened? Where did the ARN go? 

##Why This Happens

At first glance, it’s easy to assume that the ARN of a role is its unique identifier. After all, it's what we use in trust policies, logs, error messages, and Terraform or CloudFormation templates. It looks like a primary key, acts like a primary key, so it must be the primary key, right?

Not quite.

Under the hood, AWS assigns each IAM role an internal, immutable [role ID](../aws/general-knowledge/iam-key-identifiers.md) when it is created. This role ID, not the ARN, is what actually identifies the role in trust relationships, policy evaluations, and service-level authorizations.

The ARN is best thought of as a human-readable label, similar to a username. It’s a convenient pointer, but it’s not the source of truth. When you delete a role, AWS also discards the associated role ID. Recreating a role, even with the exact same name, results in a completely new role with a new role ID. The ARN may be identical, but the underlying identity is not.

This is why a trust policy that still references the original ARN will silently fail: it's pointing to an identity that no longer exists. The policy is technically valid JSON, but AWS can no longer resolve that ARN to a live principal with the matching role ID.

AWS explicitly calls this out in their [IAM documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-roles):

> If your Principal element in a role trust policy contains an ARN that points to a specific IAM role, then that ARN transforms to the role unique principal ID when you save the policy. This helps mitigate the risk of someone escalating their privileges by removing and recreating the role. You don't normally see this ID in the console, because IAM uses a reverse transformation back to the role ARN when the trust policy is displayed. However, if you delete the role, then you break the relationship. The policy no longer applies, even if you recreate the role because the new role has a new principal ID that does not match the ID stored in the trust policy

This is further elaborated in this [re:Post article](https://repost.aws/articles/ARSqFcxvd7R9u-gcFD9nmA5g/understanding-aws-s-handling-of-deleted-iam-roles-in-policies).

##Why This is a Good Thing

While frustrating at times, this behavior is a security feature. It prevents someone from deleting a trusted IAM role and then recreating it to inherit that trust, which could otherwise lead to unintended privilege escalation or lateral movement.

By locking trust relationships to unique role IDs, AWS ensures that trust must be explicit and intentional, not assumed by name reuse.

## Why this may be Dangerous

While tying trust relationships to immutable role IDs is a sound security decision, this behavior can introduce operational risk, especially in SaaS integrations.

Many SaaS platforms, especially in the security, observability, or data pipeline space, allow customers to establish integrations by trusting a specific IAM role via an ARN. The SaaS provider configures their side to call sts:AssumeRole on a role in a customer’s AWS account and uses that role to perform whatever their service needs to do.

Say that SaaS provider makes a mistake and deletes the trusted IAM Role and recreates it (intentionally or not), that new IAM role will have a different principal ID. While the ARN may be the same, from AWS' perspective that is not the same IAM role. The result? 

The SaaS provider will not be able to assume any of their customer roles.

To make matters worse, the only solution in this situation is for every single customer to modify the trust policy of their SaaS roles in every single AWS account to trust the new IAM role in the SaaS account. This can introduce downtime, addition support requests, and other issues.

## Conclusion

IAM roles may look simple on the surface, but the way AWS handles trust relationships reveals a deeper truth: identity is more than a name. When you delete and recreate a role, even with the same ARN, AWS treats it as a completely different entity. That distinction can lead to subtle, hard-to-debug failures in everything from security controls to SaaS integrations.

Whether you’re building secure infrastructure, managing third-party access, or testing cloud security boundaries, understanding this behavior is essential. Trust isn’t just about syntax—it’s about identity, and AWS is very specific about who it trusts.
