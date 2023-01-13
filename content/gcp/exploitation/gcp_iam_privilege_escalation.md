---
author_name: Aloïs THÉVENOT
title: Privilege Escalation in Google Cloud Platform
description: Privilege escalation techniques for Google Cloud Platform (GCP)
hide:
  - toc
---

# Privilege Escalation in Google Cloud Platform

| Permission | Resources |
| ---------- | --------- |
| `cloudbuilds.builds.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/cloudbuild.builds.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/working-as-intendedrce-to-iam-privilege-escalation-in-gcp)   |
| `cloudfunctions.functions.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/cloudfunctions.functions.create-call.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `cloudfunctions.functions.update` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/cloudfunctions.functions.update.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `cloudscheduler.jobs.create` | [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `composer.environments.get` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `compute.instances.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/compute.instances.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `dataflow.jobs.create` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `dataflow.jobs.update` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `dataproc.clusters.create` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `dataproc.clusters.create` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `dataproc.jobs.create` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `dataproc.jobs.update` | Blog Post [1](https://security.love/blog/gcp/2020/11/22/lateral-movement-and-privesc-in-GCP.html), [2](https://www.xmcyber.com/blog/new-privilege-escalation-techniques-are-compromising-your-google-cloud-platform/) |
| `deploymentmanager.deployments.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/deploymentmanager.deployments.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `iam.roles.update` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.roles.update.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `iam.serviceAccountKeys.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccountKeys.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `iam.serviceAccounts.getAccessToken` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.getAccessToken.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `iam.serviceAccounts.implicitDelegation` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.implicitDelegation.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `iam.serviceAccounts.signBlob` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.signBlob-accessToken.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `iam.serviceAccounts.signJwt` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/iam.serviceAccounts.signJWT.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `orgpolicy.policy.set` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/orgpolicy.policy.set.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-2/) |
| `run.services.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/run.services.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-1/) |
| `serviceusage.apiKeys.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/serviceusage.apiKeys.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-2/) |
| `serviceusage.apiKeys.list` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/serviceusage.apiKeys.list.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-2/) |
| `storage.hmacKeys.create` | [Script](https://github.com/RhinoSecurityLabs/GCP-IAM-Privilege-Escalation/blob/master/ExploitScripts/storage.hmacKeys.create.py) / [Blog Post](https://rhinosecuritylabs.com/gcp/privilege-escalation-google-cloud-platform-part-2/) |