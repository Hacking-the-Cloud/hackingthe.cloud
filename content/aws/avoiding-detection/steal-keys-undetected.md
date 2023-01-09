---
author_name: Nick Frichette
title: Bypass Credential Exfiltration Detection
description: When stealing IAM credentials from an EC2 instance you can avoid a GuardDuty detection by using VPC Endpoints.
hide:
  - toc
---

# Bypass Credential Exfiltration Detection

Link to Tool: [SneakyEndpoints](https://github.com/Frichetten/SneakyEndpoints)

A common technique when exploiting AWS environments is leveraging SSRF, XXE, command injection, etc. to steal IAM credentials from the [instance metadata service](https://hackingthe.cloud/aws/general-knowledge/intro_metadata_service/) of a target EC2 instance. This can allow you to execute AWS API calls within the victim's account, however, it comes with a risk. If you were to try to use those credentials outside of that host (for example, from your laptop) an alert would be triggered. There is a GuardDuty finding which detects when IAM credentials are being used outside of EC2 called [UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#unauthorizedaccess-iam-instancecredentialexfiltrationoutsideaws).

To get around this alert being triggered, attackers could use the stolen credentials from the attacker's EC2 instance. The alert only detected if the credentials were used outside of EC2, not the victim's specific EC2 instance. So by using their own, or exploiting another EC2 instance, attackers could bypass the GuardDuty alert.

On January 20th 2022, AWS released a new GuardDuty finding called [UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#unauthorizedaccess-iam-instancecredentialexfiltrationinsideaws). This new finding addressed the shortcomings of the previous one. Now, when IAM credentials are used from ANY EC2, if those credentials don't belong to the same account as the EC2 instance using them, it triggers the alert. Thus, simply using your own EC2 instance is no longer viable. This addresses a long standing concern within the cloud security community.

However, there is currently a functioning bypass for this - [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html). Using VPC Endpoints will not trigger the GuardDuty alert. What this means is that, as an attacker, `if you steal IAM credentials from an EC2 instance, you can use those credentials from your own EC2 instance while routing traffic through VPC Endpoints. This will not trigger the GuardDuty finding`.

To make this setup faster (and easier) for Penetration Testers and Red Teamers, [SneakyEndpoints](https://github.com/Frichetten/SneakyEndpoints) was created. This project has all the Terraform configurations necessary to spin up an environment to attack from. It will create an EC2 instance in a private subnet (no internet access) and create a number of VPC Endpoints for you to use. This setup ensures we don't accidentally expose ourselves and trigger the alert.

!!! Note
    There is another bypass option, however, it would only be useful in niche scenarios. The InstanceCredentialExfiltration finding is only tied to the AWS account, not the EC2 instance. As a result, if you compromise an EC2 instance in the target account and then compromise OTHER EC2 instances in the account, or steal their IAM credentials, you can safely use them from the initially compromised instance without fear of triggering GuardDuty.