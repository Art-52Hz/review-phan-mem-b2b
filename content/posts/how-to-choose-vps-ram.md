---
title: "How Much VPS RAM Do You Need (2026): Sizing by App with Real Plan Prices"
date: 2026-11-05
lastmod: 2026-11-27
slug: "how-to-choose-vps-ram"
summary: "Choose VPS RAM around your app, database and overlapping jobs. Compare Hostinger plans with UltaHost and check memory before upgrading."
description: "Choose VPS RAM for WordPress, Docker, n8n and databases. Compare Hostinger prices, renewal costs and practical checks before buying more memory."
keywords: ["how much ram does a vps need", "vps ram sizing", "4gb vs 8gb vps", "hostinger vps ram"]
categories: ["VPS Hosting", "Hosting Guide"]
tags: ["vps", "hostinger", "ram", "hosting"]
draft: false
toc: true
cover:
  image: "/images/thumbs/how-to-choose-vps-ram.webp"
  alt: "How Much RAM Does Your VPS Need? (2026) Sizing by Workload: aiprofreelancer.com guide cover"
  relative: false
---

For one small Linux app, shortlist 4 GB; for an app plus database and overlapping jobs, shortlist 8 GB. Choose by the busiest work that must run at the same time, then check the renewal bill: the displayed 24-month invoice is $112.56 for UltaHost Basic and $311.76 for Hostinger KVM 4.

