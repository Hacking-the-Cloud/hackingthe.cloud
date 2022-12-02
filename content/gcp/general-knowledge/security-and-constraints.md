---
author_name: Moses Frost (@mosesrenegade)
title: Security and Constraints
description: Security considerations and constraints that are unique to GCP
---


GCP Resources are typically placed into Projects. Projects are a mix of resource groups in Azure and Accounts in AWS. Projects can be either non-hierarchical or completely hierarchical. An operator can place security constraints on these projects to provide a baseline security policy. There are also Organization-wide policy constraints that apply to every project.

## Examples

From: [Organizational Policy Constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)

* constraints/iam.disableServiceAccountCreation : This can disable the overall creation of service accounts. Equivalent to Service Principals in Azure.
* constraints/iam.disableServiceAccountKeyCreation : This constraint will disable the ability to create a service account key. This constraint would be helpful if you want service accounts but only want to use RSA-based authentication. 

There are specific policies that are *not* retroactive. We can use these to our *advantage*. 

1. `constraints/compute.requireShieldedVm`: If a compute node is already created and exists without this constraint applied, then this constraint will not be retroactive. You *must* delete the object and re-create it for it to enforce shielded VMs. 
2. `constraints/compute.vmExternalIpAccess`: Consider the following scenario:
    
    - Constraint is based on the following permutation: `projects/PROJECT_ID/zones/ZONE/instances/INSTANCE`
    - Constraint looks for the `name` of the machine in the `project` identifier specified in the specific `zone`
    - If you can boot a VM with this specific set of criteria, then you can have a machine with an External IP Address
    - Machine cannot already exist.
3. `constraints/compute.vmCanIpForward`: Another Non Retroactive Setting. The machine must not exist before this setting is created. Once this is set, then machines will enforce this condition.

