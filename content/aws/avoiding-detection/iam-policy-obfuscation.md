---
author_name: Nick Frichette
title: "Obfuscating AWS IAM Policies"
description: Some techniques to obfuscate AWS IAM policies to avoid detection.
hide:
  - toc
---

A common tactic used by adversaries who gain access to AWS accounts is to attach IAM policies to new [users](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/iam/attach-user-policy.html) or [roles](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/iam/attach-role-policy.html) they've created. This may be for purposes of privilege escalation or as a means of maintaining persistence. 

When performing these actions, attackers have shown a trend of prioritizing highly-privileged policies (examples [one](https://securitylabs.datadoghq.com/articles/tales-from-the-cloud-trenches-ecs-crypto-mining/), [two](https://www.invictus-ir.com/news/the-curious-case-of-dangerdev-protonmail-me), and [three](https://expel.com/blog/incident-report-from-cli-to-console-chasing-an-attacker-in-aws/)). At face value, this makes sense; attackers want to maximize their access to resources, however, this potentially makes their activities blatantly obvious. Instead of a slick [CDR](https://sysdig.com/learn-cloud-native/what-is-cloud-detection-and-response-cdr/) or [SIEM](https://www.microsoft.com/en-us/security/business/security-101/what-is-siem), you might get caught by a simple [CNAPP](https://www.gartner.com/reviews/market/cloud-native-application-protection-platforms) or [CSPM](https://www.microsoft.com/en-us/security/business/security-101/what-is-cspm) complaining that a user has the `AdministratorAccess` policy attached.

In this post, we'll make the case that you don't need (or want) to attach highly-privileged policies to achieve your goals. We'll cover the importance of least privilege from the attackers perspective, and cover some examples to help you obfuscate your IAM policies, making it more difficult for security tools to identify your access.

## Attacker's should follow least privilege too

