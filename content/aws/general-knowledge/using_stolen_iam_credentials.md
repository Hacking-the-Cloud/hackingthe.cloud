---
author_name: Nick Frichette
title: Using Stolen IAM Credentials
description: How to work with stolen IAM credentials and things to consider.
---

As a Penetration Tester or Red Teamer it is likely you will stumble into AWS IAM credentials during an assessment. The following is a step by step guide on how you can use them, things to consider, and methods to avoid detection.

## IAM Credential Characteristics

In AWS there are typically two types of credentials you will be working with, [long term](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) (access keys) and [short term](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html).

Long term credentials will have an access key that starts with `AKIA` and will be 20 characters long. In addition to the access key there will also be a secret access key which is 40 characters long. With these two keys, you can potentially make requests against the AWS API. As the name implies, these credentials have no specified lifespan and will be useable until they are intentionally disabled/deactivated. As a result, this makes them not recommended from a security perspective. Temporary security credentials are preferred.

Temporary credentials, by comparison, will have an access key that starts with `ASIA`, be 20 characters long, and also have a 40 character secret key. In addition, temporary security credentials will also have a session token (sometimes referred to as a security token). The session token will be base64 encoded and quite long. With these 3 credentials combined you can potentially make requests to the AWS API. As the name implies, these credentials have a temporary lifespan that is determined when they were created. It can be as short as 15 minutes, and as long as several hours.

## Working with the Keys

After gathering the credentials you will likely want to use them with the AWS CLI. There are a [few](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) ways to do this, however setting them as environment variables is likely the easiest. 

To do this with long term credentials, set the following environment variables.

```
export AWS_ACCESS_KEY_ID=AKIAEXAMPLEEXAMPLEEE
export AWS_SECRET_ACCESS_KEY=EXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLESEXAM
```

To do this with short term credentials, set the following environment variables.

```
export AWS_ACCESS_KEY_ID=ASIAEXAMPLEEXAMPLEEE
export AWS_SECRET_ACCESS_KEY=EXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLESEXAM
export AWS_SESSION_TOKEN=EXAMPLEEXAMPLEEXAMPLE...<snip>
```

!!! Note
    You may also have to specify an AWS region. This can be globally set with the `aws configure` command or through the `AWS_REGION` environment variable.

## Determining Validity

Now that you have credentials and have them setup to use, how can you determine if they are valid (not expired or deactivated)? The simplest way would be to make use of the [sts:GetCallerIdentity](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/get-caller-identity.html) API call. This method is helpful because it will allow us to determine if the credentials are valid and it will also tell us useful information such as the name of the role/user associated with these credentials and the AWS account ID they belong to.

As an added bonus, we can be confident this API call will always work. From the documentation, "No permissions are required to perform this operation. If an administrator adds a policy to your IAM user or role that explicitly denies access to the sts:GetCallerIdentity action, you can still perform this operation".

```
$ aws sts get-caller-identity
{
    "UserId": "AROAEXAMPLEEXAMPLEEXA:Nick",
    "Account": "123456789123",
    "Arn": "arn:aws:sts::123456789123:assumed-role/blah/Nick"
}
```

