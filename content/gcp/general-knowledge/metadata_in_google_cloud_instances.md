---
author_name: Jan Slezak
title: Metadata in Google Cloud Instances
description: Information about the data an attacker can access via GCP's API endpoints
hide:
    - toc
---

Metadata can provide an attacker (or regular user) information about the compromised App Engine instance, such as its project ID, service accounts, and tokens used by those service accounts.  

The metadata can be accessed by a regular HTTP GET request or cURL, sans any third-party client libraries by making a request to metadata.google.internal or 169.254.169.254.  

```
curl "http://metadata.google.internal/computeMetadata/v1/?recursive=true&alt=text" -H
"Metadata-Flavor: Google"
```
_Note: If you are using your local terminal to attempt access, as opposed to Google's Web Console, you will need to add `169.254.169.254    metadata.google.internal` to your `/etc/hosts` file._

## Metadata Endpoints

For basic enumeration, an attacker can target. 
```
http://169.254.169.254/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/
http://metadata/computeMetadata/v1/
http://metadata.google.internal/computeMetadata/v1/instance/hostname
http://metadata.google.internal/computeMetadata/v1/instance/id
http://metadata.google.internal/computeMetadata/v1/project/project-id
```
To view scope:
```
http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes -H "Metadata-Flavor: Google"
```
To view project metadata:
```
curl "http://metadata.google.internal/computeMetadata/v1/project/attributes/?recursive=true&alt=text" \
    -H "Metadata-Flavor: Google"
```
To view instance metadata:
```
curl "http://metadata.google.internal/computeMetadata/v1/instance/attributes/?recursive=true&alt=text" \
    -H "Metadata-Flavor: Google"
```

The following table is pulled from the [Google Cloud Documentation](https://cloud.google.com/appengine/docs/standard/java/accessing-instance-metadata)

| Metadata Endpoint      | Description |
| ----------- | ----------- |
| `/computeMetadata/v1/project/numeric-project-id`      | The project number assigned to your project.      |
| `/computeMetadata/v1/project/project-id`   | The project ID assigned to your project.        |
| `/computeMetadata/v1/instance/zone`  |	The zone the instance is running in.|
| `/computeMetadata/v1/instance/service-accounts/default/aliases`	  | |
| `/computeMetadata/v1/instance/service-accounts/default/email` |	The default service account email assigned to your project.  |
| `/computeMetadata/v1/instance/service-accounts/default/`       |	Lists all the default service accounts for your project.|
| `/computeMetadata/v1/instance/service-accounts/default/scopes` |	Lists all the supported scopes for the default service accounts.|
| `/computeMetadata/v1/instance/service-accounts/default/token` | Returns the auth token that can be used to authenticate your application to other Google Cloud APIs.|
