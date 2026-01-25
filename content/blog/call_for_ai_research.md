---
author_name: Nick Frichette
title: "Call for research: AI and LLM security"
description: Hacking the Cloud is opening the door to AI and LLM security research.
date: 2026-01-26T00:00:40-06:00
---
<aside markdown style="display:flex">
  <p><img src="https://avatars.githubusercontent.com/u/10386884?v=4" style="width:44px;height:44px;margin:5px;border-radius:100%"></img></p>

  <span>__Nick Frichette__ · @frichette_n · <a href="https://twitter.com/Frichette_n">:fontawesome-brands-twitter:{ .twitter }</a> <a href="https://fosstodon.org/@frichetten">:fontawesome-brands-mastodon:{ .mastodon }</a> <a href="https://bsky.app/profile/frichetten.com">:fontawesome-brands-bluesky:{ .bluesky }</a></span>
  <br>
  <span>
    :octicons-calendar-24: January 25, 2026
  </span>
</aside>
---

Since 2020, Hacking the Cloud has documented attack paths in cloud environments, sharing offensive cloud security knowledge with hundreds of thousands of readers. With the rise of LLMs and AI, those same cloud environments now contain models, agents, and pipelines that inherit all the same trust boundaries and failures we’ve been writing about for years.

I’ve been seeing more AI workloads show up in the same AWS accounts, Azure subscriptions, and GCP projects that Hacking the Cloud already covers. As a result, many cloud security teams are seeing their scope expand to include systems they were never originally asked to secure.

In some ways, what was once old is new again.

The agent that gets prompt injected into exfiltrating secrets? It may be using the same [IAM permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples-agent.html) we've been abusing for years. The model endpoint that leaks training data? It is probably exposed because someone set the wrong resource policy. The S3 bucket that... well, you already know what happens to S3 buckets.

Like many cloud security teams, I’m expanding the scope of Hacking the Cloud as well. This post is an open __call for research__: Hacking the Cloud is now accepting, and actively looking for, AI and LLM security research.

## Content

Some of this content will be cloud-specific. How do you pivot from a compromised SageMaker notebook to the rest of the AWS account? What happens when you can invoke a Bedrock agent but should not be able to? That kind of research fits naturally alongside existing Hacking the Cloud content.

Other research will not be cloud-specific at all, and that is fine. Prompt injection in a RAG pipeline works the same whether the vector store runs on AWS or on a server sitting in someone’s closet. Agent toolchains have the same trust boundary problems everywhere. If the research has real security implications, I want it here.

I keep coming back to how new all of this still is. Companies are deploying models in production without understanding what can go wrong. Security teams are being asked to assess systems they have never seen before. Red teamers are discovering new attack surfaces in real time. There is not much solid documentation yet, and what exists is scattered across blog posts, conference talks, and Twitter threads.

Hacking the Cloud was created for __exactly__ this reason when it came to cloud security.

That gap is why this matters. Hacking the Cloud has always tried to be the place where offensive cloud security knowledge gets written down in one spot. AI security needs the same treatment.

## Topics I'm looking for

This is not a complete list, just enough to give you a sense of what fits:

