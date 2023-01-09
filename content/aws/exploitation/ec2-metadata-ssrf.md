---
author_name: Nick Frichette
title: Steal EC2 Metadata Credentials via SSRF
description: Old faithful; How to steal IAM Role credentials from the EC2 Metadata service via SSRF.
hide:
  - toc
---

# Steal EC2 Metadata Credentials via SSRF

!!! Note
    This is a common and well known attack in AWS environments. [Mandiant](https://www.mandiant.com/) has identified [attackers performing automated scanning of vulnerabilities](https://www.mandiant.com/resources/cloud-metadata-abuse-unc2903) to harvest IAM credentials from publicly-facing web applications. To mitigate the risks of this for your organization, it would be beneficial to enforce [IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html) for all EC2 instances which has [additional security benefits](https://hackingthe.cloud/aws/general-knowledge/intro_metadata_service/#the-security-benefits-of-imdsv2). IMDSv2 would significantly reduce the risk of an adversary stealing IAM credentials via SSRF.

One of the most commonly taught tactics in AWS exploitation is the use of Server Side Request Forgery (SSRF) to access the EC2 metadata service.

Most EC2 Instances have access to the metadata service at 169.254.169.254. This contains useful information about the instance such as its IP address, the name of the security group, etc. On EC2 instances that have an IAM role attached the metadata service will also contain IAM credentials to authenticate as this role. Depending on what version of IMDS is in place, and what capabilities the SSRF has we can steal those credentials.

It is also worth noting that shell access to the EC2 instance would also allow an adversary to gather these credentials.

In this example there is a web server running on port 80 of the EC2 instance. This web server has a simple SSRF vulnerability, allowing us to make GET requests to arbitrary addresses. We can leverage this to make a request to `http://169.254.169.254`.

<figure markdown>
  ![Showing SSRF](/images/aws/exploitation/ec2-metadata-ssrf/showing-ssrf.png){ loading=lazy }
</figure>

To determine if the EC2 instance has an IAM role associated with it, look for http://169.254.169.254/latest/meta-data/iam/. A 404 response indicates there is no IAM role associated. You may also get a 200 response that is empty, this indicates that there was an IAM Role however it has since been revoked.

If there is a valid role you can steal, make a request to http://169.254.169.254/latest/meta-data/iam/security-credentials/. This will return the name of the IAM role the credentials represent. In the example below we see that the role name is 'ec2-default-ssm'.

<figure markdown>
  ![Role Name](/images/aws/exploitation/ec2-metadata-ssrf/role-name.png){ loading=lazy }
</figure>

To steal the credentials, append the role name to your previous query. For example, with the name above we'd query http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2-default-ssm/.

<figure markdown>
  ![Stolen Keys](/images/aws/exploitation/ec2-metadata-ssrf/stolen-keys.png){ loading=lazy }
</figure>

These credentials can then be used in the AWS CLI or other means to make API calls as the IAM role.
