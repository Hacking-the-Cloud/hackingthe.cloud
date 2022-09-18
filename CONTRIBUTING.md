# Contributing

## Plagiarism Policy

All content submitted to Hacking the Cloud must be written in your own words. Submissions which appear to include plagiarized material (copying and pasting of whole articles/blog posts) will be rejected. It is okay to quote an existing article (with the reference). The goal of Hacking the Cloud is to congregate knowledge for the community into a single location. This includes having links/references to primary sources.

__If you are an author and believe your work has been plagiarized on Hacking the Cloud, please submit an [issue](https://github.com/Hacking-the-Cloud/hackingthe.cloud/issues) on GitHub and it will be taken down quickly.__

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

## Creating a New Page

All of the content for Hacking the Cloud is in the "content" directory. From here, you can navigate to the different sections of each cloud provider. If you aren't sure what specific section to place it in, no worries! Feel free to put it under ./content and we can find or create a home for it later.

When creating a page, please give it a descriptive name like "get_account_id_from_keys.md" or "brute_force_iam_permissions.md". The file must be in Markdown so please also include the ".md" extension.

After creating the file, please put the following at the top and fill it out.

```
---
author: <Your Name>
title: <Page Title>
description: <A description of the page>
---
```

From here you should be able to write your content and submit a pull request. If you have any trouble don't hesitate to reach out via our GitHub Discussions page.