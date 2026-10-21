# Active Directory Security Investigation

## Overview

For this project I built an Active Directory lab using Windows Server 2025 and Windows 11.

The goal was to learn how domain authentication works, configure Windows security auditing, and investigate failed and successful login activity from both the workstation and domain controller.

I created users, groups, OUs, Group Policy settings, and a domain-joined workstation. I then generated controlled login attempts and compared the related Windows Security events on both systems.

## Lab Environment

GIDEONLAB-DC01 - Windows Server 2025

GIDEONLAB-WS01 - Windows 11 Enterprise

Domain - gideonlab.test

DC01 IP - 192.168.62.10

WS01 IP - 192.168.62.129

Virtualization - VMware Workstation

## What I Practiced

Active Directory setup

Users, groups, and OUs

Domain joining

DNS configuration

Group Policy

Windows Security auditing

Windows Event Viewer

Failed and successful login investigation

Kerberos authentication basics

Event correlation between a workstation and domain controller

## Events Investigated

Event ID 4625 - Failed logon on WS01

Event ID 4624 - Successful logon on WS01

Event ID 4771 - Kerberos pre-authentication failure on DC01

Event ID 4768 - Successful Kerberos TGT request on DC01

## Findings

I generated 5 failed login attempts for the arivera account within 9 seconds.

WS01 recorded the failures as Event ID 4625 at:

8:01:37 AM
8:01:40 AM
8:01:42 AM
8:01:44 AM
8:01:46 AM

DC01 recorded matching Event ID 4771 events at the same times.

The DC01 events showed arivera as the account, 192.168.62.129 as the client address, and failure code 0x18.

I later generated another failed login followed by a successful login.

WS01 recorded:

8:08:04 AM - Event ID 4625
8:08:11 AM - Event ID 4624

DC01 recorded:

8:08:03 AM - Event ID 4771
8:08:10 AM - Event ID 4768

The failed and successful events could be matched using the account, timestamps, client IP address, and event details.

This helped me understand how the workstation and domain controller record different parts of the same domain authentication activity.

## Evidence

Screenshots are included in the screenshots folder showing the Active Directory structure, test users, audit policy settings, failed login events, Kerberos failures, and the failed-then-successful authentication sequence.

## Detailed Investigation

The full investigation notes are available in:

analysis/investigation.md