**[Compare Hostinger plans for your RAM budget](https://www.hostinger.com/refer?REFERRALCODE=ACFTUNGSAAEO)** or **[compare UltaHost VPS options](https://ultahost.com/#art52hz)**.

Affiliate disclosure: Some links are affiliate links. We may earn a commission on qualifying purchases at no extra cost to you. Read our [disclosure](/affiliate-disclosure/).

Prices and listed resources below were checked on November 27, 2026. Recommendations are starting points, not measured performance claims.

## Current Linux plan costs, including renewal

Both providers display monthly-equivalent rates on 24-month terms paid upfront. The first invoice covers months 1-24. At month 24, the next 24-month renewal is charged. The 12- and 24-month columns therefore show the same cash already paid; month 36 includes the renewal invoice, which also pays for months 37-48.

| Plan | RAM / CPU | First 24-month invoice | Renewal invoice at month 24 | Cash paid by month 12 | Cash paid by month 24 | Cash paid by month 36 |
|---|---|---:|---:|---:|---:|---:|
| UltaHost VPS Basic | 1 GB / 1 core | $112.56 ($4.69 x 24) | $132.48 ($5.52 x 24) | $112.56 | $112.56 | $245.04 |
| UltaHost VPS Business | 2 GB / 2 cores | $199.44 ($8.31 x 24) | $234.72 ($9.78 x 24) | $199.44 | $199.44 | $434.16 |
| UltaHost VPS Professional | 4 GB / 3 cores | $323.76 ($13.49 x 24) | $380.88 ($15.87 x 24) | $323.76 | $323.76 | $704.64 |
| Hostinger KVM 1 | 4 GB / 1 vCPU | $155.76 ($6.49 x 24) | $287.76 ($11.99 x 24) | $155.76 | $155.76 | $443.52 |
| Hostinger KVM 2 | 8 GB / 2 vCPU | $210.96 ($8.79 x 24) | $359.76 ($14.99 x 24) | $210.96 | $210.96 | $570.72 |
| Hostinger KVM 4 | 16 GB / 4 vCPU | $311.76 ($12.99 x 24) | $695.76 ($28.99 x 24) | $311.76 | $311.76 | $1,007.52 |

Sources: [Hostinger VPS plan prices, resources and billing terms](https://www.hostinger.com/vps-hosting?REFERRALCODE=ACFTUNGSAAEO), checked November 27, 2026; [UltaHost VPS plan prices, resources and billing terms](https://ultahost.com/vps-hosting#art52hz), checked November 27, 2026. The 36-month cash total includes the full 24-month renewal invoice even though 12 months of that renewed term remain unused at month 36. Taxes and checkout changes are excluded.

These Linux plan cards show no mandatory paid software license or required add-on. Hostinger lists weekly backups in its plans; UltaHost lists a managed server. Paid control panels such as cPanel or Plesk may be optional selections, and their price is not included here. The table assumes no optional panel, domain, offsite backup or third-party software purchase.

The price difference is also a service difference: UltaHost includes managed-server service, while Hostinger's cards emphasize configurable KVM resources and weekly backups. A managed label does not define which application tasks support will perform, so confirm the scope before choosing it for client work.

## Which one should you pick?

- **One cached portfolio, API or small Linux app:** choose Hostinger KVM 1 if you can administer Linux and want 4 GB RAM for $155.76 upfront. Choose UltaHost Basic only if the app fits its 1 GB allocation and managed-server service matters more than extra memory.
- **WordPress with a local database, imports or several active plugins:** choose Hostinger KVM 1 as the starting shortlist, then measure checkout, search and scheduled imports together. Move to KVM 2 if those overlapping tasks leave little available memory.
- **Docker app plus database and worker:** choose Hostinger KVM 2. Its 8 GB gives the stack more room to overlap; set container limits and leave host memory for Linux. Read the [Docker VPS buying guide](/posts/best-vps-for-docker/) for storage and container costs.
- **n8n handling client webhooks, larger payloads or parallel runs:** choose Hostinger KVM 2 if you want one VPS for n8n, its database and simultaneous work. If runs are light, begin by reducing batch size and concurrency before paying for more RAM. See the [n8n VPS guide](/posts/best-vps-for-n8n/).
- **You need more than 4 GB but want to self-manage:** choose Hostinger KVM 2 for an 8 GB shortlist, or KVM 4 when monitoring shows a need for 16 GB. Compare the [KVM 1 vs KVM 2 plans](/posts/hostinger-kvm1-vs-kvm2-2026/) before moving up.

## Size memory from your own peak, not a visitor estimate

Record three values on the intended server: idle host memory with the full stack running, the added memory during your largest normal job, and the added memory when that job overlaps with real traffic or another scheduled task. Use the available-memory reading and logs, not just a high "used" number that includes reclaimable cache.

Write down what was running beside each peak. If a nightly import can be moved outside business hours, scheduling it may avoid buying a larger tier. If client requests, database work and automation must overlap, size for that overlap. Do not sum unrelated historic peaks that cannot happen together.

For containers, include the database and workers as separate running services. Docker says containers have no resource constraints by default; host memory pressure can lead the kernel to kill processes. Set realistic limits and leave room for the host. Its [resource constraints guide](https://docs.docker.com/engine/containers/resource_constraints/), checked November 27, 2026, notes that swap is slower than RAM and is a buffer rather than equivalent capacity.

n8n's [memory troubleshooting documentation](https://docs.n8n.io/hosting/scaling/memory-errors/), checked November 27, 2026, identifies JSON and binary data size, Code nodes, manual runs and overlapping workflows as factors that increase memory use. Smaller batches and fewer simultaneous executions may solve the pressure without a plan upgrade.

When an app reports out-of-memory errors, compare its logs with host available memory and container limits. If only one container reaches its limit, tune that limit or the app. If the host runs out during a representative overlap, shortlist the next plan size. Check CPU and storage at the same time: more RAM will not fix a CPU-bound job or slow disk work.

## FAQ

These questions reflect public [WordPress RAM discussions](https://www.reddit.com/r/webhosting/comments/1uck6ey/how_much_ram_does_a_wordpress_site_actually_need/) and [n8n VPS sizing discussions](https://www.reddit.com/r/VPS/comments/1x863vt/anyone_running_n8n_on_a_vps_what_specs_do_you_recommend/), including [a 2 GB n8n server struggling with overlapping workflows](https://www.reddit.com/r/n8n/comments/1xyf17k/selfhosted_n8n_on_a_2gb_vps_falls_over_when_three/). Community accounts are examples of questions and configurations, not universal capacity tests.

### Is 4 GB RAM enough for WordPress?

It can be a reasonable starting plan for one site, but traffic, plugins, database activity and background jobs change the peak. Measure checkout or imports as well as cached pages before relying on it.

### Do I need 8 GB for WordPress?

Not by default. Consider 8 GB when a database, multiple active sites or overlapping jobs push a 4 GB host into repeatable memory pressure. Optimize caching and schedule heavy imports first if they can run separately.

### Is 2 vCPU and 4 GB RAM enough to start n8n?

It is a practical starting size for light workflows, but large data, Code nodes and simultaneous runs can use more memory. If client workflows must run concurrently, shortlist 8 GB and monitor real executions.

### Why can n8n fail on a 2 GB VPS with only a few workflows?

Workflow count is not workload size. A few runs can overlap, process large binary or JSON payloads, or load execution data into the editor. Reduce batches and concurrency, then check n8n logs and container limits.

### Should I upgrade RAM or set n8n concurrency limits?

If overload happens only when several heavy executions overlap, cap or stagger those runs first. Upgrade when a representative single run or unavoidable overlap still exhausts available host memory.

**[Compare Hostinger plan prices and RAM](https://www.hostinger.com/refer?REFERRALCODE=ACFTUNGSAAEO) with [UltaHost managed VPS options](https://ultahost.com/#art52hz) before choosing a term.**
