---
author_name: andrei8055
title: Anonymous Blob Access
description: Finding and accessing files stored in Azure Storage Accounts without authentication.
---

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    [Create an Azure Vulnerable Lab: Part #1 – Anonymous Blob Access](https://0xpwn.wordpress.com/2022/03/05/setting-up-an-azure-pentest-lab-part-1-anonymous-blob-access/) by [Andrei Agape](https://tripla.dk/author/drag0nus/)
</div>

"Storage Accounts" is the service provided by Azure to store data in the cloud. A storage account can used to store:

- Blobs
- File shares
- Tables
- Queues
- VM disks

![Azure Storage Account](../images/azure/anonyous-blob-access/Azure%20Storage%20Types.png)

For this tutorial, we will focus on the Blobs section. Blobs are stored within a container, and we can have multiple containers within a storage account. When we create a container, Azure will ask on the permissions that we grant for public access. We can chose between:

- Private Access – no anonymous access is allowed
- Blob Access – we can access the blobs anonymously, as long as we know the full URL (container name + blob name)
- Container Access – we can access the blobs anonymously, as long we know the container name (directory listing is enabled, and we can see all the files stored inside the container)

As you might have guessed, granting Container Access permission can be easily abused to download all the files stored within the container without any permissions as the only things required to be known are the storage account name and the container name, both of which can be enumerated with wordlists.

## Exploiting Anonymous Blob Access

Now, there are thousands of articles explaining how this can be abused and how to search for insecure storage in Azure, but to make things easier I’ll do a TL:DR. One of the easiest way is to use MicroBurst, provide the storage account name to search for, and it’ll check if the containers exists based on a wordlist saved in the Misc/permutations.txt:

```
PS > import-module .\MicroBurst.psm1
PS> Invoke-EnumerateAzureBlobs -Base 0xpwnstorageacc
Found Storage Account - 0xpwnstorageacc.blob.core.windows.net
Found Container - 0xpwnstorageacc.blob.core.windows.net/public
Public File Available: https://0xpwnstorageacc.blob.core.windows.net/public/flag.txt
```

Alternatively adding ```?restype=container&comp=list``` after the container name:
```
https://<storage_account>.blob.core.windows.net/<container>?restype=container&comp=list
```
Output:
```

<EnumerationResults ContainerName="https://0xpwnstorageacc.blob.core.windows.net/public">
	<Blobs>
		<Blob>
			<Name>flag.txt</Name>
			<Url>
https://0xpwnstorageacc.blob.core.windows.net/public/flag.txt
</Url>
			<Properties>
				<Last-Modified>Sat, 05 Mar 2022 18:02:14 GMT</Last-Modified>
				<Etag>0x8D9FED247B7848D</Etag>
				<Content-Length>34</Content-Length>
				<Content-Type>text/plain</Content-Type>
				<Content-Encoding/>
				<Content-Language/>
				<Content-MD5>lur6Yvd173x6Zl1HUGvtag==</Content-MD5>
				<Cache-Control/>
				<BlobType>BlockBlob</BlobType>
				<LeaseStatus>unlocked</LeaseStatus>
			</Properties>
		</Blob>
	</Blobs>
	<NextMarker/>
</EnumerationResults>
```
