---
title: "UltaHost Windows VPS (2026): Plans, License Cost and RDP Setup"
date: 2026-11-09
lastmod: 2026-11-24
slug: "ultahost-windows-vps"
draft: false
description: "Compare UltaHost Windows VPS plans, verify license and renewal costs, and set up a safer RDP connection. See which plan fits your workload."
keywords: ["UltaHost Windows VPS", "UltaHost Windows license", "Windows VPS RDP setup"]
categories: ["Hosting", "VPS"]
tags: ["UltaHost", "Windows VPS", "RDP", "Freelancers"]
cover:
  image: "/images/dedicated-server-quote.svg"
  alt: "Hosting quote checklist for hardware, full cost and operating responsibility"
  relative: false
---

For one modest Windows application, shortlist UltaHost Basic; choose Business when 4 GB RAM better fits the software requirements. Windows Server Standard is included, but that does not establish multi-user RDS or application licensing. The live page currently shows Basic at $16.10/mo on its selected 24 month term, renewing at the same rate, or $386.40 for 24 months before checkout taxes or extras.

**Affiliate disclosure:** Some links are affiliate links. We may earn a commission on qualifying purchases. [Read our disclosure](/affiliate-disclosure/).

{{< picks title="Which one should you pick?" checked="Nov 24, 2026" >}}
{{% pick label="Choose Basic if" name="UltaHost Basic Windows VPS" price="$16.10/mo - $386.40 for 24 months" renew="$16.10/mo for 2 years" note="Check the 30-day refund terms and exact invoice before paying" %}}
Pick Basic for one Windows-only utility or a small trading terminal when the software vendor's requirements fit 2 cores, 2 GB RAM and 50 GB NVMe. [See UltaHost plans](https://ultahost.com/#art52hz "affiliate") before choosing a term.
{{% /pick %}}
{{% pick label="Choose Business if" name="UltaHost Business Windows VPS" price="$24.14/mo - $579.36 for 24 months" renew="$24.14/mo for 2 years" note="Check the 30-day refund terms and exact invoice before paying" %}}
Choose Business if the application vendor recommends more than 2 GB RAM or you will run a second service alongside the desktop. [Compare UltaHost plans](https://ultahost.com/#art52hz "affiliate") against the documented workload.
{{% /pick %}}
{{% pick label="Choose another setup if" name="Linux VPS or separately licensed multi-user RDS" price="Quote required" note="Get written confirmation of software and access licensing" %}}
Use Linux when the workload supports it and you can administer it; get a written quote before planning several simultaneous Windows desktop users. [Start with UltaHost plans](https://ultahost.com/#art52hz "affiliate") only after the required access model is clear.
{{% /pick %}}
{{< /picks >}}

## Current plan prices and resources

The live page has a billing selector for monthly, yearly, two years and three years. Its currently retrieved card shows the two-year selection. The card says the displayed rate renews for two years at the same rate.

| Windows VPS plan | Displayed monthly price | CPU / RAM / NVMe | Best fit |
|---|---:|---|---|
| Basic | $16.10 | 2 cores / 2 GB / 50 GB | One narrow Windows workload |
| Business | $24.14 | 2 cores / 4 GB / 80 GB | More memory for an application and background service |
| Professional | $33.93 | 3 cores / 6 GB / 150 GB | Workload needing more CPU and storage |

Source: [UltaHost Windows VPS plan specifications and displayed prices](https://ultahost.com/windows-vps#art52hz), checked November 24, 2026. The page headline separately says it starts at $16.10/mo, matching Basic's selected two-year rate.

## What the full cost looks like

The official page exposes its selected two-year plan card and states the rate it renews at. It does not disclose the yearly and three-year card totals in the retrieved page text, nor taxes or required extras. The 12 and 36 month cells are left unverified instead of multiplying a rate from another term.

| Basic Windows VPS term | Rate shown by official page | Server charge for term | Renewal and extras |
|---|---:|---:|---|
| 12 months | Not displayed in retrieved listing | Not verified | Renewal amount not displayed |
| 24 months | $16.10/mo | $386.40 | Renews at $16.10/mo for 2 years; taxes and extras not specified |
| 36 months | Not displayed in retrieved listing | Not verified | Renewal amount not displayed |

Windows Server is included in the plan according to UltaHost. RDS access for additional users and paid desktop applications are not established as included. For a true total, ask sales for the selected term's amount due today, the same-term renewal, Windows edition, remote-user licensing, taxes, and each required add-on. The [UltaHost pricing and refund guide](/posts/ultahost-coupon-and-pricing/) explains what to reconcile on the quote.

## Windows license and RDP users

UltaHost says each Windows VPS includes a purchased Windows Server Standard edition and that it bears the operating-system purchase cost. That answers the OS line item, not every license in a remote desktop setup. Source: [UltaHost Windows VPS licensing FAQ](https://ultahost.com/windows-vps#art52hz), checked November 24, 2026.

Microsoft describes RDS Client Access Licenses for users or devices connecting to an RDS Session Host. Do not infer from a working administrator session that a team desktop deployment is covered. Give UltaHost your user count and access model, then request the hosted licensing answer in writing. Source: [Microsoft RDS client access licensing](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/rds-client-access-license), checked November 24, 2026. A recent [Reddit question about Windows VPS RDP CALs](https://www.reddit.com/r/VPS/comments/1xb6aei/need_vps_rdp_cal/) illustrates the same practical distinction between included OS licensing and multi-user access, checked November 24, 2026.

Check separately whether your desktop application allows commercial hosting or remote use. Record its license terms with the server order so the next administrator knows what was approved.

## RDP setup checklist

1. Match the server address and Windows edition to the order. Save the provider's recovery-console route before changing firewall settings.
2. Enable Remote Desktop only for the intended account. Use a unique password and keep Network Level Authentication enabled.
3. Restrict inbound RDP in both the provider firewall and Windows firewall, ideally to a VPN or trusted IP addresses.
4. On Windows, open Remote Desktop Connection, enter the server address and sign in with the assigned credentials.
5. Confirm the destination and Windows version. If a certificate warning appears, verify the host through a trusted provider channel before continuing.

Microsoft's [Remote Desktop access instructions](https://learn.microsoft.com/en-us/windows-server/remote/remote-desktop-services/remotepc/remote-desktop-allow-access) cover enabling and connecting, checked November 24, 2026. If a connection times out, check server state, address and firewall path first; do not weaken authentication to troubleshoot.

## FAQ

### Does UltaHost include a Windows license with its Windows VPS?

UltaHost says Windows Server Standard is included. Confirm the exact edition on the order; this does not confirm RDS CALs or desktop application rights.

### How much does UltaHost Basic Windows VPS cost for one, two or three years?

The currently displayed card shows $16.10/mo for two years, or $386.40 for the 24 month service term, and says it renews at the same rate for two years. The retrieved listing does not show the 12 or 36 month invoice totals. Request those term quotes at checkout.

### Can two or more people use the same Windows VPS over RDP?

Do not assume so from administrator access. Ask UltaHost to confirm the hosted licensing and configuration for your number of users and simultaneous sessions.

### Is Windows VPS Basic enough for MT5 or another trading terminal?

Compare the terminal vendor's CPU, memory and storage requirements with Basic's 2 cores, 2 GB RAM and 50 GB NVMe, including headroom for updates and any other applications. Validate your own workload before moving production activity.

### Can I use an UltaHost Windows VPS from a Mac?

Use a Microsoft Remote Desktop client available for your device, then connect to the server address and account supplied with the order. Verify the destination before saving credentials.

### Can I get a refund if the Windows VPS does not fit?

UltaHost's policy revised November 14, 2026 says a new VPS may be eligible within 30 days, subject to its terms and exclusions; it also states that Windows software licenses are not refunded. Check eligibility for the exact order before relying on a refund. Source: [UltaHost cancellation and refunds policy](https://ultahost.com/refund#art52hz), checked November 24, 2026.

## Related VPS guides

- [RDP vs Windows VPS for MT5 and bots](/posts/rdp-vs-windows-vps/) compares a shared remote desktop with owning a Windows server.
- [Best Windows VPS hosting](/posts/best-windows-vps-hosting-2026/) covers provider choice, access and licensing questions.
- [UltaHost pricing and refund rules](/posts/ultahost-coupon-and-pricing/) helps reconcile the quote and commitment.

For a focused Windows-only task, shortlist Basic if its documented resources fit. Step up to Business when the software needs more memory. Before paying, get the 12, 24 or 36 month amount and renewal in writing, and settle who is licensed to connect.

[See UltaHost Windows VPS plans](https://ultahost.com/#art52hz "affiliate")