- **Cloud-hosted AI services.** The managed offerings from AWS, Azure, and GCP all have their own quirks. How does identity work? What gets logged, and what does not? Where are the network boundaries? I'm looking for research on SageMaker, Bedrock, Vertex AI, Azure OpenAI Service, and similar platforms.
- **Agents and tool use.** LLM agents that can execute code, call APIs, or access databases have a lot of attack surface. How do you get an agent to misuse its tools? What happens when the tool permissions are too broad? This area is moving fast and not well understood.
- **RAG and retrieval systems.** Retrieval-augmented generation pipelines can leak data in interesting ways. Sometimes the problem is a cloud misconfiguration (the vector database is public). Sometimes the problem is in the retrieval logic itself (the model can be tricked into returning documents the user should not see). Both are worth documenting.
- **Model supply chain.** Where do model weights come from? How do you verify that the model you downloaded is the model you expected? What happens when someone poisons a model on Hugging Face and it gets pulled into a production pipeline? The supply chain risks here are not that different from traditional software, but the mitigations are less mature.
- **Cost and resource abuse.** Training and inference are expensive. Attackers who get access to AI infrastructure can run up significant bills or steal compute for their own purposes. Documenting these patterns helps defenders know what to monitor.
- **GPU infrastructure and isolation.** Multi-tenant GPU environments have their own class of problems. Shared memory, side channels, isolation failures. If you have done research here, I want to hear about it.
- **Defensive guidance.** While Hacking the Cloud focuses on offensive techniques, defensive guidance is welcome when it is grounded in real attack paths. How do you detect prompt injection attempts? What should you log? How do you design IAM policies for AI workloads without handing over the keys? Practical recommendations backed by experience are especially valuable.

## What I'm not looking for

Some things do not fit the site and I've documented a few of them below. If you would like to contribute an article, but aren't sure if it's a good fit, please open an [issue](https://github.com/Hacking-the-Cloud/hackingthe.cloud/issues) on GitHub and ask.

**Prompt tricks without security impact.** Getting a chatbot to roleplay as a pirate is not a security finding. I’m interested in techniques that lead to real harm: data exfiltration, unauthorized actions, privilege escalation, or denial of service. The bar is "would a security team care about this?"

**Product comparisons and marketing.** This is not a place to review or promote AI platforms. If your writeup reads like marketing or is trying to sell something, it does not belong here.

**Policy and ethics without technical content.** The policy and ethics discussions around AI are important, but this site focuses on technical security content. If there is no concrete security impact, it is likely a better fit elsewhere.

## How to contribute

Before writing, read the [contributing guide](https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/master/CONTRIBUTING.md). It covers formatting expectations and the review process. New AI/LLM content goes under `content/ai-llm/`. Follow the same structure as existing pages on the site.

A core guideline of Hacking the Cloud is that sources must always be cited and original researchers credited. You are welcome to summarize existing work or add your own analysis, but original research must be acknowledged. If you are the original researcher, you are welcome to republish or adapt your work here.

Hacking the Cloud currently sees around 8,000–9,000 unique visitors per month, and contributing can help drive traffic to your research.

When you are ready, open a [pull request](https://github.com/Hacking-the-Cloud/hackingthe.cloud/pulls). If you want to discuss an idea before writing, open an [issue](https://github.com/Hacking-the-Cloud/hackingthe.cloud/issues) or start a [discussion](https://github.com/Hacking-the-Cloud/hackingthe.cloud/discussions) with a short summary.

If you are unsure whether something fits, send me an outline. I would rather help shape a piece early than have you put in work on something that does not land.

## Deconflicting between cloud and AI sections

One question you may have already asked is where cloud-specific AI research should live. For example, should a SageMaker-specific LLM technique go in the AWS section or the AI/LLM section?

As a rule of thumb, techniques that only make sense within a specific cloud provider should live in that provider’s section. Techniques that generalize across platforms should live in the AI/LLM section.

This will be evaluated on a case-by-case basis. If you have a strong reason to place content in one section or the other, I’m open to hearing it.

## Why this matters now

The cloud security community has already been dealing with AI in production, whether or not it has been written about. Incident responders are seeing compromised SageMaker notebooks. Pentesters are finding overprivileged Bedrock agents. Red teams are being asked to test systems that did not exist two years ago.

The knowledge exists, but it is scattered. Hacking the Cloud was created to fix that problem for cloud security, and now I want to do the same for AI security.

If you’re already doing this work, I want it written down. If you’ve seen something break in production, I want to understand it. If you’ve explored an attack surface and learned something new, that’s exactly what belongs here.

If you’re already encountering these failures in real environments, now is the time to share them with the security community.
