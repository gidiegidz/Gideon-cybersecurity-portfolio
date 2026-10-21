# SSH Brute-Force Investigation

## Overview

For this project I investigated simulated SSH authentication activity on a Linux server.

The goal was to practice using Linux command-line tools to identify failed login attempts, source IP addresses, targeted usernames, successful authentication, and build a timeline of the activity.

## Lab Environment

Ubuntu Linux

WSL (Windows Subsystem for Linux)

Simulated SSH authentication log

## What I Practiced

Linux command-line analysis

SSH authentication log analysis

grep

awk

sort

uniq

head

tail

wc

Timeline analysis

Authentication investigation

## Findings

I found 20 failed SSH login attempts in the log.

18 of the failed attempts came from 185.73.44.21.

2 failed attempts came from 203.0.113.45.

The IP address 185.73.44.21 targeted admin, root, gideon, and backup.

There were 15 failed attempts from 185.73.44.21 before a successful login to gideon.

The last failed attempt against gideon happened at 08:17:15.

The successful login happened at 08:18:01, which was 46 seconds later.

After the successful login, the same IP generated 3 more failed attempts against backup.

The activity from 185.73.44.21 lasted 3 minutes and 58 seconds.

The pattern is consistent with repeated password guessing, but the log alone does not prove that the gideon account was compromised.

## Evidence

Screenshots are included in the screenshots folder showing the failed login count, source IP analysis, targeted usernames, and successful authentication.

## Detailed Investigation

The full investigation notes are available in:

analysis/investigation.md
