---
title: "Best VPS for Self-Hosted n8n (2026): RAM Needs and Monthly Cost"
date: 2026-10-30
lastmod: 2026-10-30
slug: "best-vps-for-n8n"
summary: "Choose a VPS for n8n by memory, upfront payment, renewal and maintenance responsibility, with Hostinger and UltaHost compared."
draft: false
description: "Best VPS for self-hosted n8n: Hostinger KVM 1 vs KVM 2, UltaHost alternatives, RAM planning, monthly-equivalent prices and a practical workload check."
keywords: ["best vps for n8n", "n8n ram requirements", "n8n hosting cost", "self hosted n8n vps"]
categories: ["VPS Hosting", "Hosting Guide"]
tags: ["vps", "hostinger", "n8n", "automation"]
toc: true
cover:
  image: "/images/vps-client-operations.svg"
  alt: "VPS checklist covering access, backups and recovery for automation"
  relative: false
---

**Best for a small n8n deployment you can administer: Hostinger KVM 1. Choose KVM 2 for more room when adding a database or overlapping jobs. Pick UltaHost instead if an agreed managed-server support scope matters more than RAM per dollar.**

**[See Hostinger VPS plans](https://www.hostinger.com/refer?REFERRALCODE=ACFTUNGSAAEO)**

*Affiliate disclosure: Hostinger links marked as recommendations are referral links. An eligible purchase may earn us a commission at no extra cost to you. [Read our disclosure](/affiliate-disclosure/).*

Based on official documentation and public USD pricing checked October 30, 2026; plan choices below are editorial recommendations, not measured capacity guarantees.

## Compare the bill and resources first

The table uses the official [Hostinger pricing source](https://www.hostinger.com/vps-hosting) and [UltaHost pricing source](https://ultahost.com/vps-hosting), checked October 30, 2026. Both display long-term offers here. A monthly-equivalent price is different from a monthly payment.

| Buyer criterion | Hostinger KVM 1 | Hostinger KVM 2 | UltaHost VPS Business |
|---|---|---|---|
| Advertised rate, 24-month term | $6.49/month | $8.79/month | $9.78/month |
| Renewal rate shown | $11.99/month, same term | $14.99/month, same term | $9.78/month for 2 years |
| RAM | 4 GB | 8 GB | 2 GB DDR5 |
| CPU | 1 vCPU | 2 vCPU | 2 CPU cores |
| NVMe storage | 50 GB | 100 GB | 50 GB |
| Trial or refund | Paid; 30-day money-back headline | Paid; 30-day money-back headline | Paid; 30-day headline, verify selected-term eligibility |
| Main limit | Self-managed; smaller resource budget | Self-managed; higher upfront payment | Less memory; confirm application support |
| Best fit | Small, focused automation stack | Database and concurrent-job headroom | Buyer prioritizing server assistance |

Hostinger lists **$155.76 upfront** for KVM 1 and **$210.96 upfront** for KVM 2. The latter adds **$55.20** to the initial bill, calculated from those displayed totals. Taxes, add-ons and the actual checkout selection can change the invoice. These public prices do not assume an extra referral discount.

UltaHost also advertises VPS Basic at **$5.52/month with 1 GB RAM** on its two-year card. It is cheaper, but buying the smallest memory allocation just to lower the headline bill is a poor default for an automation stack. Business is the more useful comparison when evaluating its managed positioning. Ask about the exact renewal, prepayment and refund conditions before choosing a term.

## How much RAM does self-hosted n8n need?

There is no useful universal workflow count that turns a VPS specification into guaranteed capacity. A scheduled notification and a workflow importing large attachments create very different resource demands.

The official [n8n memory troubleshooting guide](https://docs.n8n.io/hosting/scaling/memory-errors/), checked October 30, 2026, identifies payload size, binary files, Code nodes and concurrent executions as memory drivers. It also explains why manual executions use extra memory for the editor. That makes your largest payload and busiest overlap more useful buying inputs than the number of saved workflows.

My buying recommendation is to consider **4 GB** as a starting budget for a small dedicated deployment and **8 GB** when you want more space for supporting services. These are the Hostinger plan sizes in the dated table above, not minimum requirements published by n8n. Validate the fit with your own workload before committing business-critical automations.

Think about memory in separate buckets: the operating system, n8n itself, its execution data, and any additional database or service. A server with generous headline RAM can still struggle if a container has a tight memory limit or the workflow repeatedly loads an entire dataset.

For an AI workflow, distinguish calling an external model API from running a model on the VPS. The recommendations here concern orchestration and API calls. Choose infrastructure for a locally hosted model separately; a general n8n VPS recommendation does not establish that model's hardware needs.

## Who should choose Hostinger, and who should not?

**Choose KVM 1** if your goal is a focused installation: scheduled API requests, webhook handling or a modest internal process, and you can inspect logs and maintain the server. Keep unrelated applications elsewhere until you understand the workload.

**Choose KVM 2** if the same machine will host a separate database, additional containers, or workflows that may overlap. The extra resources buy flexibility, while the larger prepaid bill is the tradeoff. For more detail on that decision, read our [Hostinger KVM 1 vs KVM 2 comparison](/posts/hostinger-kvm1-vs-kvm2-2026/).

Hostinger's [official n8n template guide](https://www.hostinger.com/support/10473267-how-to-use-the-n8n-vps-template-at-hostinger/), checked October 30, 2026, describes a preinstalled Docker environment. That helps with initial deployment, but it does not remove ongoing administration. Its [VPS management explanation](https://www.hostinger.com/support/8311982-what-is-managed-hosting-in-hostinger/), checked the same day, identifies VPS hosting as self-managed.

**Do not choose a self-managed VPS** if nobody owns patching, backups and recovery. A template can get software running; someone must still decide when to update it and what to do when a workflow fails. Hostinger also offers a separate Managed n8n product, described in its [managed application documentation](https://www.hostinger.com/support/hostinger-managed-n8n-overview-and-setup/), checked October 30, 2026. Verify which product you are ordering rather than treating the two as interchangeable.

**[Compare Hostinger plans for your n8n stack](https://www.hostinger.com/refer?REFERRALCODE=ACFTUNGSAAEO)**

## When UltaHost makes more sense

UltaHost markets its VPS range as managed. Shortlist it when assistance with the server is worth more to you than the larger memory allocation in the Hostinger offers above. Ask whether its team supports your intended Docker setup, database, backup restoration and upgrade process.

Turn that conversation into a concrete responsibility list. Who patches the operating system? Who updates the application? Who restores credentials and data after a failed change? A general promise of support does not answer those questions for a custom workflow.

For this comparison, Hostinger wins on the displayed memory allocation at a lower introductory rate than UltaHost Business. UltaHost can still be the better purchase if the support tasks you need are explicitly included. Our broader [UltaHost vs Hostinger comparison](/posts/ultahost-vs-hostinger-vps-2026/) covers that operating-responsibility decision.

## What belongs in your monthly cost budget?

Use the renewal rate as your baseline for keeping the service, and treat prepayment as a separate cash-flow decision. A low equivalent monthly rate can be unsuitable if you only need a short experiment.

Add any domain renewal, independent backup storage, paid application features and external API usage to your budget. A VPS invoice does not pay the services your workflow calls. Keep those expenses visible so an automation that saves time does not quietly become expensive to operate.

Also decide how much execution history you need to retain. Logs, files and backups need an owner and a retention policy. Avoid storing sensitive payloads indefinitely simply because disk space is available. Our [Hostinger discount and renewal guide](/posts/hostinger-vps-coupon-discount/) helps separate the public offer from the ongoing bill.

## How to test it yourself in 15 minutes

Use this as an initial check **after a test instance is provisioned**, not a promise that purchase, installation and production validation fit into that time.

1. Open the editor over HTTPS and create a disposable workflow using sample data. Keep live customer credentials and outgoing messages out of the first check.
2. Reproduce the shape of your intended job: an incoming request, data transformation and a harmless response. Include a representative payload rather than only a tiny example.
3. Observe memory and CPU in the server dashboard, and container usage if available. Record the idle state and what changes while the job runs.
4. Check an overlap similar to your expected schedule. Look for failed executions, restarts and delayed work. If an external API fails, separate its rate limits from server resource problems.
5. Restart the application in the test environment and confirm the saved workflow remains available. Then write down how you would restore the database, persistent files and encryption key from backup.

A successful short check establishes basic behavior only. Before relying on the system, observe a representative business cycle and perform a recovery drill. Save the workflow shape, payload description, server configuration and observations so the next upgrade decision has evidence.

<!-- FIRST-HAND: cần ảnh hoặc số đo thật: capture a redacted resource dashboard, representative workflow/payload, concurrent execution observations and a backup restoration result on the selected VPS. -->

## FAQ

These questions follow the public installation FAQ topics in [Hostinger's n8n tutorial](https://www.hostinger.com/uk/tutorials/how-to-install-n8n/) and the official n8n hosting and memory guides, checked October 30, 2026.

### Which VPS plan should I choose for n8n?

Start by evaluating KVM 1 for a small dedicated stack. Consider KVM 2 when adding supporting services or overlapping jobs. Make the final decision from observed resource use and your ability to operate the server.

### Is 4 GB of RAM enough for n8n?

It is a reasonable starting allocation to evaluate, rather than a guarantee. Large payloads or concurrent executions can change the requirement. Reduce unnecessary data in the workflow and inspect resource use before deciding that more hardware is the only fix.

### How much does hosting n8n on Hostinger cost?

The October 30, 2026 public VPS source above lists KVM 1 at $6.49/month equivalent on a prepaid term and KVM 2 at $8.79. Budget for their renewal rates and external services as well as the initial invoice.

### Can I run n8n locally before buying a VPS?

Yes. The official [n8n self-hosting documentation](https://docs.n8n.io/hosting/), checked October 30, 2026, includes local deployment options. Local experimentation helps you understand a workflow; an always-on public service also needs reliable availability, HTTPS and operational care.

### How do I access n8n after installing the template?

Follow the hostname and HTTPS instructions in the official template guide linked above, then complete the initial owner setup. Before connecting external webhooks, confirm the public address is correct and the application remains accessible after a restart.

**Ready to run and maintain your own instance? [Start with the Hostinger plan that fits your n8n workload](https://www.hostinger.com/refer?REFERRALCODE=ACFTUNGSAAEO).**
