---
author_name: Moses Frost (@mosesrenegade)
title: Hunting GCP Buckets
description: How to find valid and invalid GCP Buckets using tools
hide:
  - toc
---

# Hunting GCP Buckets

GCP Buckets are almost 100% identical to AWS S3 Buckets. 

*Theory*: This call is based on OpenStack; maybe most cloud environments will be the same.

Using @digininja's [CloudStorageFinder](https://github.com/digininja/CloudStorageFinder) diff the following files:

`diff bucket_finder.rb google_finder.rb`

The main differences are the URLs:

- AWS Supports HTTP and HTTPS
- `AWS S3` URLs: `http://s3-region.amazonaws.com`, i.e.: `http://s3-eu-west-1.amazonaws.com`.
- GCP Endpoint: `https://storage.googleapis.com`

How to find buckets using CloudStorageFinder:

Create a wordlist with any name; in our example, it is `wordlist.txt`.

$ `ruby google_finder.rb wordlist.txt`
