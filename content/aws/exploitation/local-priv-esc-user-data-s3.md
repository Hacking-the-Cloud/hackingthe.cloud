---
author_name: Nick Frichette
title: "Local Privilege Escalation: User Data 2"
description: Escalate privileges on an EC2 instance by modifying scripts and packages called by user data.
hide:
  - toc
---

# Local Privilege Escalation: User Data 2

A common pattern when using EC2 is to define a [user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) script to be run when an instance is first started or after a reboot. These scripts are typically used to install software, download and set a config, etc. Oftentimes the scripts and packages are pulled from S3 and this introduces an opportunity for a developer/ops person to make a mistake.

If the IAM role is too permissive and allows the role to write to that location, an adversary can leverage this for privilege escalation. Additionally, if there is any other kind of misconfiguration on the bucket itself, or another role which has access gets compromised, an adversary can take advantage of this as well.

Take the following user data script:

```
#!/bin/bash
aws s3 cp s3://example-boot-bucket/start_script.sh /root/start_script.sh
chmod +x /root/start_script.sh
/root/start_script.sh
```

On first launch, the EC2 instance will pull the start_script from S3 and will run it. If an adversary can write to that location, they can escalate privileges or gain control of the EC2 instance.

!!! Note
    In addition to new instances being spun up or after a reboot, poisoning the scripts/applications can also effect EC2 instances in an [Auto Scaling Group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/AutoScalingGroup.html).
