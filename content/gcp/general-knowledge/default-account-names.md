---
author_name: Moses Frost (@mosesrenegade)
title: Default Account Information
description: Default information on how accounts and service accounts exist in GCP
---

## Service Accounts

[Service accounts](https://cloud.google.com/iam/docs/service-accounts) are similar to Azure [Service Principals](https://docs.microsoft.com/en-us/azure/active-directory/develop/app-objects-and-service-principals). They can allow for programmatic access but also abuse. 

[Information on Service Accounts](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)

User-Created Service Account: `service-account-name@project-id.iam.gserviceaccount.com`

Using the format above, you can denote the following items:

- `service-account-name`: This will tell you potentially what services this is for: `Bigtable-sa` or `compute-sa`
- `project-id`: This will be the project identifier that the service account is for. You can set your `gcloud` configuration to this `project-id`. It will be numerical typically.

## Default Service Account filename permutations: 

* `serviceaccount.json`
* `service_account.json`
* `sa-private-key.json`
* `service-account-file.json`

## Application-Based Service Account:

- `project-id@appspot.gserviceaccount.com`: Ths would be `project-id` value for App Engine or anything leveraging App Engine.
- `project-number-compute@developer.gserviceaccount.com`: This service account is for Compute Engine where the `project-number-compute` will be: `project-id`-`compute`. I.E. `1234567-compute`.

## How to use Service Accounts

In a BASH (or equivalent) shell: `export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"`

