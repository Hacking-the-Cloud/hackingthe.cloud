---
author_name: Nick Frichette
title: Bypass Credential Exfiltration Detection
description: When stealing IAM credentials from an EC2 instance you can avoid a GuardDuty detection by using VPC Endpoints.
---

# Bypass Credential Exfiltration Detection

<div class="grid cards" markdown>

-   :material-tools:{ .lg .middle } __Tools mentioned in this article__

    ---

    [SneakyEndpoints](https://github.com/Frichetten/SneakyEndpoints): Hide from the InstanceCredentialExfiltration GuardDuty finding by using VPC Endpoints 

</div>

A common technique when exploiting AWS environments is leveraging SSRF, XXE, command injection, etc. to steal IAM credentials from the [instance metadata service](https://hackingthe.cloud/aws/general-knowledge/intro_metadata_service/) of a target EC2 instance. This can allow you to execute AWS API calls within the victim's account, however, it comes with a risk. If you were to try to use those credentials outside of that host (for example, from your laptop) an alert would be triggered. There is a GuardDuty finding which detects when IAM credentials are being used outside of EC2 called [UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#unauthorizedaccess-iam-instancecredentialexfiltrationoutsideaws).

To get around this alert being triggered, attackers could use the stolen credentials from the attacker's EC2 instance. The alert only detected if the credentials were used outside of EC2, not the victim's specific EC2 instance. So by using their own, or exploiting another EC2 instance, attackers could bypass the GuardDuty alert.

On January 20th 2022, AWS released a new GuardDuty finding called [UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.InsideAWS](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-iam.html#unauthorizedaccess-iam-instancecredentialexfiltrationinsideaws). This new finding addressed the shortcomings of the previous one. Now, when IAM credentials are used from ANY EC2 instance, if those credentials don't belong to the same account as the EC2 instance which generated them, it triggers the alert. Thus, simply using your own EC2 instance is no longer viable. This addresses a long standing concern within the cloud security community.

However, there is currently a functioning bypass for this - [VPC Endpoints](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html). Using VPC Endpoints will not trigger the GuardDuty alert. What this means is that, as an attacker, `if you steal IAM credentials from an EC2 instance, you can use those credentials from your own EC2 instance while routing traffic through VPC Endpoints. This will not trigger the GuardDuty finding`.

!!! Note
    There is another bypass option, however, it would only be useful in niche scenarios. The InstanceCredentialExfiltration finding is only tied to the AWS account, not the EC2 instance. As a result, if you compromise an EC2 instance in the target account and then compromise OTHER EC2 instances in the account, or steal their IAM credentials, you can safely use them from the initially compromised instance without fear of triggering GuardDuty.

## SneakyEndpoints

To make this setup faster/easier for Penetration Testers and Red Teamers, [SneakyEndpoints](https://github.com/Frichetten/SneakyEndpoints) was created. This project is a collection of Terraform configurations which can quickly spin up an environment to attack form. It will create an EC2 instance in a private subnet (no internet access) and create a number of VPC Endpoints for you to use. This setup ensures we don't accidentally access an internet facing API endpoint and trigger the alert.

## Setup and Usage

To use SneakyEndpoints first install [Terraform](https://www.terraform.io/) and set AWS credentials within your shell session. 

Next, perform the following Terraform commands:

```shell
terraform init
terraform apply
```

Before continuing Terraform will ask you to confirm the deployment. After that, way ~10 minutes for everything to be done. Please note that after the deployment is finished it may take a short period of time for the EC2 instance to be connectable.

After this period of time, connect to the EC2 instance using the [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html).

To teardown the infrastructure, run the following command:

```shell
terraform destroy
```

## Using STS

Due to a [quirk](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_sts_vpce.html#id_credentials_sts_vpce_create) in how STS is setup, you will have to set a specific environment variable with the following command.

```shell
export AWS_STS_REGIONAL_ENDPOINTS=regional
```

This is because some versions of the AWS SDK default to using the global STS endpoint at `sts.amazonaws.com`. This is problematic because VPC endpoints are regional (e.g. `sts.us-east-1.amazonaws.com`). The result is that if you use a version that is expecting the global endpoint with SneakyEndpoints, the connection will timeout.