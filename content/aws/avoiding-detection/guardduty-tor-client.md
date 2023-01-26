---
author_name: Nick Frichette
title: "Bypass GuardDuty Tor Client Findings"
description: Connect to the Tor network from an EC2 instance without alerting GuardDuty.
hide:
  - toc
---

# Bypass GuardDuty Tor Client Findings

[UnauthorizedAccess:EC2/TorClient](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-ec2.html#unauthorizedaccess-ec2-torclient) is a high severity GuardDuty finding that fires when an EC2 instance is detected making connections to Tor [Guard](https://community.torproject.org/relay/types-of-relays/#Guard%20and%20middle%20relay) or Authority nodes. According to the documentation, "this finding may indicate unauthorized access to your AWS resources with the intent of hiding the attacker's true identity".

AWS determines this by comparing connections to the [public list of Tor nodes](https://metrics.torproject.org/exonerator.html). To those familiar with the Tor project, this is a common problem. Countries, internet service providers, and other authorities may block access to the Tor network making it difficult for citizens to access the open internet.

From a technical perspective the [Tor Project](https://www.torproject.org/) has largely gotten around this by using [Bridges](https://community.torproject.org/relay/types-of-relays/#Bridge). Bridges are special nodes that do not disclose themselves like other Tor nodes do. Individuals who would normally have difficulty connecting directly to Tor can instead route their traffic through Bridge nodes. Similarly, we can bypass the Tor Client GuardDuty finding by using bridges.

To do so, download the Tor and obfs4proxy binaries (the simplest way to do this on a Debian based system is `apt install tor obfs4proxy` and move them to your target). [Obfs4](https://gitlab.com/yawning/obfs4) is a [Pluggable Transport](https://2019.www.torproject.org/docs/pluggable-transports.html.en) which modifies Tor traffic to communicate with a bridge. Navigate to [bridges.torproject.org](https://bridges.torproject.org/options) to get a bridge address. 

From here, create a torrc file with the following contents (being sure to fill in the information you got for the bridge address):

```
UseBridges 1
Bridge obfs4 *ip address*:*port* *fingerprint* cert=*cert string* iat-mode=0
ClientTransportPlugin obfs4 exec /bin/obfs4proxy
```

You will now be able to connect to the Tor network with `tor -f torrc` and you can connect to the Socks5 proxy on port 9050 (by default).