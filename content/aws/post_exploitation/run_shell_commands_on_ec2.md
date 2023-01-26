---
author_name: Nick Frichette
title: "Run Shell Commands on EC2 with Send Command or Session Manager"
description: Leverage privileged access in an AWS account to run arbitrary commands on an EC2 instance.
---

After escalating privileges in a target AWS account or otherwise gaining privileged access you may want to run commands on EC2 instances in the account. This article hopes to provide a quick and referenceable cheat sheet on how to do this via [ssm:SendCommand](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/send-command.html) or [ssm:StartSession](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/start-session.html).

!!! Tip
    By default, the commands that are issued are not logged to CloudTrail. Specifically they are "HIDDEN_DUE_TO_SECURITY_REASONS". As a result, if an adversary were to leverage this tactic against an environment, defenders would need to get information about those commands from host based controls. Defenders, this is an excellent capability to validate. Alternatively, offensive security teams can do the testing.

## Send Command

**Required IAM Permission**: [ssm:SendCommand](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/send-command.html)  
**Recommended But Not Strictly Required**: [ssm:ListCommandInvocations](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/list-command-invocations.html), [ec2:DescribeInstances](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/describe-instances.html)

You can send arbitrary shell commands to EC2 instances from the AWS CLI via the following:

```
aws ssm send-command \
--instance-ids "i-00000000000000000" \
--document-name "AWS-RunShellScript"
--parameters commands="*shell commands here*"
```

If you're just looking to run a quick C2 payload, or perhaps create a new user this will likely be enough. However, if you also want to retrieve the output of the command you will need to make a [ssm:ListCommandInvocations](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/list-command-invocations.html) call as well.

If you would like to retrieve the output, make a note of the `CommandId` returned to you in the Send Command call. After a short period of time (to let the command run) you can use this Id to lookup the results. You can do this with the following:

```
aws ssm list-command-invocations \
--command-id "command_id_guid" \
--details
```

!!! Note
    The `--details` is required to view the output of the command.
    
The output of the command will be in the `Output` section under `CommandPlugins`.

## Session Manager

**Required IAM Permission**: [ssm:StartSession](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/start-session.html)

If instead you'd like a more interactive shell experience, you can make use of [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html). Session Manager allows you to have an SSH-esc experience, making it easy to interact with EC2 instances.

To begin, you will first need to [install the SSM Session Manager Plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html). The specifics of this will depend on what operating system you are using.

With that installed, you can then run the following command to start an interactive session.

```
aws ssm start-session --target instance-id
```
