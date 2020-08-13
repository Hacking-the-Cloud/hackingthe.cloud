---
author: "Nick Frichette"
title: "Role Chain Juggling"
description: "Keep your access by chaining assume-role calls"
enableEditBtn: true
editBaseURL: https://github.com/Hacking-the-Cloud/hackingthe.cloud/blob/master/content
---
Original Research: [Daniel Heinsen](https://twitter.com/hotnops)
Link to Tool: [GitHub](https://github.com/hotnops/AWSRoleJuggler/)

When doing an assessment in AWS you may want to maintain access for an extended period of time. You may not have the ability to create a new IAM user, or create a new key for existing users. How else can you extend your access? Role Chain Juggling.

[Role chaining](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html#Role%20chaining) is a recognized functionality of AWS in that you can use one assumed role to assume another one. When this happens the expiration field of the credentials is reset back to the original length. 

Through this, you can extend your access by chaining [assume-role](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/assume-role.html) calls.

{{< notice success "Note" >}}
You can chain the same role multiple times so long as the Trust Policy is configured correctly. Additionally, finding roles that can assume each other will allow you to cycle back and forth.
{{< /notice >}}