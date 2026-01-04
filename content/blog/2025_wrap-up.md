---
title: "2025 Hacking the Cloud: Year in Review"
description: An end of year summary for Hacking the Cloud in 2025.
date: 2026-01-05T00:00:40-05:00
---
<aside markdown style="display:flex">
  <p><img src="https://avatars.githubusercontent.com/u/10386884?v=4" style="width:44px;height:44px;margin:5px;border-radius:100%"></img></p>

  <span>__Nick Frichette__ · @frichette_n · <a href="https://twitter.com/Frichette_n">:fontawesome-brands-twitter:{ .twitter }</a> <a href="https://fosstodon.org/@frichetten">:fontawesome-brands-mastodon:{ .mastodon }</a> <a href="https://bsky.app/profile/frichetten.com">:fontawesome-brands-bluesky:{ .bluesky }</a></span>
  <br>
  <span>
    :octicons-calendar-24: January 5, 2026
  </span>
</aside>
---

As 2025 comes to a close, it’s worth taking a moment to reflect on what has been an exceptional year for both cloud security and the Hacking the Cloud community.

This year felt like a turning point, not just in the volume and criticality of cloud security research, but in its maturity. We saw deeper technical analysis, faster community-driven incident response, and clearer evidence that cloud security is no longer a niche discipline. 

AI continued to dominate headlines in 2025, but beneath the buzz we also saw more enduring themes emerge: software supply chain risk, developer-targeted attacks, and the growing importance of transparency from cloud providers. Many of these themes will undoubtedly define 2026 as well.

