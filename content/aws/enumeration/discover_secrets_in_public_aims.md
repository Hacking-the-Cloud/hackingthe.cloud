---
author_name: Eduard Schwarzkopf
title: Discover secrets in public AMIs
description: How to find public AMIs and get stored secrets.
---

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    [AWS CloudQuarry: Digging for Secrets in Public AMIs](https://securitycafe.ro/2024/05/08/aws-cloudquarry-digging-for-secrets-in-public-amis/) by [Eduard Agavriloae](https://www.linkedin.com/in/eduard-k-agavriloae/) and [Matei Josephs](https://www.linkedin.com/in/matei-anthony-josephs-325ba5199/).
</div>

For EC2 instances, Amazon Machine Images (AMIs) are crucial as they contain the essential information required to launch instances, including the operating system, configuration files, software, and relevant data. A significant security consideration of these AMIs is that they can be (either accidentally or intentionally) made public, thus accessible for anyone to utilize and potentially exploit.

## Finding Exposed AMIs

Many instances of resource exposure (and subsequent exploitation) in AWS necessitate knowing the AMI ID. This offers some level of security-by-obscurity as an attacker needs the AMI ID to exploit the resource.

However, if AMIs are marked public, the list of available public AMIs is accessible through the AWS API. If you know the account ID, you can easily run through all regions to see if any public AMIs are available:

```bash
aws ec2 describe-images --owners <account_id> --include-deprecated --region <region>
```

## Using Public AMIs and Scanning for Credentials

Once you've identified public AMIs, you can use them to launch instances and manually scan for sensitive information, including credentials.

### Launching an Instance from a Public AMI

To launch an instance from a public AMI, follow these steps:

1. **Launch an Instance:**  
Using the AWS CLI, launch an instance using the desired AMI:
```bash
aws ec2 run-instances --image-id <image_id> --instance-type t2.micro --key-name <key-pair>

```
2. **Access the Instance:**  
Once the instance is running, connect to it using Session Manager or SSH:
```bash
ssh -i <your-key-pair>.pem ec2-user@<public-dns-of-instance>
```

### Manually Scanning for Credentials

Manual scanning involves checking common locations where credentials may be stored. Here are some typical command-line operations that can help:

1. **Search for AWS Credentials:**
```bash
find / -name "credentials" -type f
```
2. **Search for SSH Keys:**
```bash
find / -name "id_rsa" -type f
```
3. **Look for Configuration Files Containing Sensitive Information:**
Use `grep` to locate keywords such as 'password', 'secret', 'key', etc.
```bash
grep -ri 'password\|secret\|key' /path/to/search
```

## Automating the Process

While the manual process can be effective for targeted searches, automation provides efficiency and consistency at scale. 

You can write scripts or use specialized tools to automate the detection of sensitive information. Here are some approaches:

1. **Using Bash Scripts:**
Create a script that executes various `find` and `grep` commands. Save this as `scan.sh`:
```bash
#!/bin/bash
# Search for AWS credentials
find /home -name "credentials" -print

# Search for SSH keys
find /home -name "id_rsa" -print

# Search for sensitive information in configuration files
grep -ri 'password\|secret\|key' /home
```
Run the script on each instance:
```bash
chmod +x scan.sh
./scan.sh
```
2. **Using Specialized Tools:**
Tools like [truffleHog](https://github.com/trufflesecurity/trufflehog) and [gitleaks](https://github.com/gitleaks/gitleaks) can detect sensitive information in codebases and configurations.
