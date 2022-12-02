---
author_name: Aloïs THÉVENOT
title: Enumerate Service Account Permissions
description: Brute force the permissions of a service account to see what you have access to.
---

Link to Tool: [GitHub](https://github.com/NicholasSpringer/thunder-ctf/blob/master/scripts/test-permissions.py)

On GCP it is possible to use the [`projects.testIamPermissions`](https://cloud.google.com/resource-manager/reference/rest/v1/projects/testIamPermissions) method to check the permissions that a caller has on the specified Project.

To enumerate permissions you will need either a service account key file or an access token as well as the project ID.

!!! info

    The project ID can be retrieved from the metadata endpoint at `/computeMetadata/v1/project/project-id`

The following script taken from the [ThunderCTF](https://github.com/NicholasSpringer/thunder-ctf/) repository can be used to enumerate permissions:

```python
from googleapiclient import discovery
import google.oauth2.service_account
from google.oauth2.credentials import Credentials
import os, sys
from permissions import permissions

if len(sys.argv) != 2:
    sys.exit("Usage python test-permissions <token | path_to_key_file>")

if os.getenv('GOOGLE_CLOUD_PROJECT'):
    PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
    print(PROJECT_ID)
else:
    sys.exit("Please set your GOOGLE_CLOUD_PROJECT environment variable via gcloud config set project [PROJECT_ID]")

if (os.path.exists(sys.argv[1])):
    print(f'JSON credential: {sys.argv[1]}')
    # Create credentials using service account key file
    credentials = google.oauth2.service_account.Credentials.from_service_account_file(sys.argv[1])
else:
    print(f'Access token: {sys.argv[1][0:4]}...{sys.argv[1][-4:]}')
    ACCESS_TOKEN = sys.argv[1]
    # Create credentials using access token
    credentials = Credentials(token=sys.argv[1])

# Split testable permissions list into lists of 100 items each
chunked_permissions = (
    [permissions[i * 100:(i + 1) * 100] for i in range((len(permissions)+99) // 100)])

# Build cloudresourcemanager REST API python object
crm_api = discovery.build('cloudresourcemanager',
                          'v1', credentials=credentials)

# For each list of 100 permissions, query the api to see if the service account has any of the permissions
given_permissions = []
for permissions_chunk in chunked_permissions:
    response = crm_api.projects().testIamPermissions(resource=PROJECT_ID, body={
        'permissions': permissions_chunk}).execute()
    # If the service account has any of the permissions, add them to the output list
    if 'permissions' in response:
        given_permissions.extend(response['permissions'])

print(given_permissions)
```

## Updating the list of permissions

The file containing the list of permissions needs to be created / updated before using the enumeration script.

The file `permissions.py` should look like this:

```python
permissions = [
  'accessapproval.requests.approve',
  ...
  'vpcaccess.operations.list'
]
```

The list of existing permissions can be obtained from the [IAM permissions reference](https://cloud.google.com/iam/docs/permissions-reference) page or from the [IAM Dataset](https://github.com/iann0036/iam-dataset/blob/main/gcp/permissions.json) powering [gcp.permissions.cloud](https://gcp.permissions.cloud/).