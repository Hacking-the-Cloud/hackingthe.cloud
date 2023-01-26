---
author_name: Chris Moberly
title: Google Cloud CLI
description: Google Cloud CLI used to create and manage Google Cloud resources. 
hide:
  - toc
---

# Google Cloud CLI

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/#gcloud)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

It is likely that the box you land on will have the GCP SDK tools installed and configured. A quick way to verify that things are set up is to run the following command:

```
gcloud config list
```

If properly configured, you should get some output detailing the current service account and project in use.

The [gcloud command set](https://cloud.google.com/sdk/gcloud/reference/) is pretty extensive, supports tab completion, and has excellent online and built-in documentation. You can also install it locally on your own machine and use it with credential data that you obtain.
Cloud APIs

The gcloud command is really just a way of automating [Google Cloud API calls](https://cloud.google.com/apis/docs/overview). However, you can also perform them manually. Understanding the API endpoints and functionality can be very helpful when you're operating with a very specific set of permissions, and trying to work out exactly what you can do.

You can see what the raw HTTP API call for any individual `gcloud` command is simply by appending `--log-http` to the command.  