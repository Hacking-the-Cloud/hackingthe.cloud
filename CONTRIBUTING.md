# Contributing

## Plagiarism Policy

All content submitted to Hacking the Cloud must be written in your own words. Submissions which appear to include plagiarized material (copying and pasting of whole articles/blog posts) will be rejected. It is okay to quote an existing article (with the reference). The goal of Hacking the Cloud is to congregate knowledge for the community into a single location. This includes having links/references to primary sources.

Think of Hacking the Cloud as the [Wikipedia](https://www.wikipedia.org/) of cloud security. We should cite our sources and quote content when needed, but our articles are written by our own contributors.

__If you are an author and believe your work has been plagiarized on Hacking the Cloud, please submit an [issue](https://github.com/Hacking-the-Cloud/hackingthe.cloud/issues) on GitHub and it will be taken down quickly.__

There is one exception to this policy; If you are the original author of the article or blog post, you are welcome to copy the contents of it and include it here on Hacking the Cloud. This rule is intended to make it easy for authors to contribute their work without having to go through the trouble of editing/changing it. If it is later determined that the submitter is not the original author, the work will be removed.

## Content Removal Policy

If you are a researcher or author and you see that you blog/article has been linked to from Hacking the Cloud and would like it removed, please submit an [issue](https://github.com/Hacking-the-Cloud/hackingthe.cloud/issues) on GitHub and it will be removed. On a case-by-case basis the article will be considered for removal. Please note, however, that if the topic of the article is on a generic topic it is unlikely to be removed. For example, say an article is related to a privilege escalation technique. As a part of that article we may link to an external source as a reference or additional reading. If the author of the external source would like their link removed, it will be. However, the article itself will remain (so long as it is not plagiarized) as an individual cannot claim ownership of a generic technique.

## Getting Started

Hacking the Cloud uses Material for MkDocs and the Awesome Pages Plugin. To make it easy to setup, there is a Docker file in this repository you can use to get up and running. First, build the docker container.

```
docker build -t mkdocs-material .
```

To run a test server for your local environment you can run the Docker container (ensuring you expose a port and provide the local directory).

```
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs mkdocs-material
```

__NOTE__: You do not have to run the Docker container to contribute. You can make edits or even create new pages directly from GitHub. Go to the file you'd like to edit, or the directory you'd like to add to and click "Add File" in the mid-top right. Use the Markdown editor built into GitHub and submit your Pull Request.

## Using Cards

If you'd like to use a card, for [example](https://hackingthe.cloud/aws/post_exploitation/create_a_console_session_from_iam_credentials/) `Technique seen in the wild`, `Tools mentioned in this article`, etc, __please be aware that you would need a subscription for [Material for MKDocs](https://squidfunk.github.io/mkdocs-material/reference/grids/#using-card-grids) for the cards to be properly displayed on your local machine__. Simply copy and paste the template from the options below and it will be properly rendered on the site (we have a subscription to Material for MKDocs).

### Card Templates

```
<div class="grid cards" markdown>

-   :material-tools:{ .lg .middle } __Tools mentioned in this article__

    ---

    [](): Title

-   :material-account:{ .lg .middle } __Original Research__

    ---

    [](): Title

-   :material-account:{ .lg .middle } __Original Research__

    ---

    <aside style="display:flex">
    <p><a href="link">title</a> by <a href="profile link">name</a></p>
    <p><img src="image" alt="name" style="width:44px;height:44px;margin:5px;border-radius:100%;max-width:unset"></img></p>
    </aside>

-   :material-alert-decagram:{ .lg .middle } __Technique seen in the wild__

    ---

    Reference: []()

-   :material-book:{ .lg .middle } __Additional Resources__

    ---

    Reference: []()

-   :material-shield-lock:{ .lg .middle } __Required IAM Permissions__

    ---

    - []()

-   :material-shield-plus:{ .lg .middle } __Recommended but not Required IAM Permissions__

    ---

    - 

-   :material-link-box-outline:{ .lg .middle } __Technique Article__

    ---

    - 
</div>
```

## Creating a New Page

All of the content for Hacking the Cloud is in the "content" directory. From here, you can navigate to the different sections of each cloud provider. If you aren't sure what specific section to place it in, no worries! Feel free to put it under ./content and we can find or create a home for it later.

When creating a page, please give it a descriptive name like "get_account_id_from_keys.md" or "brute_force_iam_permissions.md". The file must be in Markdown so please also include the ".md" extension.

After creating the file, please put the following at the top and fill it out.

```
---
author_name: <Your Name>
title: <Page Title>
description: <A description of the page>
---
```

From here you should be able to write your content and submit a pull request. If you have any trouble don't hesitate to reach out via our GitHub Discussions page.
