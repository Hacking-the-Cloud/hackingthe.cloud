---
author_name: skdg
title: Enumerate Root User Email Address from the AWS Console
description: Identify if an email address belongs to the root user of an AWS account.
hide:
  - toc
---

Based on error responses from the AWS Console it is possible to determine if a given email address belongs to the root user of an AWS account.

From the [AWS Console](https://console.aws.amazon.com/), ensure the `Root user` radio button is selected and enter an email address that you suspect owns an AWS account. 

If that email address is valid, you will be prompted to enter a password. If that email address is invalid, you will receive an error message:

```
There was an error - An AWS account with that sign-in information does not exist. Try again or create a new account.
```