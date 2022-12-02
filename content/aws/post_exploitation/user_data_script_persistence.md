---
author_name: Nick Frichette
title: User Data Script Persistence
description: Maintain access to an EC2 instance and it's IAM role via user data scripts.
---

When using EC2 instances a common design pattern is to define a [user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html) script to be run when an instance is first started or after a reboot. These scripts are typically used to install software, download a config, etc. Additionally these scripts are run as root or System which makes them even more useful. Should we gain access to an EC2 instance we may be able to persist by abusing user data scripts via two different methods.

## Modify the User Data Script
**Required IAM Permission**: [modify-instance-attribute](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/modify-instance-attribute.html)  
**Recommended but not required**: [start-instances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/start-instances.html), [describe-instances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instances.html), [stop-instances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/stop-instances.html) (makes things go faster, requires less enumeration. The instance must be stopped to alter the user data)  

If we have permission to directly modify the user data scripts, we can potentially persist by adding our own backdoor to it. To do this, we must stop the instance because user data scripts can only be modified when the instance is stopped. You could theoretically wait for this to happen naturally, have a script that constantly tries to modify it, or stop it yourself if you have permissions to do so.

The steps to modify user data scripts can be found [here](/aws/exploitation/local-priv-esc-mod-instance-att/).

### Modify a Resource Called by the Script
In situations where we cannot modify the user data script itself, we may be able to modify a resource called by the script. Say for example a script is downloaded by an S3 bucket, we may be able to add our backdoor to it.