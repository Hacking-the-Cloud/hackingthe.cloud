---
author: Ben Leembruggen
title: Modify GuardDuty Configuration
description: Modify existing GuardDuty configurations in the target account to hinder alerting and remediation capabilities.
---

When an account has been successfully compromised, an attacker can modify threat detection services like GuardDuty to reduce the likelihood of their actions triggering an alert.  Modifying, as opposed to outright deleting, key attributes of GuardDuty may be less likely to raise alerts, and result in a similar degradation of effectiveness.  The actions available to an attacker will largely depend on the compromised permissions available to the attacker, the GuardDuty architecture and the presence of higher level controls like Service Control Policies. 

## GuardDuty
Where GuardDuty uses a delegated admin or invite model, features like detector configurations and IP Trust lists are centrally managed, and so only able to be modified in the GuardDuty administrator account.  Where this is not the case, these features can be modified in the account that GuardDuty is running in.

---
### Misconfiguring the Detector
An attacker could modify an existing GuardDuty detector in the account, to remove logs sources or lessen its effectiveness.

Configuration changes may include a combination of:
- Disabling the detector altogether.
- Removing Kubernetes and s3 as data sources, which removes all [S3 Protection](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-s3.html) and [Kubernetes alerts](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-kubernetes.html).
- Increasing the event update frequency to 6 hours, as opposed to as low as 15 minutes.


#### Required Permissions to execute:
- guardduty:ListDetectors
- guardduty:UpdateDetector

Example CLI commands
```
# Disabling the detector
aws guardduty update-detector \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --no-enable 

# Removing s3 as a log source
aws guardduty update-detector \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --data-sources S3Logs={Enable=false}

# Increase finding update time to 6 hours
aws guardduty update-detector \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --finding-publishing-frequency SIX_HOURS
```
---
### Modifying Trusted IP Lists
An attacker could create or update GuardDuty's [Trusted IP list](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html), including their own IP on the list.  Any IPs in a trusted IP list will not have any Cloudtrail or VPC flow log alerts raised against them. 

<i> DNS findings are exempt from the Trusted IP list </i>

#### Required Permissions to execute:
- guardduty:ListDetectors
- guardduty:ListIPSet
- iam:PutRolePolicy
- guardduty:CreateIPSet (To create new list)
- guardduty:UpdateIPSet (To update an existing list)

<i> Depending on the level of stealth required, the file can be uploaded to an s3 bucket in the target account, or an account controlled by the attacker. </i>


Example CLI commands
```
aws guardduty update-ip-set \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --ip-set-id 24adjigdk34290840348exampleiplist \
    --location https://malicious-bucket.s3-us-east-1.amazonaws.com/customiplist.csv \
    --activate
```

---
### Modify Cloudwatch events rule
GuardDuty populates its findings to Cloudwatch Events on a 5 minute cadence.  Modifying the Event pattern or Targets for an event may reduce GuardDuty's ability to alert and trigger auto-remediation of findings, especially where the remediation is triggered in a member account - as GuardDuty administrator protections do not extend to the Cloudwatch events in the member account. 

!!! Note  
In a delegated or invitational admin GuardDuty architecture, cloudwatch events will still be created in the admin account.

#### Required Permissions to execute:
- event:ListRules
- event:ListTargetsByRule
- event:PutRule
- event:RemoveTargets

Example CLI commands
```
# Disable GuardDuty Cloudwatch Event
aws events put-rule --name guardduty-event \
--event-pattern "{\"source\":[\"aws.guardduty\"]}" \
--state DISABLED

# Modify Event Pattern
aws events put-rule --name guardduty-event \
--event-pattern '{"source": ["aws.somethingthatdoesntexist"]}'

# Remove Event Targets
aws events remove-targets --name guardduty-event \
--ids "GuardDutyTarget"
```