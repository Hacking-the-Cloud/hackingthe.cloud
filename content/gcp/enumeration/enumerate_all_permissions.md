---
author_name: Scott Weston (@WebbinRoot)
title: Enumerate Org/Folder/Project Permissions + Individual Resource Permissions
description: Brute force the permissions of all resources above to see what permissions you have. Includes example of brute forcing ~9500 permissions at the end. Also introduces tool that passively collections permissions allowed as run (gcpwn)
---

<div class="grid cards" markdown>
-   :material-tools:{ .lg .middle } __Tools mentioned in this article__

    ---

    [gcpwn](https://github.com/NetSPI/gcpwn)
</div>

## What is testIamPermissions?

GCP offers a "testIamPermissions" API call on most resources that support policies. This includes resources like:

- Organizations
- Folders
- Projects
- Compute Instances
- Cloud Functions

In MOST cases, the general psuedo-code is the same regardless of the resource. However, the permissions allowed are usually dependent on the resource. 

For example, for **"Projects"** (probably 99% of people's interest), testIamPermissions is documented [here](https://cloud.google.com/resource-manager/reference/rest/v1/projects/testIamPermissions). Note the general pattern is passing in an array (or list) of individual permissions and the service will return the list of permissions the caller is allowed **in that specific project**. So in the example below, we pass in a large number of permissions and maybe just "cloudfunctions.functions.list" is returned indicating our caller has that permission within this project (aka, can list all cloud functions in this project).

```
# Input
{
  "permissions": [
    compute.instances.addAccessConfig
    cloudfunctions.functions.list
    etc
  ]
}

# Output
{
  "permissions": [
     cloudfunctions.functions.list
  ]
}
```

However, testIamPermissions does NOT just exist for projects. The compute service allows you to specify permissions at the compute instance level (as opposed to the project level). As such, testIamPermissions actually exists for instances as well shown in the documentation [here](https://cloud.google.com/compute/docs/reference/rest/v1/instances/testIamPermissions). You'll notice the API call is pretty much the same as the projects API call in that it takes in a big list of permission and returns the list of permissions the caller has on THAT specific instance; we are just calling testIamPermissions on the **instance** as opposed to the **project**. Also note we could not pass in "cloudfunctions.functions.list", for example, to the instances testIamPermissions as it will only accept instance-level permissions.

```
# Input
{
  "permissions": [
                'compute.instances.addAccessConfig',
                'compute.instances.addMaintenancePolicies',
                'compute.instances.addResourcePolicies',
                'compute.instances.attachDisk',
                'compute.instances.createTagBinding',
                'compute.instances.delete',
                'compute.instances.deleteAccessConfig',
                'compute.instances.deleteTagBinding',
                'compute.instances.detachDisk',
                'compute.instances.get',
                'compute.instances.getEffectiveFirewalls',
                'compute.instances.getGuestAttributes',
                'compute.instances.getIamPolicy',
                'compute.instances.getScreenshot',
                'compute.instances.getSerialPortOutput',
                'compute.instances.getShieldedInstanceIdentity',
                'compute.instances.getShieldedVmIdentity',
                'compute.instances.listEffectiveTags',
                'compute.instances.listReferrers',
                'compute.instances.listTagBindings',
                'compute.instances.osAdminLogin',
                'compute.instances.osLogin',
                'compute.instances.removeMaintenancePolicies',
                'compute.instances.removeResourcePolicies',
                'compute.instances.reset',
                'compute.instances.resume',
                'compute.instances.sendDiagnosticInterrupt',
                'compute.instances.setDeletionProtection',
                'compute.instances.setDiskAutoDelete',
                'compute.instances.setIamPolicy',
                'compute.instances.setLabels',
                'compute.instances.setMachineResources',
                'compute.instances.setMachineType',
                'compute.instances.setMetadata',
                'compute.instances.setMinCpuPlatform',
                'compute.instances.setName',
                'compute.instances.setScheduling',
                'compute.instances.setSecurityPolicy',
                'compute.instances.setServiceAccount',
                'compute.instances.setShieldedInstanceIntegrityPolicy',
                'compute.instances.setShieldedVmIntegrityPolicy',
                'compute.instances.setTags',
                'compute.instances.simulateMaintenanceEvent',
                'compute.instances.start',
                'compute.instances.startWithEncryptionKey',
                'compute.instances.stop',
                'compute.instances.suspend',
                'compute.instances.update',
                'compute.instances.updateAccessConfig',
                'compute.instances.updateDisplayDevice',
                'compute.instances.updateNetworkInterface',
                'compute.instances.updateSecurity',
                'compute.instances.updateShieldedInstanceConfig',
                'compute.instances.updateShieldedVmConfig',
                'compute.instances.use',
                'compute.instances.useReadOnly'
  ]
}

# Output
{
  "permissions": [
                'compute.instances.start',
                'compute.instances.startWithEncryptionKey',
                'compute.instances.stop',
  ]
}
```

## GCPwn Introduction

[gcpwn](https://github.com/NetSPI/gcpwn/tree/main) is a tool that will run testIamPermission on all resources identified if specified by the end user. This means it will cover testIamPermission test cases for organizations, projects, folders, compute instances, cloud functions, cloud storage (buckets), service accounts, etc. For orgs/projects/folders it runs a small list of permissions as the input but you can specify through flags to brute force **~9500 permissions**.

To install the tool, follow the installation instructions [here](https://github.com/NetSPI/gcpwn/wiki). Once installed, review the ["Common Use Cases"](https://github.com/NetSPI/gcpwn/wiki/4.-Common-Use-Cases-(Bruteforcing-9500-Permissions)) which covers both of the items above.

To see a live demo, you can watch [this](https://www.youtube.com/watch?v=opvv9h3Qe0s) which covers testIamPermissions briefly.

!!! Note
    The tool will also passively record all API permissions you were able to call regardless if testIamPermissions is used, testIamPermissions just will give you more permissions back usually.

## Enumerate Permissions on Individual Resources

Each enumeration  module (ex. `enum_instances`) in the tool allows you to pass in an `--iam` flag that will call testIamPermissions on the resource while enumerating it. Once run, you can run `creds info` as shown below and this will list out all the permissions your caller has. Review the POC below.

1. Show the value for the service account key. Note the  same technique can be used for application default credentials (username/password) as well as standalone Oauth2 tokens
2. Start up the tool via `python3 main.py`. Load in the service account credentials for the file we just showed.
3. Now that the credentials are loaded in and the project is set (Note if project is `Unknown` you can set it with `projects set <project_id>`), run `creds info` and note that NO permissions are known for the current user
4. Run enum_instances and see an instance is found. Run `creds info` again and note that permission are now populated saying the user has `compute.instances.list` on the project and `compute.instances.get` on the instance itself.
5. Run enum_instances again **but now include testIamPermission calls** with the `--iam` flag. Run `creds info` again and note way more permissions were identified for the specified compute instance as gcpwn ran testIamPermissions during the enumeration phaes and saved the results. Now we can see our caller has not just `compute.instances.get` but `compute.instances.addAccessConfig`, `compute.instances.addMaintenancePolicies`, `compute.instances.addResourcePolicies`, etc. on `instance-20240630-025631`
6. This is hard to read. So you can pass in `--csv` with `creds info` to export it to an easy to read Excel file. creds info will highlight "dangerous" permissions red and the resulting CSV has a column for True/False for dangerous permissions.

```
┌──(kali㉿kali)-[~/gcpwn]
└─$ cat key.json
{
  "type": "service_account",
  "project_id": "production-project[TRUNCATED]",
  "private_key_id": "2912[TRUNCATED]",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0B[RECACTED]\n-----END PRIVATE KEY-----\n",
  "client_email": "newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com",
  "client_id": "11[TRUNCATED]",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/newserviceaccount%40production-project[TRUNCATED].iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

┌──(kali㉿kali)-[~/gcpwn]
└─$ python3 main.py 
[*] No workspaces were detected. Please provide the name for your first workspace below.
> New workspace name: DemoWorkspace
[*] Workspace 'DemoWorkspace' created.

[TRUNCATED]

[*] Listing existing credentials...


Submit the name or index of an existing credential from above, or add NEW credentials via Application Default 
Credentails (adc - google.auth.default()), a file pointing to adc credentials, a standalone OAuth2 Token, 
or Service credentials. See wiki for details on each. To proceed with no credentials just hit ENTER and submit 
an empty string. 
[1] *adc      <credential_name> [tokeninfo]                    (ex. adc mydefaultcreds [tokeninfo]) 
[2] *adc-file <credential_name> <filepath> [tokeninfo]         (ex. adc-file mydefaultcreds /tmp/name2.json)
[3] *oauth2   <credential_name> <token_value> [tokeninfo]      (ex. oauth2 mydefaultcreds ya[TRUNCATED]i3jJK)  
[4] service   <credential_name> <filepath_to_service_creds>    (ex. service mydefaultcreds /tmp/name2.json)

*To get scope and/or email info for Oauth2 tokens (options 1-3) include a third argument of 
"tokeninfo" to send the tokens to Google's official oauth2 endpoint to get back scope. 
tokeninfo will set the credential name for oauth2, otherwise credential name will be used.
Advised for best results. See https://cloud.google.com/docs/authentication/token-types#access-contents.
Using tokeninfo will add scope/email to your references if not auto-picked up.

Input: service service_user /home/kali/gcpwn/key.json
[*] Credentials successfuly added
Loading in Service Credentials...
[*] Loaded credentials service_user
(production-project[TRUNCATED]:service_user)> creds info

Summary for service_user:
Email: newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com
Scopes:
    - N/A
Default Project: production-project[TRUNCATED]
All Projects:

Access Token: N/A
(production-project[TRUNCATED]:service_user)> modules run enum_instances
[*] Checking production-project[TRUNCATED] for instances...
[**] Reviewing instance-20240630-025631
[***] GET Instance
[SUMMARY] GCPwn found 1 Instances in production-project[TRUNCATED]
   - zones/us-central1-c                                                                                                                                                                    
     - instance-20240630-025631                                                                                                                                                             
(production-project[TRUNCATED]:service_user)> creds info

Summary for service_user:
Email: newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com
Scopes:
    - N/A
Default Project: production-project[TRUNCATED]
All Projects:

Access Token: N/A

[******] Permission Summary for service_user [******]
- Project Permissions
  - production-project[TRUNCATED]
    - compute.instances.list
- Compute Actions Allowed Permissions
  - production-project[TRUNCATED]
    - compute.instances.get
      - instance-20240630-025631 (instances)

(production-project[TRUNCATED]:service_user)> modules run enum_instances --iam
[*] Checking production-project[TRUNCATED] for instances...
[**] Reviewing instance-20240630-025631
[***] GET Instance
[***] TEST Instance Permissions
[SUMMARY] GCPwn found 1 Instances in production-project[TRUNCATED]
   - zones/us-central1-c                                                                                                                                                                    
     - instance-20240630-025631                                                                                                                                                             
(production-project[TRUNCATED]:service_user)> creds info

Summary for service_user:
Email: newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com
Scopes:
    - N/A
Default Project: production-project[TRUNCATED]
All Projects:

Access Token: N/A

[******] Permission Summary for service_user [******]
- Project Permissions
  - production-project[TRUNCATED]
    - compute.instances.list
- Compute Actions Allowed Permissions
  - production-project[TRUNCATED]
    - compute.instances.get
      - instance-20240630-025631 (instances)
    - compute.instances.addAccessConfig
      - instance-20240630-025631 (instances)
    - compute.instances.addMaintenancePolicies
      - instance-20240630-025631 (instances)
    - compute.instances.addResourcePolicies
      - instance-20240630-025631 (instances)
    - compute.instances.attachDisk
      - instance-20240630-025631 (instances)
    - compute.instances.createTagBinding
      - instance-20240630-025631 (instances)
    - compute.instances.delete
      - instance-20240630-025631 (instances)
    - compute.instances.deleteAccessConfig
      - instance-20240630-025631 (instances)
    - compute.instances.deleteTagBinding
      - instance-20240630-025631 (instances)
    - compute.instances.detachDisk
      - instance-20240630-025631 (instances)
    - compute.instances.getEffectiveFirewalls
      - instance-20240630-025631 (instances)
    - compute.instances.getGuestAttributes
      - instance-20240630-025631 (instances)
    - compute.instances.getIamPolicy
      - instance-20240630-025631 (instances)
    - compute.instances.getScreenshot
      - instance-20240630-025631 (instances)
    - compute.instances.getSerialPortOutput
      - instance-20240630-025631 (instances)
    - compute.instances.getShieldedInstanceIdentity
      - instance-20240630-025631 (instances)
    - compute.instances.getShieldedVmIdentity
      - instance-20240630-025631 (instances)
    - compute.instances.listEffectiveTags
      - instance-20240630-025631 (instances)
    - compute.instances.listReferrers
      - instance-20240630-025631 (instances)
    - compute.instances.listTagBindings
      - instance-20240630-025631 (instances)
    - compute.instances.osAdminLogin
      - instance-20240630-025631 (instances)
    - compute.instances.osLogin
      - instance-20240630-025631 (instances)
    - compute.instances.removeMaintenancePolicies
      - instance-20240630-025631 (instances)
    - compute.instances.removeResourcePolicies
      - instance-20240630-025631 (instances)
    - compute.instances.reset
      - instance-20240630-025631 (instances)
    - compute.instances.resume
      - instance-20240630-025631 (instances)
    - compute.instances.sendDiagnosticInterrupt
      - instance-20240630-025631 (instances)
    - compute.instances.setDeletionProtection
      - instance-20240630-025631 (instances)
    - compute.instances.setDiskAutoDelete
      - instance-20240630-025631 (instances)
    - compute.instances.setIamPolicy
      - instance-20240630-025631 (instances)
    - compute.instances.setLabels
      - instance-20240630-025631 (instances)
    - compute.instances.setMachineResources
      - instance-20240630-025631 (instances)
    - compute.instances.setMachineType
      - instance-20240630-025631 (instances)
    - compute.instances.setMetadata
      - instance-20240630-025631 (instances)
    - compute.instances.setMinCpuPlatform
      - instance-20240630-025631 (instances)
    - compute.instances.setName
      - instance-20240630-025631 (instances)
    - compute.instances.setScheduling
      - instance-20240630-025631 (instances)
    - compute.instances.setSecurityPolicy
      - instance-20240630-025631 (instances)
    - compute.instances.setServiceAccount
      - instance-20240630-025631 (instances)
    - compute.instances.setShieldedInstanceIntegrityPolicy
      - instance-20240630-025631 (instances)
    - compute.instances.setShieldedVmIntegrityPolicy
      - instance-20240630-025631 (instances)
    - compute.instances.setTags
      - instance-20240630-025631 (instances)
    - compute.instances.simulateMaintenanceEvent
      - instance-20240630-025631 (instances)
    - compute.instances.start
      - instance-20240630-025631 (instances)
    - compute.instances.startWithEncryptionKey
      - instance-20240630-025631 (instances)
    - compute.instances.stop
      - instance-20240630-025631 (instances)
    - compute.instances.suspend
      - instance-20240630-025631 (instances)
    - compute.instances.update
      - instance-20240630-025631 (instances)
    - compute.instances.updateAccessConfig
      - instance-20240630-025631 (instances)
    - compute.instances.updateDisplayDevice
      - instance-20240630-025631 (instances)
    - compute.instances.updateNetworkInterface
      - instance-20240630-025631 (instances)
    - compute.instances.updateSecurity
      - instance-20240630-025631 (instances)
    - compute.instances.updateShieldedInstanceConfig
      - instance-20240630-025631 (instances)
    - compute.instances.updateShieldedVmConfig
      - instance-20240630-025631 (instances)
    - compute.instances.use
      - instance-20240630-025631 (instances)
    - compute.instances.useReadOnly
      - instance-20240630-025631 (instances)

(production-project[TRUNCATED]:service_user)> creds info --csv
^C

┌──(kali㉿kali)-[~/gcpwn]
└─$ cd GatheredData/1_demoworkspace/Reports/Snapshots/    
                                                                                                                                                                                            
┌──(kali㉿kali)-[~/…/GatheredData/1_demoworkspace/Reports/Snapshots]
└─$ ls
Permission_Summary_service_user_20240714161752.csv  service_user_1720988272.6552665.csv
                                                                                                                                                                                            
┌──(kali㉿kali)-[~/…/GatheredData/1_demoworkspace/Reports/Snapshots]
└─$ cat Permission_Summary_service_user_20240714161752.csv 
Credname,Permission,Asset Type,Asset Name,Project_ID,Flagged
service_user,compute.instances.list,Project,production-project[TRUNCATED],production-project[TRUNCATED],False
service_user,compute.instances.get,instances,instance-20240630-025631,production-project[TRUNCATED],False
service_user,compute.instances.addAccessConfig,instances,instance-20240630-025631,production-project[TRUNCATED],False
service_user,compute.instances.addMaintenancePolicies,instances,instance-20240630-025631,production-project[TRUNCATED],False
service_user,compute.instances.addResourcePolicies,instances,instance-20240630-025631,production-project[TRUNCATED],False
service_user,compute.instances.attachDisk,instances,instance-20240630-025631,production-project[TRUNCATED],False
```

As mentiond before, each individual service can have testIamPermission so each enum module can have testIamPermissions. This would kinda stink if you had to run them individually so added an `enum_all` module which calls ALL enumeration modules. You can pass in `--iam` to `enum_all` to run all possible testIamPermissions

```
└─$ python3 main.py 
[*] Found existing sessions:
  [0] New session
  [1] DemoWorkspace
  [2] exit
Choose an option: 1
[TRUNCATED]

Welcome to your workspace! Type 'help' or '?' to see available commands.

[*] Listing existing credentials...
  [1] service_user (service) - newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com


Submit the name or index of an existing credential from above, or add NEW credentials via Application Default 
Credentails (adc - google.auth.default()), a file pointing to adc credentials, a standalone OAuth2 Token, 
or Service credentials. See wiki for details on each. To proceed with no credentials just hit ENTER and submit 
an empty string. 
[1] *adc      <credential_name> [tokeninfo]                    (ex. adc mydefaultcreds [tokeninfo]) 
[2] *adc-file <credential_name> <filepath> [tokeninfo]         (ex. adc-file mydefaultcreds /tmp/name2.json)
[3] *oauth2   <credential_name> <token_value> [tokeninfo]      (ex. oauth2 mydefaultcreds ya[TRUNCATED]i3jJK)  
[4] service   <credential_name> <filepath_to_service_creds>    (ex. service mydefaultcreds /tmp/name2.json)

*To get scope and/or email info for Oauth2 tokens (options 1-3) include a third argument of 
"tokeninfo" to send the tokens to Google's official oauth2 endpoint to get back scope. 
tokeninfo will set the credential name for oauth2, otherwise credential name will be used.
Advised for best results. See https://cloud.google.com/docs/authentication/token-types#access-contents.
Using tokeninfo will add scope/email to your references if not auto-picked up.

Input: 1
Loading in Service Credentials...
[*] Loaded credentials service_user
(production-project[TRUNCATED]:service_user)> modules run enum_all --iam 
[***********] Beginning enumeration for production-project[TRUNCATED] [***********]
[*] Beginning Enumeration of RESOURCE MANAGER Resources...
[*] Searching Organizations
[*] Searching All Projects
[*] Searching All Folders
[*] Getting remainting projects/folders via recursive folder/project list calls starting with org node if possible
[*] NOTE: This might take a while depending on the size of the domain
[SUMMARY] GCPwn found or retrieved NO Organization(s)
[SUMMARY] GCPwn found or retrieved NO Folder(s)
[SUMMARY] GCPwn found 1 Project(s)
   - projects/[TRUNCATED] (Production Project 1) - ACTIVE                                                                                                           
[*] Beginning Enumeration of CLOUD COMPUTE Resources...
[*] Checking production-project[TRUNCATED] for instances...
[**] Reviewing instance-20240630-025631
[***] GET Instance
[***] TEST Instance Permissions
[SUMMARY] GCPwn found 1 Instances in production-project[TRUNCATED]
   - zones/us-central1-c                                                                                                                                            
     - instance-20240630-025631                                                                                                                                     
[*] Checking Cloud Compute Project production-project[TRUNCATED]...
[*] Only first few metadata characters shown, run `data tables cloudcompute-projects --columns project_id,common_instance_metadata` to see all of metadata. Use --csv to export it to a csv.
[SUMMARY] GCPwn found 1 Compute Project(s) potentially with metadata
   - production-project[TRUNCATED]                                                                                                                                                            
[*] Beginning Enumeration of CLOUD FUNCTION Resources...
[*] Checking production-project[TRUNCATED] for functions...
[**] Reviewing projects/production-project[TRUNCATED]/locations/us-central1/functions/function-12
[***] GET Individual Function
[***] TEST Function Permissions
[SUMMARY] GCPwn found 1 Function(s) in production-project[TRUNCATED]
   - [us-central1] function-12                                                                                                                                                              
[*] Beginning Enumeration of CLOUD STORAGE Resources...
[*] Checking production-project[TRUNCATED] for HMAC keys...
[SUMMARY] GCPwn found 1 HMAC Key(s) in production-project[TRUNCATED]
   - [production-project[TRUNCATED]] GOOG1EV[TRUNCATED] - ACTIVE                                                                                   
     SA: [TRUNCATED]-compute@developer.gserviceaccount.com                                                                                                                                 
[*] Checking production-project[TRUNCATED] for buckets/blobs via LIST buckets...
[**] Reviewing bucket-to-see-how-much-stuff-121212121212
[***] GET Bucket Object
[X] 403 The user does not have storage.buckets.get permissions on bucket bucket-to-see-how-much-stuff-121212121212
[***] TEST Bucket Permissions
[***] LIST Bucket Blobs
[X] 403: The user does not have storage.objects.list permissions on
[**] Reviewing gcf-v2-sources-[TRUNCATED]-us-central1
[***] GET Bucket Object
[***] TEST Bucket Permissions
[***] LIST Bucket Blobs
[***] GET Bucket Blobs
[**] Reviewing gcf-v2-uploads-[TRUNCATED]-us-central1
[***] GET Bucket Object
[***] TEST Bucket Permissions
[***] LIST Bucket Blobs
[**] Reviewing testweoajrpjqfpweqjfpwejfwef
[***] GET Bucket Object
[***] TEST Bucket Permissions
[***] LIST Bucket Blobs
[SUMMARY] GCPwn found 4 Buckets (with up to 10 blobs shown each) in production-project[TRUNCATED]
   - bucket-[TRUNCATED]                                                                                                                    
   - gcf-[TRUNCATED]                                                                                                                      
     - function-12/function-source.zip                                                                                                                              
   - gcf-[TRUNCATED]                                                                                                                       
   - test[TRUNCATED]                                                                                                                                 
[*] Beginning Enumeration of SECRETS MANAGER Resources...
[**] [production-project[TRUNCATED]] Reviewing projects/[TRUNCATED]/secrets/test
[***] GET Base Secret Entity
[***] TEST Secret Permissions
[***] LIST Secret Versions
[****] GET Secret Version 2
[****] TEST Secret Version Permissions
[****] GETTING Secret Values For 2
[****] SECRET VALUE RETRIEVED FOR 2
[****] GET Secret Version 1
[****] TEST Secret Version Permissions
[****] GETTING Secret Values For 1
[****] SECRET VALUE RETRIEVED FOR 1
[**] [production-project[TRUNCATED]] Reviewing projects/[TRUNCATED]/secrets/test-location
[***] GET Base Secret Entity
[***] TEST Secret Permissions
[***] LIST Secret Versions
[****] GET Secret Version 1
[****] TEST Secret Version Permissions
[****] GETTING Secret Values For 1
[****] SECRET VALUE RETRIEVED FOR 1
[SUMMARY] GCPwn found 2 Secrets in production-project[TRUNCATED]
   - test                                                                                                                                                           
     - 1: test121212                                                                                                                                                
     - 2: test                                                                                                                                                      
   - test-location                                                                                                                                                  
     - 1: test121212                                                                                                                                                
[*] Beginning Enumeration of IAM Resources...
[*] Checking production-project[TRUNCATED] for service accounts...
[SUMMARY] GCPwn found 3 Service Account(s) in production-project[TRUNCATED]
   - [TRUNCATED]-compute@developer.gserviceaccount.com                                                                                                             
   - newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com                                                                                        
   - production-project[TRUNCATED]@appspot.gserviceaccount.com                                                                                                      
[*] Checking production-project[TRUNCATED] for roles...
[SUMMARY] GCPwn found or retrieved NO Custom Role(s)
[*] Checking IAM Policy for Organizations...
[*] Checking IAM Policy for Folders...
[*] Checking IAM Policy for Projects...
[*] Checking IAM Policy for Buckets...
[X] 403: The user does not have storage.buckets.getIamPolicy permissions
[*] Checking IAM Policy for CloudFunctions...
[*] Checking IAM Policy for Compute Instances...
[*] Checking IAM Policy for Service Accounts...
[*] Checking IAM Policy for Secrets...
[***********] Ending enumeration for production-project[TRUNCATED] [***********]

(production-project[TRUNCATED]:service_user)> creds info

Summary for service_user:
Email: newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com
Scopes:
    - N/A
Default Project: production-project[TRUNCATED]
All Projects:
    - production-project[TRUNCATED]

Access Token: N/A

[******] Permission Summary for service_user [******]
- Project Permissions
  - production-project[TRUNCATED]
    - cloudfunctions.functions.call
    - cloudfunctions.functions.create
    - cloudfunctions.functions.list
    - cloudfunctions.functions.setIamPolicy
    - cloudfunctions.functions.sourceCodeSet
    - cloudfunctions.functions.update
    - compute.disks.create
    - compute.instances.create
    - compute.instances.list
    - compute.instances.setMetadata
    - compute.instances.setServiceAccount
    - compute.projects.get
    - compute.subnetworks.use
    - compute.subnetworks.useExternalIp
    - deploymentmanager.deployments.create
    - iam.roles.update
    - iam.serviceAccountKeys.create
    - iam.serviceAccounts.actAs
    [TRUNCATED]
- Storage Actions Allowed Permissions
  - production-project[TRUNCATED]
    - storage.buckets.delete
      - bucket[TRUNCATED] (buckets)
      - gcf-v2-[TRUNCATED] (buckets)
      - gcf-v2-[TRUNCATED] (buckets)
      - test[TRUNCATED] (buckets)
    - storage.buckets.get
      - gcf-v2-[TRUNCATED] (buckets)
      - gcf-v2-[TRUNCATED] (buckets)
      - testw[TRUNCATED] (buckets)
    - storage.buckets.getIamPolicy
      - gcf-v2-[TRUNCATED] (buckets)
      - gcf-v2-[TRUNCATED] (buckets)
      - testw[TRUNCATED] (buckets)
    - storage.buckets.setIamPolicy
      - gcf-v2-[TRUNCATED] (buckets)
      - gcf-v2-[TRUNCATED] (buckets)
      - testw[TRUNCATED] (buckets)
     [TRUNCATED]
- Secret Actions Allowed Permissions
  - production-project[TRUNCATED]
    - secretmanager.secrets.get
      - test (secrets)
      - test-location (secrets)
    - secretmanager.secrets.delete
      - test (secrets)
      - test-location (secrets)
    - secretmanager.secrets.getIamPolicy
      - test (secrets)
      - test-location (secrets)
    - secretmanager.secrets.setIamPolicy
      - test (secrets)
      - test-location (secrets)
    - secretmanager.secrets.update
      - test (secrets)
      - test-location (secrets)
    - secretmanager.versions.get
      - test (Version: 1) (secret version)
      - test (Version: 2) (secret version)
      - test-location (Version: 1) (secret version)
    - secretmanager.versions.access
      - test (Version: 1) (secret version)
      - test (Version: 2) (secret version)
      - test-location (Version: 1) (secret version)
    - secretmanager.versions.destroy
      - test (Version: 1) (secret version)
      - test (Version: 2) (secret version)
      - test-location (Version: 1) (secret version)
    - secretmanager.versions.disable
      - test (Version: 1) (secret version)
      - test (Version: 2) (secret version)
      - test-location (Version: 1) (secret version)
    - secretmanager.versions.enable
      - test (Version: 1) (secret version)
      - test (Version: 2) (secret version)
      - test-location (Version: 1) (secret version)
```

## Enumerate ~9500 Permission on Org/Folder/Project

gcpwn includes a special flag for `enum_resources` called `--all-permissions`. When this is used with the `--iam` flag, gcpwn will attempt ~9500 individual permissions via testIamPermissions. This effectively should tell you every permission the user has in the current resource. Note you can find the list of permissions via the repository. For example, here are all the project permissions it [tries](https://github.com/NetSPI/gcpwn/blob/main/Modules/ResourceManager/utils/all_project_permissions.txt). **NOTE AGAIN TESTIAMPERMISSIONS IS NOT ACTUALLY ACTIVELY INVOKING THESE APIS**. Thus it should be safe to run these all through testIamPermissions. While not shown below you can pass `--all-permissions` and `--iam` into `enum_all` if you want to do this as part of the everything enumeration.

```
(production-project[TRUNCATED]:service_user)> modules run enum_resources --iam --all-permissions
[*] Searching Organizations
[*] Searching All Projects
[*] Checking permissions in batches for projects/[TRUNCATED], note this might take a few minutes (~9000 permissions @ 500/~ 2 min = 36 min)
Completed 5/95
Completed 10/95
Completed 15/95
Completed 20/95
Completed 25/95
Completed 30/95
Completed 35/95
Completed 40/95
Completed 45/95
Completed 50/95
Completed 55/95
Completed 60/95
Completed 65/95
Completed 70/95
Completed 75/95
Completed 80/95
Completed 85/95
Completed 90/95
Completed 95/95
[*] Searching All Folders
[*] Getting remainting projects/folders via recursive folder/project list calls starting with org node if possible
[*] NOTE: This might take a while depending on the size of the domain
[SUMMARY] GCPwn found or retrieved NO Organization(s)
[SUMMARY] GCPwn found or retrieved NO Folder(s)
[SUMMARY] GCPwn found 1 Project(s)
   - projects/[TRUNCATED] (Production Project 1) - ACTIVE

(production-project[TRUNCATED]:service_user)> creds info

Summary for service_user:
Email: newserviceaccount@production-project[TRUNCATED].iam.gserviceaccount.com
Scopes:
    - N/A
Default Project: production-project[TRUNCATED]
All Projects:
    - production-project[TRUNCATED]

Access Token: N/A

[******] Permission Summary for service_user [******]
- Project Permissions
  - production-project[TRUNCATED]
    - accessapproval.requests.approve
    - accessapproval.requests.dismiss
    - accessapproval.requests.get
    - accessapproval.requests.invalidate
    - accessapproval.requests.list
    - accessapproval.serviceAccounts.get
    - accessapproval.settings.delete
    - accessapproval.settings.get
    - accessapproval.settings.update
    - actions.agent.claimContentProvider
    [TRUNCATED]
    - workloadmanager.insights.export
    - workloadmanager.insights.write
    - workloadmanager.locations.get
    - workloadmanager.locations.list
    - workloadmanager.operations.cancel
    - workloadmanager.operations.delete
    - workloadmanager.operations.get
    - workloadmanager.operations.list
    - workloadmanager.results.list
    - workloadmanager.rules.list
    - workstations.operations.get
    - workstations.workstationClusters.create
    - workstations.workstationClusters.delete
    - workstations.workstationClusters.get
    - workstations.workstationClusters.list
    - workstations.workstationClusters.update
    - workstations.workstationConfigs.create
    - workstations.workstationConfigs.delete
    - workstations.workstationConfigs.get
    - workstations.workstationConfigs.getIamPolicy
    - workstations.workstationConfigs.list
    - workstations.workstationConfigs.setIamPolicy
    - workstations.workstationConfigs.update
    - workstations.workstations.create
    - workstations.workstations.delete
    - workstations.workstations.get
    - workstations.workstations.getIamPolicy
    - workstations.workstations.list
    - workstations.workstations.setIamPolicy
    - workstations.workstations.start
    - workstations.workstations.stop
    - workstations.workstations.update

```
