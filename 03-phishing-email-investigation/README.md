# Phishing Email Investigation

## Overview

For this project I investigated a simulated phishing email.

The goal was to practice analyzing email headers, authentication results, suspicious URLs, domains, IP addresses, and other indicators that could help determine whether an email was phishing.

I also created a small Python script to extract indicators from the email sample.

## Lab Environment

Ubuntu Linux

WSL (Windows Subsystem for Linux)

Synthetic .eml phishing sample

## What I Practiced

Email header analysis

SPF

DKIM

DMARC

DNS lookups

WHOIS

RDAP

VirusTotal

urlscan.io

AbuseIPDB

Python

IOC extraction

Phishing investigation

Incident response reasoning

## Findings

The visible sender claimed to be Microsoft, but the Reply-To, Return-Path, sending server, and URL all pointed to account-security.example.

SPF failed for the envelope sender domain.

DKIM was not present.

DMARC failed because there was no aligned SPF or DKIM pass supporting the visible microsoft.com From domain.

The email also used urgency and threatened account suspension to pressure the recipient into clicking the link.

The overall pattern was highly suspicious and consistent with phishing.

## Evidence

The synthetic email sample is included in:

samples/phishing-sample.eml

The Python IOC extraction script is included in:

scripts/extract_iocs.py

Screenshots and other evidence are stored in the screenshots folder.

## Detailed Investigation

The full investigation notes are available in:

analysis/investigation.md
