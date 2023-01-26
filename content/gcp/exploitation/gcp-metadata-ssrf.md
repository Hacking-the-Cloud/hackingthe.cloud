---
author_name: Chris Moberly
title: Steal an OAuth Token via SSRF
description: Using SSRF to steal OAuth Tokens from a GCP hosted VM.
hide:
  - toc
---

# Steal an OAuth Token via SSRF

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

---

If you've found an SSRF vulnerability on a server hosted in GCP, you can extract this OAuth token from the metadata server. If you're lucky, your target has not disabled the /v1beta metadata endpoint. Try this first by pointing your SSRF payload at:

```
http://metadata.google.internal/computeMetadata/v1beta/instance/service-accounts/default/token
```

However, most folks will have now disabled that old endpoint in favor of the more secure v1 endpoint, which requires a custom header to be set. If this is the case, you'll be redirected to /v1/ and given an HTTP 403 error. You'll need to find a way to set the header as decribed in the [metadata page](/gcp/general-knowledge/metadata_in_google_cloud_instances/).

The OAuth tokens available via the metadata server are short-lived, meaning they expire fairly quickly. This means you'll either need to work fast or get new tokens from the SSRF endpoint at regular intervals.

If you're looking to build your own HTTP requests to mimic gcloud commands, you can run any `gcloud` command with the `--log-http` parameter to view the raw API requests.
