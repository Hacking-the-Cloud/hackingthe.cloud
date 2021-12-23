---
author: Nick Frichette
title: "Terraform Enterprise: Attack the Metadata Service"
description: Leverage a default configuration in Terraform Enterprise to steal credentials from the Metadata Service
---

[Terraform Enterprise](https://www.terraform.io/enterprise) is a self-hosted version of Terraform Cloud, allowing organizations to maintain their own private instance of Terraform. There are many benefits for an enterprise to run this, however, there is also a default configuration that Red Teamers and Penetration Testers can potentially take advantage of.

## Remote (Code) Execution

For many engineers, their first experience with Terraform was locally on their workstations. When they invoked a `terraform apply` or `terraform plan` all of that activity took place on the engineers workstation, reaching out to cloud APIs, tracking state, etc.

An exciting feature of Terraform Enterprise (and Cloud) is the idea of [Remote Execution](https://www.terraform.io/cloud-docs/overview#remote-terraform-execution), wherein all those operations take place server-side. In Terraform Cloud the execution takes place in "disposable virtual machines". In [Terraform Enterprise](https://www.terraform.io/enterprise/install/interactive/installer#alternative-terraform-worker-image) however, it takes place in "disposable Docker containers". 

This introduces an interesting opportunity; If you compromise credentials to initiate a `plan` or `apply` operation (or otherwise have access to them. I.E insider threat) we can execute code in a Docker container on the Terraform Enterprise server.

!!! Note
    It is possible to disable Remote Execution via a configuration however this is [discouraged](https://www.terraform.io/cloud-docs/run#disabling-remote-operations). "Many of Terraform Cloud's features rely on remote execution, and are not available when using local operations. This includes features like Sentinel policy enforcement, cost estimation, and notifications."

## Docker Containers and Metadata Services

Aside from container escapes via [mounted Docker sockets](https://www.secureideas.com/blog/2018/05/escaping-the-whale-things-you-probably-shouldnt-do-with-docker-part-1.html) or [kernel exploits](https://www.cyberark.com/resources/threat-research-blog/the-route-to-root-container-escape-using-kernel-exploitation), running user-supplied code in a container is an interesting opportunity in a cloud context. The specifics will depend upon the cloud provider. For example, in AWS, an attacker could target the [Instance Metadata Service](https://hackingthe.cloud/aws/general-knowledge/intro_metadata_service/). This would provide the attacker IAM credentials for the IAM role associated with the EC2 instance.

Other opportunities include things such as the instance [user data](https://hackingthe.cloud/aws/general-knowledge/introduction_user_data/), which may help enumerate what software is on the host, or what integrations it has outside of it.

## Attack Prevention

It is worth noting that there are two potential methods to mitigate this attack. The first is the configuration of [restrict_worker_metadata_access](https://www.terraform.io/enterprise/system-overview/security-model#restrict-terraform-build-worker-metadata-access) in the Terraform Enterprise settings. This is __not__ the default, meaning that out of the box Terraform operations have access to the metadata service and its credentials.

The second option would depend upon the cloud provider, but options to harden or secure the Metadata Service can also be used. For example, [IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) in an AWS situation would prevent the [Docker container from reaching the Metadata Service](https://hackingthe.cloud/aws/general-knowledge/intro_metadata_service/).

!!! Note
    Nothing should prevent these two methods from working at the same time. It is a good idea to require IMDSv2 of all EC2 instances in your environment.

## Walkthrough
