---
author_name: Nick Frichette
title: Connection Tracking
description: Abuse security group connection tracking to maintain persistence even when security group rules are changed.
hide:
  - toc
---

# Connection Tracking

<div class="grid cards" markdown>
-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="https://frichetten.com/blog/abusing-aws-connection-tracking/">Abusing AWS Connection Tracking</a> by <a href="https://twitter.com/frichette_n">Nick Frichette</a></p>
    <p><img src="/images/researchers/nick_frichette.jpg" alt="Nick Frichette" style="width:44px;height:44px;margin:5px;border-radius:100%;max-width:unset"></img></p>
    </aside>
</div>

Security Groups in AWS have an interesting capability known as [Connection Tracking](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/security-group-connection-tracking.html). This allows the security groups to track information about the network traffic and allow/deny that traffic based on the Security Group rules.

There are two kinds of traffic flows; tracked and untracked. For example the AWS documentation mentions a tracked flow as the following, "if you initiate an ICMP ping command to your instance from your home computer, and your inbound security group rules allow ICMP traffic, information about the connection (including the port information) is tracked. Response traffic from the instance for the ping command is not tracked as a new request, but rather as an established connection and is allowed to flow out of the instance, even if your outbound security group rules restrict outbound ICMP traffic".

An interesting side effect of this is that tracked connections are allowed to persist, even after a Security Group rule change. 

Let's take a simple example: There is an EC2 instance that runs a web application. This EC2 instance has a simple Security Group that allows SSH, port 80, and port 443 inbound, and allows all traffic outbound. This EC2 instance is in a public subnet and is internet facing.

<figure markdown>
  ![Inbound SG](../../images/aws/general-knowledge/connection-tracking/inbound-sg.png){ loading=lazy }
</figure>

While performing a penetration test you've gained command execution on this EC2 instance. In doing so, you pop a simple [reverse shell](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet). You work your magic on the box before eventually triggering an alert to our friendly neighborhood defender. They follow their runbooks which may borrow from the official AWS [whitepaper](https://d1.awsstatic.com/whitepapers/aws_security_incident_response.pdf) on incident response. 

As part of the "Isolate" step, the typical goal is to isolate the affected EC2 instance with either a restrictive Security Group or an explicit Deny NACL. The slight problem with this is that NACLs affect the entire subnet, and if you are operating in a space with a ton of EC2 instances the defender is unlikely to want to cause an outage for all of them. As a result, swapping the Security Group is the recommended procedure.

The defender switches the Security Group from the web and ssh one, to one that does not allow anything inbound or outbound.

<figure markdown>
  ![Change Security Group](../../images/aws/general-knowledge/connection-tracking/change-sg.png){ loading=lazy }
</figure>

The beauty of connection tracking is that because you've already established a connection with your shell, it will persist. So long as you ran the shell before the SG change, you can continue scouring the box and looking for other vulnerabilities.

<figure markdown>
  ![whoami](../../images/aws/general-knowledge/connection-tracking/whoami.png){ loading=lazy }
</figure>

To be clear, if the restrictive security group doesn't allow for any outbound rules we won't be able to communicate out (and if you're using a beaconing C2 that will not function).

<figure markdown>
  ![No Outbound](../../images/aws/general-knowledge/connection-tracking/no-outbound.png){ loading=lazy }
</figure>
