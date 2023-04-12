---
author_name: Wes Ladd (@righteousgambit)
title: Unauthenticated Enumeration of Google Workspace Email Addresses
description: Discover how to exploit information disclosure configurations in Google Workspace to enumerate valid email addresses.
hide:
  - toc
---

# Unauthenticated Enumeration of Valid Google Workspace Email Addresses
You can enumerate valid email addresses associated with the Google Workspace service using [Quiet Riot](https://github.com/righteousgambit/quiet-riot). These addresses can be used for password spraying attacks, a technique where an attacker attempts to authenticate against multiple accounts using a set of commonly used passwords. This can potentially grant unauthorized access to the target account. It can also be used to test for valid Root User accounts in AWS, assuming that the email address is the same. Then, a similar password spraying approach can be implemented against identified AWS Root User accounts.