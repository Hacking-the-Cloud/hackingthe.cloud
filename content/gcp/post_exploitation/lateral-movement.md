---
author_name: Chris Moberly
title: Lateral Movement
description: Common lateral movement techniques in GCP.
---

Extracted from the GitLab blog post "[Tutorial on privilege escalation and post exploitation tactics in Google Cloud Platform environments](https://about.gitlab.com/blog/2020/02/12/plundering-gcp-escalating-privileges-in-google-cloud-platform/)" by [Chris Moberly](https://about.gitlab.com/company/team/#cmoberly)

---

You've compromised one VM inside a project. Great! Now let's get some more...

You can try the following command to get a list of all instances in your current project:

```
$ gcloud compute instances list
```

## SSH'ing around

You can use local privilege escalation tactics to move around to other machines.

One way is to [applying SSH keys at the project level](https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys#project-wide), granting you permission to SSH into a privileged account for any instance that has not explicitly chosen the "Block project-wide SSH keys" option.

After you've identified the strategy for selecting or creating a new user account, you can use the following syntax.

```
$ gcloud compute project-info add-metadata --metadata-from-file ssh-keys=meta.txt
```

If you're really bold, you can also just type `gcloud compute ssh [INSTANCE]` to use your current username on other boxes.

## Abusing networked services

### Some GCP networking tidbits

Compute Instances are connected to networks called VPCs or [Virtual Private Clouds](https://cloud.google.com/vpc/docs/vpc). [GCP firewall](https://cloud.google.com/vpc/docs/firewalls) rules are defined at this network level but are applied individually to a Compute Instance. Every network, by default, has two [implied firewall rules](https://cloud.google.com/vpc/docs/firewalls#default_firewall_rules): allow outbound and deny inbound.

Each GCP project is provided with a VPC called `default`, which applies the following rules to all instances:

- default-allow-internal (allow all traffic from other instances on the `default` network)
- default-allow-ssh (allow 22 from everywhere)
- default-allow-rdp (allow 3389 from everywhere)
- default-allow-icmp (allow ping from everywhere)

### Meet the neighbors

Firewall rules may be more permissive for internal IP addresses. This is especially true for the default VPC, which permits all traffic between Compute Instances.

You can get a nice readable view of all the subnets in the current project with the following command:

```
$ gcloud compute networks subnets list
```

And an overview of all the internal/external IP addresses of the Compute Instances using the following:

```
$ gcloud compute instances list
```

If you go crazy with nmap from a Compute Instance, Google will notice and will likely send an alert email to the project owner. This is more likely to happen if you are scanning public IP addresses outside of your current project. Tread carefully.

### Enumerating public ports

Perhaps you've been unable to leverage your current access to move through the project internally, but you DO have read access to the compute API. It's worth enumerating all the instances with firewall ports open to the world - you might find an insecure application to breach and hope you land in a more powerful position.

In the section above, you've gathered a list of all the public IP addresses. You could run nmap against them all, but this may taken ages and could get your source IP blocked.

When attacking from the internet, the default rules don't provide any quick wins on properly configured machines. It's worth checking for password authentication on SSH and weak passwords on RDP, of course, but that's a given.

What we are really interested in is other firewall rules that have been intentionally applied to an instance. If we're lucky, we'll stumble over an insecure application, an admin interface with a default password, or anything else we can exploit.

[Firewall rules](https://cloud.google.com/vpc/docs/firewalls) can be applied to instances via the following methods:

- [Network tags](https://cloud.google.com/vpc/docs/add-remove-network-tags)
- [Service accounts](https://cloud.google.com/vpc/docs/firewalls#serviceaccounts)
- All instances within a VPC

Unfortunately, there isn't a simple `gcloud` command to spit out all Compute Instances with open ports on the internet. You have to connect the dots between firewall rules, network tags, services accounts, and instances.

The GitLab Red Team has automated this completely using [this python script](https://gitlab.com/gitlab-com/gl-security/gl-redteam/gcp_firewall_enum) which will export the following:

- CSV file showing instance, public IP, allowed TCP, allowed UDP
- nmap scan to target all instances on ports ingress allowed from the public internet (0.0.0.0/0)
- masscan to target the full TCP range of those instances that allow ALL TCP ports from the public internet (0.0.0.0/0)

Full documentation on that tool is availabe in the [README](https://gitlab.com/gitlab-com/gl-security/gl-redteam/gcp_firewall_enum/blob/master/README.md).
