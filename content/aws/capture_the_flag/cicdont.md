---
author: Nick Frichette
title: CI/CDon't
description: An AWS/GitLab CICD themed CTF.
---

Link to Project: [CI/CDon't](https://github.com/Hacking-the-Cloud/htc-ctfs/tree/main/aws/cicdont)

!!! Note
    This project will deploy intentionally vulnerable software/infrastructure to your AWS account. Please ensure there is no sensitive or irrecoverable data in the account. Attempts have been made to mitigate this however they may not be fullproof; Security Group rules only allow access to the vulnerable EC2 instance from your public IP address, and a randomly generated password is required to access it.

!!! Warning
    If you intend to play the CTF it is a good idea to read through this page carefully to ensure you have all the details (minus the walkthrough). This writeup will familiarize the player with how the CTF works, what the objective is, and what the storyline is.

## Background

This is an AWS/GitLab CI/CD themed CTF that you can run in your own AWS account. All that is required is an AWS account and Terraform [installed](https://learn.hashicorp.com/tutorials/terraform/install-cli) locally on your machine.

Costs should be minimal, running this infrastructure in my own account for two hours didn't accrue a cent in the Billing Dashboard, however extended time frames may cause costs to add up.

In terms of difficulty, it would be rated low. The goal is more about having fun and working through some simple CI/CD/AWS challenges that even non-security folks would enjoy.

## How to Play

Clone this repository and navigate to the cicdont directory.

```
git clone https://github.com/Hacking-the-Cloud/htc-ctfs.git
cd htc-ctfs/aws/cicdont
```

To deploy the CTF environment run the Terraform init/apply command.

```
terraform init
terraform apply
```

You will be prompted with two questions. The first is a consent related to the costs of the CTF (Again, these should be minimal however the environment should still be taken down when you're finished with it). The second is asking your player name. Please do not use special characters in the name, only upper and lower case letters. This will be used in the game.

!!! Note
    It will take approximately 10 minutes for all the infrastructure to be deployed and ready. This 10 minute timer begins AFTER the Terraform apply has completed. This time is used to install all the software, create the NPCs, etc.

!!! Warning
    To be able to access the vulnerable instance, Terraform will attempt to determine your public IP address and create a security group that only that IP address can access. If you cannot access the target_ip (explained below) after 10 minutes, check the AWS console for a security group named `allow_http` and ensure that it's configuration would allow you to reach it.

To destroy the CTF environment run the Terraform destroy command.

```
terraform destroy
```

This will again prompt you for the two questions. Please answer them and the infrastructure will be destroyed.

## The Important Bits

Once you've run terraform apply, you will receive 5 outputs. This will include the following:

* Player Username
* Player Password (randomly generated)
* Attackbox IP
* Target IP
* Time warning

The attackbox is an EC2 instance you can use for whatever purposes you deem fit. In particular you can use it to catch a reverse shell, or load your C2 platform of choice on it (you have sudo access via the password).

To access the attackbox, you can ssh using your player username and password.

```
ssh <player username>@<attackbox IP>
```

!!! Note
    When sshing with a player username, note that the username is case-sensitive.

It will take approximately 10 minutes for all the infrastructure to finish deploying. If you'd like to test if it's finished, you can navigate to `http://<target IP>/`. If it doesn't respond, or only shows a generic GitLab log in page, then the CTF is not ready yet. If you see a message about SoftHouseIO, then everything is setup and ready.

Please Note: To be able to access the vulnerable instance, Terraform will attempt to determine your public ip address and create a security group that only that ip address can access. If you cannot access the target_ip (explained below) after 10 minutes, check the AWS console for a security group named `allow_http` and ensure that it's configuration would allow you to reach it.

!!! Note
    To be able to access the vulnerable instance, Terraform will attempt to determine your public IP address and create security group rules that only that IP address can access. If you cannot access the target instance after 10 minutes (likely shorter), check the AWS console for a security group named `allow_http` and ensure that ti's configuration would allow you to reach it.

    These security group rules apply to both the target (GitLab) and the attackbox. Additionally, the rules are configured to allow the attackbox to receive incoming traffic from the target (to catch shells).

If you see any references to gamemaster, please ignore it. Those scripts are used to simulate the NPCs and have them complete their lore tasks. It is unrelated to the challenge.

## The Story

You are <player username>, a developer at SoftHouseIO, an independent software development consultancy firm. Recently, things haven't been going your way, and you're looking for a payday.

What if you leverage your access as a developer to gain access to company resources? Can you say cryptominer?

The best place to get started is probably the company GitLab server at http://<target IP>. Your username and password should you get you in.

## The Objective

Gain access to the terraform_admin_user through whatever means necessary (Note that this role has no permissions. It is simply the goal).

## Walkthrough

The following is a step by step walkthrough of the CTF. You can refer to this if you get stuck or simply just want to know what is next. Click the summary below to expand it.

??? Summary
    **Consent and Name**

    To begin the CTF we must first stand up all the infrastructure. We do this using Terraform.

    Download the challenge using git.
    ```
    git clone https://github.com/Hacking-the-Cloud/htc-ctfs.git
    cd htc-ctfs/aws/cicdont
    ```

    Initialize the project.
    ```
    terraform init
    ```

    Create the infrastructure.
    ```
    terraform apply
    ```

    We will be prompted first with a consent. Read through the question and answer with yes or no.

    After this, it will ask for a player name. Please only use lower and uppercase letters. No special characters or numbers.

    ![Consent Message](/images/aws/capture_the_flag/cicdont/consent.png)

    After this, you will be asked if you'd like to perform the deployment. Answer with "yes".

    The Terraform deployment will begin.

    **Wait**

    !!! Note
        You will now need to wait 10 minutes for the deployment to finish. The 10 minute timer starts **AFTER** you get the "Apply complete" notification.

    ![Output](/images/aws/capture_the_flag/cicdont/output.png)

    Does it really take 10 minutes? Yes, it takes a little bit to get everything setup. You can take this time to get familiar with your attackbox. This is an EC2 instance you can use for whatever you need during the CTF, particularly to catch shells.

    You can ssh into the box using your username and password

    ```
    ssh <player_username>@<target_ip>
    ```

    !!! Note
        The username is case-sensitive.

    **Getting Started**

    After waiting those 10 minutes, you finally have a target. You can navigate to the target_ip to see a GitLab instance. Log in using your player username and password.


## Acknowledgements

These wonderful folks helped beta-test this CTF and provided feedback.

[Christophe Tafani-Dereeper](https://twitter.com/christophetd)  
[Jake Berkowsky](https://twitter.com/JBerkowsky)  
[Kaushik Pal](https://github.com/kaushik853)