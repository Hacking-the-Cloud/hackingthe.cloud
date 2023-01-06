---
author_name: skdg
title: Enumerate AWS root account ID from AWS Console
description: Unauthorized users can identify whether an AWS root account is valid or invalid
---

From the [AWS Console](https://console.aws.amazon.com/), make sure the "Root-user" radio button is selected and enter an email address that you suspect owns an AWS account. 
If that email address is valid, it will prompt you to enter a password.
If that email address is invalid, you will receive an error message:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*"There was an error - An AWS account with that sign-in information does not exist. Try again or create a new account."*
