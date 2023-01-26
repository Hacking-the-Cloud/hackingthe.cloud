---
author_name: Chris Moberly
title: Security Concepts
description: Common security concepts in GCP.
---

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

---

What you can actually do from within a compromised instance is the resultant combination of service accounts, access scopes, and IAM permissions. These are described below.

## Resource hierarchy

Google Cloud uses a [Resource hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy) that is similar, conceptually, to that of a traditional filesystem. This provides a logical parent/child workflow with specfic attachment points for policies and permissions.

At a high level, it looks like this:

```
Organization
--> Folders
  --> Projects
    --> Resources
```

A virtual machine (called a Compute Instance) is a resource. This resource resides in a project, probably alongside other Compute Instances, storage buckets, etc.

## Service accounts

Virtual machine instances are usually assigned a service account. Every GCP project has a [default service account](https://cloud.google.com/compute/docs/access/service-accounts#default_service_account), and this will be assigned to new Compute Instances unless otherwise specified. Administrators can choose to use either a custom account or no account at all. This service account can be used by any user or application on the machine to communicate with the Google APIs. You can run the following command to see what accounts are available to you:

```
$ gcloud auth list
```

Default service accounts will look like one of the following:

```
PROJECT_NUMBER-compute@developer.gserviceaccount.com
PROJECT_ID@appspot.gserviceaccount.com
```

More savvy administrators will have configured a custom service account to use with the instance. This allows them to be more granular with permissions.

A custom service account will look like this:

```
SERVICE_ACCOUNT_NAME@PROJECT_NAME.iam.gserviceaccount.com
```

If `gcloud auth list` returns multiple accounts available, something interesting is going on. You should generally see only the service account. If there is more than one, you can cycle through each using `gcloud config set account [ACCOUNT]` while trying the various tasks in this blog.



!!! info

    If you are looking for ways to bypass access scopes checkout: [Bypassing access scopes](/gcp/exploitation/gcp-priv-esc/#bypassing-access-scopes)


The service account on a GCP Compute Instance will use OAuth to communicate with the Google Cloud APIs. When [access scopes](https://cloud.google.com/compute/docs/access/service-accounts#accesscopesiam) are used, the OAuth token that is generated for the instance will have a [scope](https://oauth.net/2/scope/) limitation included. This defines what API endpoints it can authenticate to. It does NOT define the actual permissions.

When using a custom service account, Google [recommends](https://cloud.google.com/compute/docs/access/service-accounts#service_account_permissions) that access scopes are not used and to rely totally on IAM. The web management portal actually enforces this, but access scopes can still be applied to instances using custom service accounts programatically.

There are three options when setting an access scope on a VM instance:
- Allow default access
- All full access to all cloud APIs
- Set access for each API

You can see what scopes are assigned by querying the metadata URL. Here is an example from a VM with "default" access assigned:

```
$ curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes \
    -H 'Metadata-Flavor:Google'

https://www.googleapis.com/auth/devstorage.read_only
https://www.googleapis.com/auth/logging.write
https://www.googleapis.com/auth/monitoring.write
https://www.googleapis.com/auth/servicecontrol
https://www.googleapis.com/auth/service.management.readonly
https://www.googleapis.com/auth/trace.append
```

The most interesting thing in the default scope is `devstorage.read_only`. This grants read access to all storage buckets in the project. This can be devastating, which of course is great for us as an attacker.

Here is what you'll see from an instance with no scope limitations:

```
$ curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes -H 'Metadata-Flavor:Google'
https://www.googleapis.com/auth/cloud-platform
```

This `cloud-platform` scope is what we are really hoping for, as it will allow us to authenticate to any API function and leverage the full power of our assigned IAM permissions. It is also Google's recommendation as it forces administrators to choose only necessary permissions, and not to rely on access scopes as a barrier to an API endpoint.

It is possible to encounter some conflicts when using both IAM and access scopes. For example, your service account may have the IAM role of `compute.instanceAdmin` but the instance you've breached has been crippled with the scope limitation of `https://www.googleapis.com/auth/compute.readonly`. This would prevent you from making any changes using the OAuth token that's automatically assigned to your instance.

## Identify and access management (IAM)

IAM permissions are used for fine-grained access control. There are [a lot](https://cloud.google.com/iam/docs/permissions-reference) of them. The permissions are bundled together using three types of [roles](https://cloud.google.com/iam/docs/understanding-roles):

- Primitive roles: Owner, Editor, and Viewer. These are the old-school way of doing things. The default service account in every project is assigned the Editor role. This is insecure and we love it.
- Predefined roles: These roles are managed by Google and are meant to be combinations of most-likely scenarios. One of our favorites is the `compute.instanceAdmin` role, as it allows for easy privilege escalation.
- Custom roles: This allows admins to group their own set of granular permissions.

Individual permissions are bundled together into a role. A role is connected to a member (user or service account) in what Google calls a [binding](https://cloud.google.com/iam/docs/reference/rest/v1/Policy#binding). Finally, this binding is applied at some level of the GCP hierarchy via a [policy](https://cloud.google.com/iam/docs/reference/rest/v1/Policy).

This policy determines what actions are allowed - it is the intersection between accounts, permissions, resources, and (optionally) conditions.

You can try the following command to specifically enumerate roles assigned to your service account project-wide in the current project:

```
$ PROJECT=$(curl http://metadata.google.internal/computeMetadata/v1/project/project-id \
    -H "Metadata-Flavor: Google" -s)
$ ACCOUNT=$(curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email \
    -H "Metadata-Flavor: Google" -s)
$ gcloud projects get-iam-policy $PROJECT  \
    --flatten="bindings[].members" \
    --format='table(bindings.role)' \
    --filter="bindings.members:$ACCOUNT"
```

Don't worry too much if you get denied access to the command above. It's still possible to work out what you can do simply by trying to do it.

More generally, you can shorten the command to the following to get an idea of the roles assigned project-wide to all members.

```
$ gcloud projects get-iam-policy [PROJECT-ID]
```

Or to see the IAM policy [assigned to a single Compute Instance](https://cloud.google.com/sdk/gcloud/reference/compute/instances/get-iam-policy) you can try the following.

```
$ gcloud compute instances get-iam-policy [INSTANCE] --zone [ZONE]
```

There are similar commands for various other APIs. Consult the documentation if you need one other than what is shown above.