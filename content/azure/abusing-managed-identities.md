---
author_name: andrei8055
title: Abusing Managed Identities
description: Abusing Managed Identities 
---

Original Research: [0xPwN Blog - Create an Azure Vulnerable Lab: Part #4 – Managed Identities](https://0xpwn.wordpress.com/2022/03/13/create-an-azure-vulnerable-lab-part-4-managed-identities/)

Using Managed Identities it is possible to grant a resource (such as VM/WebApp/Function/etc) access to other resource (such as Vaults/Storage Accounts/etc.) For example, if we want to give our web application access to a private storage account container without having to deal with how we safely store connection strings in config files or source code, we could use a managed identity.

    Compute Resource --> Managed Identity --> Assigned Role(s) --> Storage Account --> Container

A Managed Identity can be a System or User identity. A System identity is bound to the resource, but a User identity is independent.


## Setup Azure Managed Identity

First we enable the managed identity for the web application:


![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-20.png)

Once enabled, we are given the possibility to configure the roles assigned for this identity (i.e: permissions granted to the service that we enabled the identity for).

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-21.png)

Lastly, we assign one or more roles (which is a set of permissions) for that identity. A role can be assigned at Subscription level, Resource group, Storage Account, Vault or SQL and it propagates “downwards” in the Azure architecture layer.

The default Owner, owning the resource, and Contributor, read/write content of the resource, roles have the most permissions.

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/1.png)

Under each role, we can see in details what permissions are included. Azure allows also to configure custom roles in case the built-in ones are not suitable for your case.

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-22.png?w=1024)

Similarly, to see who has permissions granted for a give resource, we can check that under the Access Control (IAM) -> View access to this resource.

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-23.png?w=1024)

So in our case, we should see under the Storage Account that the web application has Reader and Data Access:

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-24.png)


## Next steps

Now that we have the basics of how Managed Identity works, let’s see how can we exploit this. Since the web application has access to the storage account, and we compromised the web application, we should be able to get as well access to the storage account. Long story short, we get the same permissions that the resource we compromised had. Based on how poorly the Identity roles are assigned, it could even be the case that the permissions are assigned at Subscription level, effectively granting us access to all resources inside it!

![Azure Managed Identities](https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-setup-guide/media/organize-resources/scope-levels.png)

While in our case it looks that the permissions are proper (we are limiting access only to the Storage Account that we need access to) and limit the roles to Reader and Data Access (instead of Contributor or Owner), there is still a catch. Our web app needs permissions only to the “images” container, but the managed identity configured has enough permissions to list the access keys to the whole Storage Account granting us access to any other containers hosted in the same account. 


## Exploiting Azure Managed Identity

Abusing the command injection on the web app, we can make a curl request to the $IDENTITY_ENDPOINT URL stored in the environment variables and get an access token and account id (client id in the response) which can be used to authenticate to Azure.
```bash
curl "$IDENTITY_ENDPOINT?resource=https://management.azure.com/&api-version=2017-09-01" -H secret:$IDENTITY_HEADER
```
![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-25.png)


Using the Azure Powershell module, we can connect to Azure with the access token: 
```powershell
PS> Install-Module -Name Az -Repository PSGallery -Force
PS> Connect-AzAccount -AccessToken <access_token> -AccountId <client_id>
```

Once connected, you should see details about the Subscription and Tenant that the Managed Identity we are impersonating has access to. Using the Get-AzResource Azure Powershell cmdlet, we can check which resources inside the subscription we can access:

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-26.png)


To list the roles assigned to the managed, we can use the Azure Powershell cmdlet Get-AzRoleAssignment. This cmdlet requires additionally a graph token which we can get from the https://graph.microsoft.com/ endpoint, but also the permission to list roles and permissions for identities which our Identity does not have.

However, we can still try to access the Storage Account keys without these permissions and see if we are successful. For that we will use the Get-AzStorageAccountKey cmdlet with the Resource Group Name and Account Name that we found in the previous step.

Get storage account keys:

```powershell
>Get-AzStorageAccountKey -ResourceGroupName "0xpwnlab" -AccountName "0xpwnstorageacc"
 
KeyName Value                       Permissions CreationTime
------- -----                       ----------- ----------
key1    L175hccq[...]lH9DJ==        Full 3/12/20...
key2    vcZiPzJp[...]ZkKvA==        Full 3/12/20...
```

[http://aka.ms/storage-explorer](http://aka.ms/storage-explorer)


If the above command returns two keys, than it means that our identity had permissions to list them. Let’s use these keys in Azure Storage Explorer and see if there are other containers stored on the same account. In the Azure Storage Explorer, we click the connect icon and select storage account or service.

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-27.png)

On the second step, this time we select the Account name and key option:

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-28.png)

For the Account name we use the name that we enumerated in the Get-AzResource step, while for the key we can use either of the two we found:

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-29.png)

Once we connect, on the left side menu we should find a new storage account, we see 2 containers: the images container used by the web app, but also another one containing the flag. 

![Azure Managed Identities](https://0xpwn.files.wordpress.com/2022/03/image-30.png)

And that’s it! We have just seen how abusing a command injection into a web app, we discovered that it had a managed identity associated to it. After we got the JWT access token, we connected to Azure using the Azure Powershell and enumerated the resources that we have access to. The improper permissions set for the Managed Identity allowed us to read the access key for the whole Storage Account and discover another private container that was not referenced anywhere, containing the flag sensitive information. 
