---
author_name: Moses Frost (@mosesrenegade)
title: Security and Constraints
description: Security considerations and constraints that are unique to GCP
---

Resources in GCP are created within projects. Projects are a mix of resource groups in Azure and accounts in AWS. Projects can optionally be organized using folders, which can be nested, to create a hierarchy. Projects and folders exist below a top-level organization. If a customer environment does not have a defined organization, the top-level entity will be an unnamed organization.

An operator can place security constraints on organizations, folders, and projects to provide a baseline security policy. There are also organization-wide policy constraints that apply to every project. Policies are inherited from all containing items.

![](https://cloud.google.com/static/resource-manager/img/cloud-hierarchy.svg)

Reference: [Resource hierarchy](https://cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy)

## Examples

From: [Organizational Policy Constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints)

* constraints/iam.disableServiceAccountCreation : This can disable the overall creation of service accounts. Equivalent to Service Principals in Azure.
* constraints/iam.disableServiceAccountKeyCreation : This constraint will disable the ability to create a service account key. This constraint would be helpful if you want service accounts but only want to use RSA-based authentication. 

The majority of org policies are *not* retroactive. This means that if an org policy is created to enforce a particular constraint, any resources that already existed at the time of the policy creation will not be affected - even if they violate the new constraint. For example, if a policy is created to prevent creation of global load balancers, any existing global load balancers will not be impacted or deleted when the policy is established, and the load balancers will continue to function.

According to Google, "If an organization policy constraint is retroactively enforced, it will be labeled as such on the [organization policy constraints](https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints) page." At the time of writing, only two constraints are retroactively enforced:

1. `constraints/sql.restrictNoncompliantResourceCreation`: The documentation oddly states that this is retroactive, but then proceeds to state that it is retroactive in that it applies to existing projects, but does not apply to resources that existed at the time of policy modification (which thus means it is not retroactive).
2. `constraints/dataform.restrictGitRemotes`: This is used to restrict access to repositories from Dataform. It makes sense that this would be retroactive, as it impacts communication rather than resource creation.

We can use the non-retroactive nature of org policies to our *advantage*. 

1. `constraints/compute.requireShieldedVm`: If a compute node is already created and exists without this constraint applied, then this constraint will not be retroactive. You *must* delete the object and re-create it for it to enforce shielded VMs. 
2. `constraints/compute.vmExternalIpAccess`: Consider the following scenario:
   
    - Constraint is based on the following permutation: `projects/PROJECT_ID/zones/ZONE/instances/INSTANCE`
    - Constraint looks for the `name` of the machine in the `project` identifier specified in the specific `zone`
    - If you can boot a VM with this specific set of criteria, then you can have a machine with an External IP Address
    - Machine cannot already exist.
3. `constraints/compute.vmCanIpForward`: The machine must not exist before this setting is created. Once this is set, then machines will enforce this condition.

