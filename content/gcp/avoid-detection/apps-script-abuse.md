---
author_name: Taylor Smith
title: Apps Script project impersonation / Google Apps Script persistence
description: Google Workspace Apps Script projects create hidden GCP projects (sys-<...>) that can be impersonated by attackers. This technique enables stealthy persistence (service accounts, hidden compute, cryptomining) and can bypass common console inspections.
---

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    [Ghost in the Script: Impersonating Google App Script projects for stealthy persistence](https://www.exaforce.com/blogs/ghost-in-the-script) by [Bleon Proko](https://www.linkedin.com/in/bleon-proko/) and [Jakub Pavlik](https://www.linkedin.com/in/pavlikjakub/).
</div>


Google Apps Script is a low-code platform that allows users to automate and integrate Google Workspace applications. When an Apps Script is deployed, it automatically creates a corresponding Google Cloud Platform (GCP) Project within the user's organization. These projects are often hidden from the standard GCP console view, creating an opportunity for attackers to achieve stealthy persistence.

## The Vulnerability

Apps Script projects are created with a specific ID format: `sys-<26 numbers>`. These projects reside in a `system-gsuite/apps-script` folder and are not visible in the organization's project list in the GCP console, though they are visible via the `gcloud` CLI.

An attacker with the `resourcemanager.projects.create` permission can create a standard GCP project that mimics this naming convention. By placing this impersonated project inside the `apps-script` folder, it becomes hidden from the console view, just like a legitimate Apps Script project. This allows the attacker to host malicious resources undetected.

## Attack Vector 1: Malicious Resources

A common abuse is to deploy a high-performance instance for cryptomining within a hidden project. This requires linking the project to a billing account and enabling the necessary APIs.

1.  **Create a hidden project** with a name mimicking a legitimate function:
    ```bash
    gcloud projects create 'sys-22222222222222222222222222' --name "Exaforce Google Sheet Function" --folder-936086877446
    ```
2.  **Link the project to a billing account:**
    ```bash
    gcloud beta billing projects link sys-22222222222222222222222222-btlling-account xxxxxx
    ```
3.  **Create a large compute instance** for cryptomining:
    ```bash
    gcloud compute instances create app-script-instance project=sys-22222222222222222222222222 --zone=us-central1-a --machine-type=n2-standard-16 --image-family=debian-11 --image-project=deblan-cloud --boot-disk-size=200GB
    ```

## Attack Vector 2: Stealthy Persistence

Attackers can use a hidden project to create a service account and grant it highly privileged roles for long-term persistence. This identity is hard to discover because it is associated with a project that appears to be managed by Google.

1.  **Create a service account** inside the hidden project:
    ```bash
    gcloud iam service-accounts create persistence-service-account --display-name "Persistence Service Account" --project sys-22222222222222222222222222
    ```
2.  **Bind the service account** to a privileged role at the organization level:
    ```bash
    gcloud organizations add-iam-policy-binding xxxxxxx --member="serviceAccount:persistence-service-account@sys-222222222222.iam.gserviceaccount.com" --role="organizations/xxxxx/roles/AppScriptPolicy"
    ```

Notably, IAM service accounts are free resources, so this persistence mechanism can be established even without linking the project to a billing account, bypassing some detection methods.

-----

## Detection and Mitigation

### Detection Methods

1.  **Billing Information**: A legitimate Apps Script project will have `billingEnabled: false`. An impersonated project used for cryptomining will be linked to a billing account (`billingEnabled: true`). You can check this with the command: `acloud beta billing projects describe <project-id>`.

2.  **Enabled APIs**: A real Apps Script project has no services enabled by default. An attacker's manually created project will have a list of default APIs enabled. Compare a real vs. fake project with: `gcloud services list --enabled-project <project-id>`.

3.  **Audit Logs**: Query the `CreateProject` logs for the `apps-script` folder. A legitimate project's `principalEmail` will be `appsdev-apps-dev-script-auth@system.gserviceaccount.com`. An impersonated project will show the attacker's user email as the creator.

### Mitigation Strategy

You can prevent this attack by implementing a custom organization policy that denies the creation of projects with an ID matching the Apps Script format.

```yaml
name: >-

organizations/012345678912/customConstraints/custom.denyAppsScriptProjectImpersonation
resource_types: cloudresourcemanager.googleapis.com/Project
method_types:
  - CREATE
  - UPDATE
condition: 'resource.projectId.matches(''sys-[0-9]{26}'')'
action_type: DENY
display_name: Deny Apps Script Project Impersonation
description: ''
```

**Note:** This policy is effective but will also block the creation of legitimate Apps Script projects for all users in the organization.