!!! Tip
    For defensive security professionals, it may be worthwhile to alert on invocations of `sts:GetCallerIdentity` from identities that have no history of calling it. For example, if an application server in a production environment has never called it before, that may be an indication of compromise.

    It is worth noting that `sts:GetCallerIdentity` may be [legitimately used](https://twitter.com/SpenGietz/status/1283846678194221057) by a large number of projects, and that individual developers may use it as well. To attempt to reduce the number of false positives, it would be best to only alert on identities which have no history of calling it.

### Operational Security Considerations

If you are attempting to maintain stealth, `sts:GetCallerIdentity` may be a risk. This API call logs to [CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html) which means that defenders will have a log with additional details that this occurred. To get around this, we can make use of [data events](https://aws.amazon.com/premiumsupport/knowledge-center/cloudtrail-data-management-events/).

Data events are high-volume API calls for resources in an AWS account. Because of the number of times these APIs may be called, they are not logged to CloudTrail by default and in some cases they cannot be logged at all.

An example of this would be [sqs:ListQueues](https://hackingthe.cloud/aws/enumeration/whoami/#sqslistqueues). By making this API call we can get similar information to `sts:GetCallerIdentity` without the risk of logging to CloudTrail.

```
user@host:~$ aws sqs list-queues

An error occurred (AccessDenied) when calling the ListQueues operation: User: arn:aws:sts::123456789012:assumed-role/no_perms/no_perms is not authorized to perform: sqs:listqueues on resource: arn:aws:sqs:us-east-1:123456789012: because no identity-based policy allows the sqs:listqueues action
```

For more information on this technique, please see its [article](https://hackingthe.cloud/aws/enumeration/whoami/).

## Avoiding Detection

There are situations where simply using the credentials could alert defenders to your presence. As a result, it is a good idea to be mindful of these circumstances to avoid being caught.

### GuardDuty Pentest Findings and CLI User Agents

If you are using a "pentesting" Linux distribution such as [Kali Linux](https://www.kali.org/), [Parrot Security](https://www.parrotsec.org/), or [Pentoo Linux](https://www.pentoo.ch/) you will immediately trigger a [PenTest GuardDuty finding](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#pentest-iam-kalilinux). This is because the AWS CLI will send along a user agent string which contains information about the operating system making the API call.

In order to avoid this, it is best to make use of a "safe" operating system, such as Windows, Mac OS, or Ubuntu. If you are short on time, or simply MUST use one of these Linux distributions, you can modify your [botocore](https://github.com/boto/botocore) library with a hard-coded user agent.

!!! Tip
    Are you going up against an apex blue team who will detect anything? It may be a good idea to spoof a user agent string that one would expect in the environment. For example, if these IAM credentials belong to a developer who uses a Windows workstation, it would be very strange for API calls to suddenly start having a user agent with a Linux operating system.

    Defenders, this may also be worth looking into for detection purposes.

For more information on this, please see its [article](https://hackingthe.cloud/aws/avoiding-detection/guardduty-pentest/).

### GuardDuty Credential Exfiltration

!!! Note
    This section only applies to IAM credentials taken from the [Instance Metadata Service](https://hackingthe.cloud/aws/general-knowledge/intro_metadata_service/) of an EC2 instance. It does not apply to other IAM credentials.

When using IAM credentials taken from an EC2 instance, you run the risk of triggering the [UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#unauthorizedaccess-iam-instancecredentialexfiltrationoutsideaws) GuardDuty finding. This finding alerts on scenarios in which IAM credentials from an EC2 instance are used from outside AWS (E.X your home IP address).

This is particularly relevant in scenarios in which you have access to the IAM credentials, but not the host ([Server Side Request Forgery](https://portswigger.net/web-security/ssrf)).

To get around this, we can make use of [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html) which will not trigger this alert. To make things easier, the [SneakyEndpoints](https://github.com/Frichetten/SneakyEndpoints) tool was developed to allow you to quickly stand up infrastructure to bypass this detection.

For more information on this, please see its [article](https://hackingthe.cloud/aws/avoiding-detection/steal-keys-undetected/).

## Situational Awareness

Now that you have everything set up and you know what to look out for, your next question may be, "what is in this AWS account?". If you are performing a no-knowledge assessment, and thus, don't have any insights into what services are running in the account, it makes it difficult to know what to target or look into.

One option would be to [enumerate the service-linked roles](https://hackingthe.cloud/aws/enumeration/enum_iam_user_role/) in the account. A [service-linked](https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html) role is a special kind of IAM role that allows an AWS service to perform actions in your account. Because of this, we can potentially enumerate them without authentication. 

From the previous validity checking step, we will know the AWS account ID we are operating in. That, combined with [this](https://hackingthe.cloud/aws/enumeration/enum_iam_user_role/) technique will allow us to enumerate what services the AWS account uses. This can be helpful to answer questions such as, "Is our target using GuardDuty? Is this account a part of an organization? Are they using containers (ECS, EKS), or are they using EC2?".

For more information on this, please see its [article](https://hackingthe.cloud/aws/enumeration/enum_iam_user_role/).