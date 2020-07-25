---
author: "Nick Frichette"
title: "AWS Consoler"
description: "Leverage stolen credentials to use the AWS Console"
---
Author: Nick Frichette
Original Research: [Ian Williams](https://blog.netspi.com/gaining-aws-console-access-via-api-keys/)
Link to Tool: [GitHub](https://github.com/NetSPI/aws_consoler)

When performing an AWS assessment you will likely encounter IAM Credentials. Traditionally, the majority of these that you would find would only be usable from the AWS CLI. Using a tool called [AWS Consoler](https://github.com/NetSPI/aws_consoler) you can create links that will allow you to access the AWS Console. In this example we will walk through gathering credentials and using those credentials along with Consoler to generate a Console link.

First, we need to gather valid IAM credentials. These are typically found a number of different ways. In this example, we have shell access to an EC2 instance with an attached role and we will curl the metadata service to access them.

![Stolen Credentials](/images/aws/persistence/aws_consoler/stolen_credentials.png)

Next, install and compile [AWS Consoler](https://github.com/NetSPI/aws_consoler) (install Python dependencies with pip and then do a sudo make install).

From here invoke the Consoler tool and provide the -a (access key) -s (secret access key) and -t (session token) flags along with the retrieved values.

![Command](/images/aws/persistence/aws_consoler/command.png)

This will generate a link you can use to access the AWS Console.

![link](/images/aws/persistence/aws_consoler/link.png)

![proof](/images/aws/persistence/aws_consoler/proof.png)
