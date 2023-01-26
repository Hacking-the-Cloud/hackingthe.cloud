---
author_name: Chris Moberly
title: Client Credential Search Order
description: The order by which GCP client libraries search for credentials.
---

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

---

## Default service account token

The metadata server available to a given instance will provide any user/process on that instance with an OAuth token that is automatically used as the default credentials when communicating with Google APIs via the `gcloud` command.

You can retrieve and inspect the token with the following curl command:

```
$ curl "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token" \
    -H "Metadata-Flavor: Google"
```

Which will receive a response like the following:

```
{
      "access_token":"ya29.AHES6ZRN3-HlhAPya30GnW_bHSb_QtAS08i85nHq39HE3C2LTrCARA",
      "expires_in":3599,
      "token_type":"Bearer"
 }
```

This token is the combination of the service account and access scopes assigned to the Compute Instance. So, even though your service account may have every IAM privilege imaginable, this particular OAuth token might be limited in the APIs it can communicate with due to access scopes.

## Application default credentials

As an alternative to first pulling a token from the metadata server, Google also has a strategy called [Application Default Credentials](https://cloud.google.com/docs/authentication/production). When using one of Google's official GCP client libraries, the code will automatically go searching for credentials to use in a defined order.

The very first location it would check would be the [source code itself](https://cloud.google.com/docs/authentication/production#passing_the_path_to_the_service_account_key_in_code). Developers can choose to statically point to a service account key file.

The next is an environment variable called `GOOGLE_APPLICATION_CREDENTIALS`. This can be set to point to a service account key file. Look for the variable itself set in the context of a system account or for references to setting it in scripts and instance metadata.

Finally, if neither of these are provided, the application will revert to using the default token provided by the metadata server as described in the section above.

Finding the actual JSON file with the service account credentials is generally much more desirable than relying on the OAuth token on the metadata server. This is because the raw service account credentials can be activated without the burden of access scopes and without the short expiration period usually applied to the tokens.
