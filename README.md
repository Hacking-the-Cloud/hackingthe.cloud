# hackingthe.cloud ![Deploy](https://github.com/Hacking-the-Cloud/hackingthe.cloud/workflows/Deploy/badge.svg) 
Hacking the cloud is a encyclopedia of the attacks/tactics/techniques that offensive security professionals can use on their next cloud exploitation adventure. The goal is to share this knowledge with the security community to better defend cloud environments.

All content on this site is created by volunteers. If you'd like to be one of them, you can contribute your knowledge by submitting a [Pull Request](https://github.com/Hacking-the-Cloud/hackingthe.cloud/pulls). We are open to content from any major cloud provider and will also accept cloud-related technologies as well (Docker, Terraform, K8s, etc.). Additionally you are encouraged to update/modify/improve existing pages as well.

Topics can include offensive techniques, tools, general knowledge related to cloud security, etc. **Defensive knowledge is also welcome!** At the end of the day the primary goal is to make the cloud safer, and defenders are welcome to submit content all the same.

Don't worry about submitting content in the wrong format or what section it should be a part of, we can always make improvements later :) When writing content: do try to credit the researcher who discovered it and link to their site/talk. 

## Contributing
Want to contribute to hacking the Cloud? Awesome! Here are some tips to get started:

### Setup Hugo
Hacking the Cloud is built using [Hugo](https://gohugo.io/), which lets us write content in a simple Markdown editor. If you've not worked with Markdown before check out this handy [cheatsheet](https://www.markdownguide.org/cheat-sheet) or look to existing examples on Hacking the Cloud.

**Please Note**: You do not have to install Hugo to contribute to the site. You can also use GitHub itself to create new pages (Go to the directory you'd like to add to and click "Add File" in the mid-top right). This lets you use the Markdown editor in GitHub (which is very handy).

To install Hugo, please checkout [these](https://gohugo.io/getting-started/installing/) installation instructions.

After installing Hugo, you can setup an instance of Hacking the Cloud by cloning the git repository and starting the Hugo server with the following commands.

```
git clone https://github.com/Hacking-the-Cloud/hackingthe.cloud.git
hugo server
```

In this mode, every time you modify a file Hugo will automatically update the site. This makes it easy for you to see you changes as they occur.

To navigate to the local instance, go to http://localhost:1313 in your browser of choice.

### Creating a New Page
All of the content for Hacking the Cloud is in the "content" directory. From here, you can navigate to the different sections of each cloud provider. If you aren't sure what specific section to place it in, no worries! Feel free to put it under ./content and we can find or create a home for it later.

When creating a page, please give it a descriptive name like "get_account_id_from_keys.md" or "brute_force_iam_permissions.md". The file must be in Markdown so please also include the ".md" extension.

After creating the file, please put the following at the top and fill it out.

```
---
author: <Your Name>
title: <Page Title>
description: <A description of the page>
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/main/content
---
```

These fields help Hugo generate the site and provide additional information for SEO. The enableEditBtn must always be set to true (in the future we may find a way to remove this attribute with the button just always enabled).

From here you should be able to write your content and submit a pull request. If you have any trouble don't hesitate to reach out via our [GitHub Discussions](https://github.com/Hacking-the-Cloud/hackingthe.cloud/discussions) page.

## Roadmap
Currently the site has some material on AWS, and very little for Azure or GCP. If you have experience in any of those areas you are welcome to submit content. Even something as small as fixing grammar mistakes or adding a screenshot is appreciated! In the future I'd like to expand the site to include labs for folks to get hands-on experience with the content.