In reflecting on 2025, I wanted to share not just project metrics, but a more holistic view of everything that shaped the year. If you’re primarily interested in the site’s performance by the numbers, you can skip ahead to that section [here](#hacking-the-cloud-in-2025-by-the-numbers).

---

## 2025 highlights

### fwd:cloudsec US and EU

Once again, fwd:cloudsec US and fwd:cloudsec EU brought together some of the most thoughtful and technically rigorous minds in cloud security. These conferences have continued to prove that there is a strong appetite for deep, practitioner-focused content that goes beyond surface-level cloud discussions.

While you should absolutely watch every single talk, here are a few highlights I’d recommend starting with:

- [Patience brings prey: lessons learned from a year of threat hunting in the cloud](https://www.youtube.com/watch?v=cugwipMXHp0) (fwd:cloudsec US 2025)
- [I SPy: Rethinking Entra ID research for new paths to Global Admin](https://www.youtube.com/watch?v=oNpwtt1TEkQ) (fwd:cloudsec US 2025)
- [Shared-GPU Security Learnings from Fly.io](https://www.youtube.com/watch?v=_W4NHw-4P8A) (fwd:cloudsec US 2025)
- [ECS-cape – Hijacking IAM Privileges in Amazon ECS](https://www.youtube.com/watch?v=WXdB-9pTqAU) (fwd:cloudsec US 2025)
- [whoAMI: Discovering and exploiting a large-scale AMI name confusion attack](https://www.youtube.com/watch?v=2mxMW6dw-Fs) (fwd:cloudsec US 2025)
- [Mistrusted Advisor: When AWS Tooling Leaves Public S3 Buckets Undetected](https://www.youtube.com/watch?v=JUM77vJzM54) (fwd:cloudsec EU 2025)
- [Source IP Spoofing in Cloud Logs: A Hands-On Look Across AWS, Azure, and GCP](https://www.youtube.com/watch?v=wzr2EIBuYqU) (fwd:cloudsec EU 2025)
- [The File That Contained the Keys Has Been Removed: An Analysis of Secret Leaks in Cloud Buckets and Responsible Disclosure Outcomes](https://www.youtube.com/watch?v=y1-sVKoQxrw) (fwd:cloudsec EU 2025)

Last year marked the first time we produced Hacking the Cloud stickers. In 2025, we expanded that effort with event-specific drops, including a limited run of holographic stickers for fwd:cloudsec Europe 2025. The reception was overwhelmingly positive, and this is something we plan to continue, and expand, next year.

![Holographic fwd:cloudsec Europe 2025 stickers](../images/blog/2025_wrap-up/stickers.jpg)

With the surprising announcement that AWS re:Inforce will [not](https://reinforce.awsevents.com/) be happening in 2026, it has been particularly striking to see fwd:cloudsec continue to thrive. Some may remember that fwd:cloudsec originally emerged as something of an add-on to re:Inforce. Over time, however, its independent value has become clear. Today, fwd:cloudsec doesn’t just stand on its own, it needs to.

### Supply chain security continues to be a growing risk

While AI remained front and center throughout 2025, a close second in terms of impact was the continued rise of software supply chain attacks. Attackers are increasingly targeting developers, build systems, and trusted distribution mechanisms rather than production infrastructure directly. This year alone saw incidents such as [Shai-Hulud](https://securitylabs.datadoghq.com/articles/shai-hulud-2.0-npm-worm/), [S1ngularity](https://nx.dev/blog/s1ngularity-postmortem), and more.

As a cloud security–focused project, it would be impossible not to highlight a supply chain incident that directly involved a major cloud provider: AWS.

In July, it was [reported](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/) that a threat actor abused a [memory dump issue in AWS CodeBuild](https://aws.amazon.com/security/security-bulletins/aws-2025-016/) to steal an "inappropriately scoped GitHub token". That token was then used to push malicious code into the [Amazon Q Developer VS Code extension](https://github.com/aws/aws-toolkit-vscode).

The injected payload consisted of a prompt instructing the AI to “clean a system to a near-factory state and delete file-system and cloud resources.” Given the popularity of the extension, the potential blast radius was enormous.

The only thing standing between us and nearly a million machines getting wiped was....a typo? It seems the attacker dropped the ball at the very last second. The attacker attempted to invoke the prompt with:

```shell
q --trust-all-tools --no-interactive "${re}"
```

However, the correct command should have been:

```shell
q chat --trust-all-tools --no-interactive "${re}"
```

Because of this mistake, the injected prompt was effectively inert.

While any organization can fall victim to a supply chain attack, AWS’s response left much to be desired. As the situation unfolded, independent security researchers were often deriving and sharing a clearer picture than AWS was presenting. The community relied heavily on those researchers while official communication lagged behind.

As one researcher succinctly put it:

> “The security community is giving us the details AWS hasn’t yet (a security bulletin is not a post mortem).”
> — [Matt Fuller](https://x.com/matthewdfuller/status/1948773224583496025?s=20)

A major shout-out is warranted for [Michael Bargury](https://x.com/mbrg0), whose work reconstructing a [detailed timeline](https://mbgsec.com/posts/2025-07-24-constructing-a-timeline-for-amazon-q-prompt-infection/) of the attack provided critical clarity when it was most needed.

Beyond the lack of timely information, there were also moments of demonstrable misinformation, which only compounded confusion and frustration within the community.

![Q Developer Misinformation](../images/blog/2025_wrap-up/nick-meme-q-dev.png)

This incident highlights a recurring challenge within large cloud providers: legacy incident-response instincts that prioritize silence over transparency. AWS has an opportunity to lead by example in cloud security, but doing so requires a willingness to communicate openly and early. It is my hope that AWS learns from this event and raises the bar going forward.

### One Token to Rule Them All: The most critical cloud vulnerability of 2025

In one of the most striking cloud security stories of the year, researcher Dirk-jan Mollema [uncovered a vulnerability](https://dirkjanm.io/obtaining-global-admin-in-every-entra-id-tenant-with-actor-tokens/) in Microsoft Entra ID that could have allowed an attacker to obtain Global Administrator privileges in virtually any tenant using a little-known authentication mechanism called Actor Tokens. 

The flaw, later tracked as [CVE-2025-55241](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-55241) and rated CVSS 10.0, stemmed from a combination of undocumented “Actor tokens” (internal, backend impersonation tokens used by Microsoft services that bypass many modern security controls) and a token validation issue in the legacy Azure AD Graph API that failed to verify the originating tenant properly. 

Because tenant IDs and user identifiers (netIds) can be discovered via public APIs, an attacker could craft a malicious Actor Token in their own tenant and send it to the Graph API of another tenant, bypassing Conditional Access, multifactor authentication (MFA), and standard logging. With this, they could impersonate any user, including Global Admins, and make changes that those privileged accounts could make, from user creation to configuration changes, without detection. What made this especially alarming was that these tokens didn’t generate telemetry in the victim tenant, and the API component didn’t log access effectively, meaning a real attack could have unfolded with few traces.

While there’s no evidence this vulnerability was exploited in the wild, its existence underscores a profound risk: identity providers are the single point of failure in cloud ecosystems, and weaknesses in core authentication logic can have catastrophic implications. 

This vulnerability is arguably the most critical cloud vulnerability that has ever been publicly disclosed. Major shout out to [Dirk-jan](https://x.com/_dirkjan) for this incredible discovery! He has set the bar high for other researchers to follow.

### A comprehensive IAM privilege escalation and lateral movement knowledge base

(**Full disclosure**: [Seth Art](https://x.com/sethsec) is a friend and colleague, which introduces some bias. That said, Pathfinding.cloud stands on its own merits and is well worth highlighting.)

In late 2025, the cloud security community saw the release of [Pathfinding.cloud](https://pathfinding.cloud/paths/), an extensive open knowledge base documenting how AWS Identity and Access Management (IAM) permissions can be chained together to create privilege escalation and lateral movement attack paths. Built by security researchers and released through [Datadog Security Labs](https://securitylabs.datadoghq.com/), Pathfinding.cloud focuses on real-world combinations of permissions and configurations that allow one principal to escalate its privileges or assume access to another principal in an AWS environment.

Each documented “path” includes:

- Prerequisites for the escalation sequence  
- Exploitation steps 
- Visualizations illustrating how permissions interact 
- Remediation recommendations to break the chain before it’s exploitable 

For cloud security teams, penetration testers, and red teamers alike, Pathfinding.cloud has quickly become a valuable reference for both offense (understanding what an adversary could chain together) and defense (prioritizing mitigations that disrupt those chains). Its release in 2025 reflects a broader shift in cloud security toward understanding relationships between permissions, not just individual misconfigurations.

---

## Personal highlights from 2025

Hacking the Cloud has always been, and will always be, an independent, community-driven resource. That said, I’d like to briefly share a few personal milestones from 2025 that intersect with the project.

### Conference speaking

In 2025, I spoke at three conferences, including:

- Keynote at Wild West Hacking Fest: Mile High: [I Want You to Hack AWS: Cloud Penetration Testing for Traditional Hackers](https://www.youtube.com/watch?v=47cjTYtd9yI)
- Speaker at RSA Conference: [Critiquing Cloud Criminals: Ready for Smarter Cloud Attacks?](https://www.youtube.com/watch?v=oL2JnblVzmA)
- Speaker at fwd:cloudsec Europe: [Sweet Deception: Mastering AWS Honey Tokens to Detect and Outsmart Attackers](https://www.youtube.com/watch?v=R75ZTBnUwXk)

### #1 on the AWS Vulnerability Disclosure Program leaderboard

In 2024, AWS launched its [Vulnerability Disclosure Program (VDP)](https://hackerone.com/aws_vdp). Over the past year, I’ve been submitting vulnerabilities that my automation identifies in AWS APIs. As a result of that work, I reached the **#1 spot on the public AWS VDP leaderboard** at the time of writing.

![AWS VDP Leader Board](../images/blog/2025_wrap-up/leaderboard.png)

Additionally, the AWS security team awarded me a challenge coin in recognition of these contributions.

![AWS Security Challenge Coin](../images/blog/2025_wrap-up/coin.jpg)

This accomplishment reinforces a belief I’ve long held: cloud security is a team sport. Meaningful improvements require collaboration between cloud providers and independent researchers, and programs like the VDP are a critical part of that ecosystem.

### A quieter year

Compared to previous years, my public output was somewhat lower in 2025. A combination of non-cloud-focused work and external distractions limited the time I could dedicate to research.

That said, I’m planning to return to cloud security research more fully in 2026 and continue delivering the kind of work that initially motivated Hacking the Cloud.

---

## Hacking the Cloud in 2025: by the numbers

With the narrative context out of the way, let's take a look at how Hacking the Cloud is doing by the numbers. All data was collected around 10:00 AM Central on December 28, 2025.

### Project metrics

In 2025, Hacking the Cloud recorded:

- **683 new GitHub stars** (2,448 total)
- **63 commits made**
- **96,329 unique visitors**
- **181,561 pageviews**
- **8,092 average monthly visitors** (excluding December)
- And, of course, **a partridge in a pear tree**

The number of contributors also grew to **41 total contributors**, up from 33 the previous year. A sincere thank you to everyone who contributed to Hacking the Cloud this year. From fixing a single typo to authoring entire articles, every contribution meaningfully improves the quality and accuracy of the project. This site exists because of the time, effort, and expertise of its contributors, and I’m deeply grateful for all of it.

### Most popular articles

- [AWS CLI Tips and Tricks](https://hackingthe.cloud/aws/general-knowledge/aws_cli_tips_and_tricks/) – 13,229 pageviews
- [Steal EC2 Metadata Credentials via SSRF](https://hackingthe.cloud/aws/exploitation/ec2-metadata-ssrf/) – 10,623 pageviews
- [Abusing Managed Identities](https://hackingthe.cloud/azure/abusing-managed-identities/) – 7,377 pageviews
- [Exploiting Public AWS Resources - CLI Attack Playbook](https://hackingthe.cloud/aws/exploitation/Misconfigured_Resource-Based_Policies/exploting_public_resources_attack_playbook/) – 5,126 pageviews
- [AWS Organizations Defaults & Pivoting](https://hackingthe.cloud/aws/general-knowledge/aws_organizations_defaults/) – 4,686 pageviews

### Social media traffic sources

![Social pie chart](../images/blog/2025_wrap-up/socials.png)

1. LinkedIn – 47% (+7% YoY)
2. GitHub – 23% (+9% YoY)
3. Twitter – 14% (−9% YoY)
4. Reddit – 12% (−8% YoY)
5. Bluesky – 2% (+2% YoY)

LinkedIn continues to be the dark horse of social platforms for cloud security, now accounting for nearly half of all social media–driven traffic.

Twitter’s decline has been consistent year over year, dropping from 30% in 2023 to 23% in 2024, and now to 14% in 2025. Both the data and anecdotal experience suggest a significant reduction in meaningful technical discourse. For some of you (including myself) this is a really dissapointing statistic. Back in the day, Twitter was THE place to be when discussing vulnerabilities, major incidents, and more. 

While I can't say that LinkedIn is a replacement, it is at least a bit more productive than the general spam you find on Twitter these days. 

---

## Looking ahead to 2026

### Evaluating a new CMS

For several [years](https://hackingthe.cloud/blog/v2_new_look/), Hacking the Cloud has been built on [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/), which has served the project well. However, due to the fact that MKDocs is no longer being maintained, the team behind Material for MKDocs are branching out with their own CMS, [Zeniscal](https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/). 

This move reflects a desire for longer-term extensibility, richer content features, and more sustainable platform evolution. Zeniscal is still in early development, but we’ll be closely evaluating it as it matures to determine when—and if—it makes sense for Hacking the Cloud to migrate.

---

## Closing thoughts

Hacking the Cloud exists because a community of practitioners continues to share, test, and document offensive cloud security techniques, often in environments where transparency is not guaranteed.

Thank you to every contributor, reader, researcher, and reviewer who made 2025 what it was. I’m excited to see where we can take this project together in 2026.