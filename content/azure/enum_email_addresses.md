---
author_name: Wes Ladd (@righteousgambit)
title: Unauthenticated Enumeration of Azure Active Directory Email Addresses
description: Discover how to exploit information disclosure configurations in Azure Active Directory to enumerate valid email addresses.
hide:
  - toc
---

# Unauthenticated Enumeration of Valid Azure Active Directory Email Addresses
You can enumerate valid email addresses associated with the Azure Active Directory service using [CredMaster](https://github.com/knavesec/CredMaster) or [Quiet Riot](https://github.com/righteousgambit/quiet-riot). These addresses can be used for password spraying attacks, a technique where an attacker attempts to authenticate against multiple accounts using a set of commonly used passwords. This can potentially grant unauthorized access to the target account. It can also be used to test for valid Root User accounts in AWS, assuming that the email address is the same. Then, a similar password spraying approach can be implemented against identified AWS Root User accounts.