---
author_name: Nick Frichette
title: AWS CLI Tips and Tricks
description: A collection of tips and tricks for using the AWS CLI.
---

# AWS CLI Tips and Tricks

## Standard Input/Output Redirection with "-"

!!! Warning
    The following examples have been tested in [bash](https://www.gnu.org/software/bash/) and [zsh](https://zsh.sourceforge.io/). Functionality may vary in other shells. If you find these commands work in additional environments, please open a pull request to update this note.

When working in an AWS environment, you may frequently need to view the contents of objects stored in S3. The traditional approach involves a two-step process: using [s3:cp](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/s3/cp.html) to download the file to your local machine, then using `cat` or a similar tool to view it. While effective, this method can clutter your local system with temporary files and may be slower than necessary.

Fortunately, the AWS CLI allows us to simplify this process by using the `-` [character](https://www.baeldung.com/linux/dash-in-command-line-parameters) which represents standard input/output (STDIN/STDOUT). Using `-`, you can read or write file content directly from or to S3 without creating local copies.

### Reading from S3

To read the contents of an object stored in S3 without having to download it first, use the following command:

```bash
aws s3 cp s3://bucket-name/object-key -
```

Example:

```bash
nick@host:~$ aws s3 cp s3://hackingthecloud/content -
hacking the cloud
```

### Writing to S3

To upload content directly to an object in S3 without a temporary file, use this command:

```bash
echo "hacking the cloud" | aws s3 cp - s3://bucket-name/object-key
```

This command writes the specified text to an S3 object, again bypassing the need for a local file.

## Modifying the CloudTrail Log User-Agent with `AWS_EXECUTION_ENV`

!!! example "Shout-out"
    Shout-out to [Christophe Tafani-Dereeper](https://christophetd.fr/) for showing me this.

When making API calls to AWS, a `User-Agent` header is included in each request, containing details about the client making the request. Although it’s not possible to fully [customize](https://github.com/aws/aws-cli/issues/3990) this header, you can append information to it, which can be useful for tracking API calls in CloudTrail logs.

One way to modify the `User-Agent` is by setting the `AWS_EXECUTION_ENV` environment variable, used by AWS SDKs to identify the execution environment. Tools like [grimoire](https://github.com/DataDog/grimoire) leverage this variable to append custom information to the `User-Agent` header, making API tracking more informative.