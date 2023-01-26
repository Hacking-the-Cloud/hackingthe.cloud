---
author_name: Chris Moberly
title: GCP Privilege Escalation
description: Common privilege escalation techniques in GCP.
---

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

---

In this section, we'll talk about ways to potentially increase our privileges within the cloud environment itself.

### Organization-level IAM permissions

Most of the commands in this blog focus on obtaining project-level data. However, it's important to know that permissions can be set at the highest level of "Organization" as well. If you can enumerate this info, this will give you an idea of which accounts may have access across all of the projects inside an org.

The following commands will list the policies set at this level:

```
# First, get the numeric organization ID
$ gcloud organizations list

# Then, enumerate the policies
$ gcloud organizations get-iam-policy [ORG ID]
```

Permissions you see in this output will be applied to EVERY project. If you don't have access to any of the accounts listed, continue reading to the [Service Account Impersonation](#service-account-impersonation) section below.

### Bypassing access scopes

There's nothing worse than having access to a powerful service account but being limited by the access scopes of your current OAuth token. But fret not! Just the existence of that powerful account introduces risks which we might still be able to abuse.

#### Pop another box

It's possible that another box in the environment exists with less restrictive access scopes. If you can view the output of `gcloud compute instances list --quiet --format=json`, look for instances with either the specific scope you want or the `auth/cloud-platform` all-inclusive scope.

Also keep an eye out for instances that have the default service account assigned (`PROJECT_NUMBER-compute@developer.gserviceaccount.com`).

#### Find service account keys

