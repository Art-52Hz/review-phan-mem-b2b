---
title: "WordPress Client Site Transfer: Ownership, Add-ons and Acceptance"
date: 2026-10-08
slug: "wordpress-client-site-transfer-checklist"
draft: false
description: "Prepare a single WordPress site transfer from an agency account to a client: receiving roles, DNS, add-ons, billing and acceptance evidence."
categories: ["Hosting"]
tags: ["WordPress", "client handoff", "freelancers"]
cover:
  image: "/images/wordpress-site-transfer.svg"
  alt: "Client site transfer checklist: receiving owner, dependencies and acceptance"
  relative: false
---

This guide is based on documentation, not a completed hosting transfer or recovery benchmark. It contains no affiliate referral link. Its worksheet is blank; untested results remain unknown.

Use this checklist when moving one client WordPress site out of an agency hosting account. If you are still choosing infrastructure, start with our [managed WordPress versus VPS responsibility guide](/posts/managed-wordpress-vps-hosting-2026/) and [client workload checklist](/posts/best-vps-for-freelancers-2026/). Here, the task is to define what the receiving client actually obtains.

## Separate the site from the company

Transferring a site and changing the owner of a company account are different operations. Identify the individual site and destination company before preparing a transfer. Do not transfer unrelated agency sites as part of one client's handoff.

Kinsta's [transfer documentation](https://kinsta.com/docs/company-settings/transfer-ownership/), read October 7, 2026, says a site transfer can be initiated by a Company Owner or Company Administrator. The receiving user needs an applicable company role. A company ownership change instead requires the Company Owner to initiate it.

## Map dependencies before acceptance

| Item | Question for the receiving owner | Evidence to record |
|---|---|---|
| Destination | Is this the intended client company and site? | Approved destination and receiving role |
| DNS | Is DNS managed in MyKinsta or elsewhere? | DNS owner and transfer scope |
| Add-ons | Which services follow the site and which stop? | Required services and destination availability |
| Billing | Could preserved capacity add a charge? | Destination quote and named cost approver |
| Operations | Who maintains integrations and responds to incidents? | Named operator and agreed scope |

The same Kinsta document says MyKinsta-managed DNS moves with the site. PHP, Redis and Premium staging add-ons transfer; other add-ons are disabled. It also describes an automatically applied PHP performance add-on when needed to preserve capacity above the destination plan's allowance. Review the destination cost before accepting. These are provider-specific rules, not promises for every hosting service.

## Agree acceptance before starting

Write down the pages, forms and integrations the receiving owner expects to work. Use only an authorized environment and appropriate sample data. Record the expected result, actual observation, unresolved problem and person responsible for each check. A successful account transfer alone does not prove the application works.

Keep domain registration, third-party DNS, plugin licenses and external email services on the dependency list until their ownership is confirmed separately. Do not assume every connected service is included in the hosting transfer.

## Keep recovery separate from transfer

Review the existing backup location, retention and recovery procedure with the incoming operator. If a recovery test has not been performed, mark it untested. Do not remove the agency's necessary access or cancel services until the client has reviewed the agreed acceptance evidence and open tasks.

Download the [blank site transfer worksheet](/downloads/wordpress-site-transfer-worksheet.txt). It records requirements and observations; it is not evidence that Kinsta or another provider passed a test. Keep passwords, tokens, billing details and private customer data out of the shared worksheet.

## Before calling the handoff complete

- The receiving owner can access the intended site under the agreed role.
- DNS, add-ons and outside dependencies have a named owner.
- Destination charges and ongoing maintenance responsibility are understood.
- Required workflows have recorded observations or explicit unresolved items.
- Access removal and service cancellation have a named decision maker.

No measured transfer time, performance score or commission is claimed here.

