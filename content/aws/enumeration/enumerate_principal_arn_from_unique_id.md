---
author_name: Nick Frichette
title: Derive a Principal ARN from an AWS Unique Identifier
description: How to convert an unique identifier to a principal ARN.
---

<div class="grid cards" markdown>

-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="https://awsteele.com/blog/2023/11/19/reversing-aws-iam-unique-ids.html">Reversing AWS IAM unique IDs</a> by <a href="https://twitter.com/__steele">Aidan Steele</a></p>
    <p><img src="/images/researchers/aidan_steele.jpg" alt="Aidan Steele" style="width:44px;height:44px;margin:5px;border-radius:100%;max-width:unset"></img></p>
    </aside>

-   :material-book:{ .lg .middle } __Additional Resources__

    ---

    Reference: [Unique identifiers](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids)

</div>

When operating in an AWS environment, you may come upon a variety of [IAM unique identifiers](https://hackingthe.cloud/aws/general-knowledge/iam-key-identifiers/). These identifiers correspond to different types of AWS resources, and the type of the resource can be identified by the prefix (the first four characters).

For IAM users (AIDA) and roles (AROA) you can reverse the unique ID to its corresponding ARN by referencing it in a [resource-based policy](https://hackingthe.cloud/aws/exploitation/Misconfigured_Resource-Based_Policies/).

To do this, we can use the example ID of `AROAJMD24IEMKTX6BABJI` from [Aidan Steele](https://twitter.com/__steele)'s excellent explanation of the topic. While this technique should work with most resource-based policies, we will use a role's trust policy.

First, we will create a role with the following trust policy:

```json
{
	"Version": "2008-10-17",
	"Statement": [
		{
			"Sid": "Statement1",
			"Effect": "Allow",
			"Principal": {
				"AWS": "AROAJMD24IEMKTX6BABJI"
			},
			"Action": "sts:AssumeRole"
		}
	]
}
```

We will then save the policy and refresh the page. 

!!! Note
    You may get a warning in the policy editor saying, "Invalid Role Reference: The Principal element includes the IAM role ID AROAJMD24IEMKTX6BABJI. We recommend that you use a role ARN instead", however this will not prevent you from saving the policy.

After refreshing the page the policy will now be as follows:

```json
{
    "Version": "2008-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::607481581596:role/service-role/abctestrole"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

This reveals the ARN of the role associated with the original unique identifier.
