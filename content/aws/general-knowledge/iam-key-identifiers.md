---
author_name: Nick Frichette
title: IAM unique identifiers
description: Chart of the IAM unique ID prefixes.
---

# IAM ID Identifiers

<div class="grid cards" markdown>

-   :material-book:{ .lg .middle } __Additional Resources__

    ---

    Reference: [AWS Documentation: Unique Identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids)

</div>

In AWS, different resources are assigned a "unique identifier". This identifier is a unique, 21 character value. The first four characters of the identifier are a prefix to denote the type of resource it represents.

The full list of prefixes can be found below.

| Prefix | Entity Type                  |
| ------ | ---------------------------  |
| ABIA   | AWS STS service bearer token |
| ACCA   | Context-specific credential  |
| AGPA   | Group                        |
| AIDA   | IAM user                     |
| AIPA   | Amazon EC2 instance profile  |
| AKIA   | Access key                   |
| ANPA   | Managed policy               |
| ANVA   | Version in a managed policy  |
| APKA   | Public key                   |
| AROA   | Role                         |
| ASCA   | Certificate                  |
| ASIA   | Temporary (AWS STS) keys     |

From a security perspective, there are 2 primary prefixes which are important to know, `AKIA` and `ASIA`.

## AKIA

IAM credentials with the `AKIA` prefix belong to long lived access keys. These are associated with IAM users. These credentials can potentially be exposed and used by attackers. Because they do not expire by default, they serve as an excellent vehicle to gain initial access to an AWS environment.

## ASIA

IAM credentials with the `ASIA` prefix belong to short lived access keys which were generated using [STS](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html). These credentials last for a limited time. In the event you come across an access key prefixed with `ASIA`, a secret key, and a session token, make use of them quickly before they expire.