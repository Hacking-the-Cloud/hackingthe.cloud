---
author: Nick Frichette
title: Bypass Credential Exfiltration Detection
description: When stealing IAM credentials from an EC2 instance you can avoid a GuardDuty detection by using the keys from another EC2 instance.
---

A common occurrence while performing penetration testing on AWS is leveraging SSRF, XXE, command injection, etc. to steal IAM credentials from the meta data service. This can allow you to execute API calls you otherwise wouldn't be able to (especially if you can't get code execution on the EC2 instance), however it comes at a penalty. There is a GuardDuty rule which detects IAM credentials being used outside of EC2 called [IAMUser/InstanceCredentialExfiltration](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#unauthorizedaccess-iam-instancecredentialexfiltration).

The wording is very specific, "This finding informs you of attempts to run AWS API operations from a host outside of EC2". It does not mean outside of EC2 instances in your account. It mean outside of EC2 AT ALL. As a result, you can use those credentials on ANY EC2 instance, including one you control. Doing so will not trigger the credential exfiltration GuardDuty finding.