Google states very clearly [**"Access scopes are not a security mechanism... they have no effect when making requests not authenticated through OAuth"**](https://cloud.google.com/compute/docs/access/service-accounts#accesscopesiam).

So, if we have a powerful service account but a limited OAuth token, we need to somehow authenticate to services without OAuth.

The easiest way to do this would be to stumble across a [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) stored on the instance. These are RSA private keys that can be used to authenticate to the Google Cloud API and request a new OAuth token with no scope limitations.

You can tell which service accounts, if any, have had key files exported for them. This will let you know whether or not it's even worth hunting for them, and possibly give you some hints on where to look. The command below will help.

```
$ for i in $(gcloud iam service-accounts list --format="table[no-heading](email)"); do
    echo Looking for keys for $i:
    gcloud iam service-accounts keys list --iam-account $i
done
```

These files are not stored on a Compute Instance by default, so you'd have to be lucky to encounter them. When a service account key file is exported from the GCP console, the default name for the file is [project-id]-[portion-of-key-id].json. So, if your project name is `test-project` then you can search the filesystem for `test-project*.json` looking for this key file.

The contents of the file look something like this:

```
{
"type": "service_account",
"project_id": "[PROJECT-ID]",
"private_key_id": "[KEY-ID]",
"private_key": "-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----\n",
"client_email": "[SERVICE-ACCOUNT-EMAIL]",
"client_id": "[CLIENT-ID]",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://accounts.google.com/o/oauth2/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/[SERVICE-ACCOUNT-EMAIL]"
}

```

Or, if generated from the CLI they will look like this:

```
{
"name": "projects/[PROJECT-ID]/serviceAccounts/[SERVICE-ACCOUNT-EMAIL]/keys/[KEY-ID]",
"privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE",
"privateKeyData": "[PRIVATE-KEY]",
"validAfterTime": "[DATE]",
"validBeforeTime": "[DATE]",
"keyAlgorithm": "KEY_ALG_RSA_2048"
}
```

If you do find one of these files, you can tell the `gcloud` command to re-authenticate with this service account. You can do this on the instance, or on any machine that has the tools installed.

```
$ gcloud auth activate-service-account --key-file [FILE]
```

You can now test your new OAuth token as follows:

```
$ TOKEN=`gcloud auth print-access-token`
$ curl https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=$TOKEN
```

You should see `https://www.googleapis.com/auth/cloud-platform` listed in the scopes, which means you are not limited by any instance-level access scopes. You now have full power to use all of your assigned IAM permissions.

#### Steal gcloud authorizations

It's quite possible that other users on the same box have been running `gcloud` commands using an account more powerful than your own. You'll need local root to do this.

First, find what `gcloud` config directories exist in users' home folders.

```
$ sudo find / -name "gcloud"
```

You can manually inspect the files inside, but these are generally the ones with the secrets:

- ~/.config/gcloud/credentials.db
- ~/.config/gcloud/legacy_credentials/[ACCOUNT]/adc.json
- ~/.config/gcloud/legacy_credentials/[ACCOUNT]/.boto
- ~/.credentials.json

Now, you have the option of looking for clear text credentials in these files or simply copying the entire `gcloud` folder to a machine you control and running `gcloud auth list` to see what accounts are now available to you.

### Service account impersonation

There are three ways in which you can [impersonate another service account](https://cloud.google.com/iam/docs/understanding-service-accounts#impersonating_a_service_account):

- Authentication using RSA private keys (covered [above](#find-service-account-keys))
- Authorization using Cloud IAM policies (covered below)
- Deploying jobs on GCP services (more applicable to the compromise of a user account)

It's possible that the service account you are currently authenticated as has permission to impersonate other accounts with more permissions and/or a less restrictive scope. This behavior is authorized by the predefined role called `iam.serviceAccountTokenCreator`.

A good example here is that you've compromised an instance running as a custom service account with this role, and the default service account still exists in the project. As the default service account has the primitive role of Project Editor, it is possibly even more powerful than the custom account.

Even better, you might find a service account with the primitive role of Owner. This gives you full permissions, and is a good target to then grant your own Google account rights to log in to the project using the web console.

`gcloud` has a `--impersonate-service-account` [flag](https://cloud.google.com/sdk/gcloud/reference/#--impersonate-service-account) which can be used with any command to execute in the context of that account.

To give this a shot, you can try the following:

```
# View available service accounts
$ gcloud iam service-accounts list

# Impersonate the account
$ gcloud compute instances list \
    --impersonate-service-account xxx@developer.gserviceaccount.com
```

### Exploring other projects

If you're really lucky, either the service account on your compromised instance or another account you've bagged thus far has access to additional GCP projects. You can check with the following command:

```
$ gcloud projects list
```

From here, you can hop over to that project and start the entire process over.

```
$ gcloud config set project [PROJECT-ID]
```

### Granting access to management console

Access to the [GCP management console](https://console.cloud.google.com/) is provided to user accounts, not service accounts. To log in to the web interface, you can grant access to a Google account that you control. This can be a generic "@gmail.com" account, it does not have to be a member of the target organization.

To grant the primitive role of Owner to a generic "@gmail.com" account, though, you'll need to use the web console. `gcloud` will error out if you try to grant it a permission above Editor.

You can use the following command to grant a user the primitive role of Editor to your existing project:

```
$ gcloud projects add-iam-policy-binding [PROJECT] \
    --member user:[EMAIL] --role roles/editor
```

If you succeeded here, try accessing the web interface and exploring from there.

This is the highest level you can assign using the gcloud tool. To assign a permission of Owner, you'd need to use the console itself.

You need a fairly high level of permission to do this. If you're not quite there, keep reading.

### Spreading to G Suite via domain-wide delegation of authority

[G Suite](https://gsuite.google.com/) is Google's collaboration and productivity platform which consists of things like Gmail, Google Calendar, Google Drive, Google Docs, etc. Many organizations use some or all of this platform as an alternative to traditional Microsoft AD/Exchange environments.

Service accounts in GCP can be granted the rights to programatically access user data in G Suite by impersonating legitimate users. This is known as [domain-wide delegation](https://developers.google.com/admin-sdk/reports/v1/guides/delegation). This includes actions like reading email in GMail, accessing Google Docs, and even creating new user accounts in the G Suite organization.

G Suite has [its own API](https://developers.google.com/gsuite/aspects/apis). Permissions are granted to G Suite API calls in a similar fashion to how permissions are granted to GCP APIs. However, G Suite and GCP are two different entities - being in one does not mean you automatically have access to another.

It is possible that a G Suite administrator has granted some level of G Suite API access to a GCP service account that you control. If you have access to the Web UI at this point, you can browse to IAM -> Service Accounts and see if any of the accounts have "Enabled" listed under the "domain-wide delegation" column. The column itself may not appear if no accounts are enabled. As of this writing, there is no way to do this programatically, although there is a [request for this feature](https://issuetracker.google.com/issues/116182848) in Google's bug tracker.

It is not enough for you to simply enable this for a service account inside GCP. The G Suite administrator would also have to configure this in the G Suite admin console.

Whether or not you know that a service account has been given permissions inside G Suite, you can still try it out. You'll need the service account credentials exported in JSON format. You may have acquired these in an earlier step, or you may have the access required now to create a key for a service account you know to have domain-wide delegation enabled.

This topic is a bit tricky... your service account has something called a "client_email" which you can see in the JSON credential file you export. It probably looks something like `account-name@project-name.iam.gserviceaccount.com`. If you try to access G Suite API calls directly with that email, even with delegation enabled, you will fail. This is because the G Suite directory will not include the GCP service account's email addresses. Instead, to interact with G Suite, we need to actually impersonate valid G Suite users.

What you really want to do is to impersonate a user with administrative access, and then use that access to do something like reset a password, disable multi-factor authentication, or just create yourself a shiny new admin account.

The GitLab Red Team created [this Python script](https://gitlab.com/gitlab-com/gl-security/gl-redteam/gcp_misc/blob/master/gcp_delegation.py) that can do two things - list the user directory and create a new administrative account. Here is how you would use it:

```
# Validate access only
$ ./gcp_delegation.py --keyfile ./credentials.json \
    --impersonate steve.admin@target-org.com \
    --domain target-org.com

# List the directory
$ ./gcp_delegation.py --keyfile ./credentials.json \
    --impersonate steve.admin@target-org.com \
    --domain target-org.com \
    --list

# Create a new admin account
$ ./gcp_delegation.py --keyfile ./credentials.json \
    --impersonate steve.admin@target-org.com \
    --domain target-org.com \
    --account pwned
```

You can try this script across a range of email addresses to impersonate various users. Standard output will indicate whether or not the service account has access to G Suite, and will include a random password for the new admin account if one is created.

If you have success creating a new admin account, you can log on to the [Google admin console](https://admin.google.com) and have full control over everything in G Suite for every user - email, docs, calendar, etc. Go wild.
