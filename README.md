# hackingthe.cloud ![Deploy](https://github.com/Hacking-the-Cloud/hackingthe.cloud/workflows/Deploy/badge.svg) 
Hacking the cloud is an encyclopedia of the attacks/tactics/techniques that offensive security professionals can use on their next cloud exploitation adventure. The goal is to share this knowledge with the security community to better defend cloud environments.

All content on this site is created by volunteers. If you'd like to be one of them, you can contribute your knowledge by submitting a [Pull Request](https://github.com/Hacking-the-Cloud/hackingthe.cloud/pulls). We are open to content from any major cloud provider and will also accept cloud-related technologies as well (Docker, Terraform, K8s, etc.). Additionally you are encouraged to update/modify/improve existing pages as well.

Topics can include offensive techniques, tools, general knowledge related to cloud security, etc. **Defensive knowledge is also welcome!** At the end of the day the primary goal is to make the cloud safer, and defenders are welcome to submit content all the same.

Don't worry about submitting content in the wrong format or what section it should be a part of, we can always make improvements later :) When writing content: do try to credit the researcher who discovered it and link to their site/talk. 

## Contributing
Want to contribute to hacking the Cloud? Awesome! Here are some tips to get started:

### Setting up the Environment
Hacking the Cloud uses [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) and the [Awesome Pages Plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin/). To make it easy to setup, there is a Docker file in this repository you can use to get up and running. First, build the docker container.

```
docker build -t mkdocs-material .
```

To run a test server for your local environment you can run the Docker container (ensuring you expose a port and provide the local directory).

```
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs mkdocs-material
```

__NOTE__: You do not have to run the Docker container to contribute. You can make edits or even create new pages directly from GitHub. Go to the file you'd like to edit, or the directory you'd like to add to and click "Add File" in the mid-top right. Use the Markdown editor built into GitHub and submit your Pull Request.

### Creating a New Page
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

From here you should be able to write your content and submit a pull request. If you have any trouble don't hesitate to reach out via our [GitHub Discussions](https://github.com/Hacking-the-Cloud/hackingthe.cloud/discussions) page.

## Roadmap
Currently the site has some material on AWS, and very little for Azure or GCP. If you have experience in any of those areas you are welcome to submit content. Even something as small as fixing grammar mistakes or adding a screenshot is appreciated!
