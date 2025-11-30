# Healthcare Clinic Network — README

## Project

**Healthcare Clinic Network** — design, deploy, and operate a secure, resilient, and auditable network for a two-branch healthcare clinic. This repository contains full project documentation intended for handover to network operations, security teams, and auditors.

---

## Purpose and scope

Provide a complete, production-ready specification and operational playbook to build a segmented clinic network that:

* Protects patient and organizational data through segmentation and policy enforcement.
* Enables reliable clinic-to-clinic connectivity across a routed WAN backbone.
* Centralizes security controls (FortiGate) and network management.
* Supports growth, fault tolerance, and maintainability.

This README covers architecture, addressing and VLAN plans, FortiGate integration, step-by-step deployment, testing/validation, monitoring and logging, operational runbooks, backup and change management, bill of materials, and handover checklist.

---

## Intended audience

* Network Engineers and Administrators
* Security Engineers / SOC Analysts
* Systems Engineers (DHCP/DNS/Authentication)
* IT Managers / Project Sponsors
* Auditors and Compliance Officers

---

## Project team (as recorded)

* Supervisor: Elhosein Ahmed.
* Team: Ayad Zewail, Hazem Ahmed, Mohamed Khaled, Mostafa Mahmoud, Youssef Said, Seif Samer. 

---

## High-level requirements

1. Role-based segmentation: Admins, Clinical Staff (Doctors/Nurses), and Guests/Waiting-room users separated into VLANs. 
2. Inter-VLAN routing at the distribution layer (multilayer switching). 
3. WAN connectivity between two clinic branches over routed backbone. 
4. High availability at L2/L3 edges (Port Channels/LACP, protocol-level resilience such as PVST or vendor equivalent). 
5. Centralized FortiGate security appliance providing firewall policies, web filtering (category-based), antivirus (flow-based), and application control. 
6. Centralized DHCP for VLANs, logging to a central collector, and maintainable configuration objects. 

---

## Architecture summary (logical)

* Two physical sites (Branch A, Branch B) connected via a routed WAN (site-to-site VPN or private routed link). 
* Each site:

  * Access layer switches (ports for workstations, printers, APs).
  * Distribution multilayer switch (SVIs for VLANs / inter-VLAN routing).
  * Edge security: FortiGate controls north-south traffic and enforces security profiles. 
* Central services (can be on-prem or cloud): DHCP, authentication (RADIUS/AD), logging/SIEM, and backup repository.

---

## Network design — addressing and VLANs (production-ready plan)

### VLANs and subnets

| VLAN ID | Name           | Usage / Policy summary                                 | Subnet (CIDR)         |
| ------: | -------------- | ------------------------------------------------------ | --------------------: |
|      21 | ADMINS         | Administrative staff, privileged access, low filtering |         10.10.21.0/24 |
|      22 | CLINICAL       | Doctors & Nurses — allowed clinical and research sites |         10.10.22.0/24 |
|      23 | GUESTS_WAITING | Guest Wi-Fi and waiting-room devices, strict policy    |         10.10.23.0/24 |

---

## FortiGate integration — interface mapping and security design


### FortiGate physical/subinterface plan

* `port1` — Internet/WAN A — public/ISP link (IP: 192.168.107.128/24 as shown in presentation; use your ISP-assigned IPs). 
* `port2` — Internal LAN trunk to distribution switch (carry VLANs).
* `port3` — Secondary WAN or site-to-site peer (backup transit or other ISP) (IP: 10.0.4.1/24). 

### Security profile plan

* **Antivirus**: Flow-based scanning; block infected files. Use block mode for high-risk clinic networks. 
* **Web Filtering**: Category-based profiles. Create group-based profiles (Admins = permissive, Clinical = medium, Guests = strict). 
* **Application Control**: Block non-business and high-bandwidth consumer apps during work hours (e.g., video streaming), allow necessary clinical apps. 

---

## Deployment: step-by-step (detailed operational playbook)

**Assumptions:** devices are available, credentials have been provisioned, and a maintenance window is scheduled.

### Phase 1 — Network Configuration

1. **Inter-VLAN & SVIs**
   Create all VLANs and configure SVIs on the distribution switch to enable inter-VLAN routing and act as the default gateway for each subnet.

2. **DHCP**
   Configure DHCP relay on each SVI (or local DHCP scopes) with correct DNS and gateway settings for every VLAN.

3. **Routing**
   Enable Layer-3 routing on the distribution switch and apply necessary static or dynamic routes for WAN reachability.

4. **Port Channel (LACP)**
   Build an LACP Port Channel for uplinks to the core/edge device to provide redundancy and aggregated bandwidth.

5. **PVST**
   Enable PVST and set the distribution switch as the primary root bridge (with a secondary root if available) to maintain a stable Layer-2 topology.


### Phase 2 — FortiGate initial configuration

1. Perform initial admin password rotation.
2. Configure interfaces:

   * `port1` (WAN) — set ISP parameters and default route. 
   * `port2` — set as trunk or connect to SVI (carry all VLANs). 
   * `port3` — configure secondary WAN / site peer. 
3. Create address objects and groups for VLAN subnets.

### Phase 3 — Firewall policy and access controls

1. **Antivirus (AV) — Configure and enforce flow-based AV in block mode**

   * Enable flow-based scanning on relevant policies so files are inspected in-line with minimal latency.
   * Set action to **block** on detection and enable full logging of AV events.
   * Apply AV profile to all Internet-facing and inter-VLAN policies that may carry file transfers.

2. **Web Filtering — Apply category-based, group-tiered profiles**

   * Create three web-filter profiles (Admins = permissive, Clinical = moderate, Guests = strict) and assign by source group.
   * Configure category blocks according to role (allow medical/research categories for Clinical; block high-risk categories for Guests).

3. **Application Control — Enforce app-level allow/deny and bandwidth-preservation rules**

   * Define application-control profiles that explicitly **allow** required clinical/business apps and **deny** non-business/high-bandwidth apps.


---
