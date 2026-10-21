# Phishing Email Investigation

## Goal

The goal of this project was to investigate a simulated phishing email and identify suspicious indicators using email headers, authentication results, DNS information, domain registration data, and reputation sources.

I also created a Python script to extract URLs, IP addresses, email addresses, and domains from the email sample.

## Evidence Reviewed

The investigation used the following evidence:

Synthetic phishing email sample

Email headers including From, Reply-To, Return-Path, Received, and Authentication-Results

SPF, DKIM, and DMARC results

URLs, domains, IP addresses, and email addresses extracted from the message

DNS records

WHOIS and RDAP registration information

VirusTotal reputation information

urlscan.io scan data

AbuseIPDB IP reputation information

## Initial Findings

The visible From address claimed to be:

security@microsoft.com

The Reply-To address was:

helpdesk@account-security.example

The Return-Path was:

bounce@account-security.example

The sending server shown in the Received header was:

mail.account-security.example

This created a mismatch between the visible Microsoft sender and the infrastructure associated with account-security.example.

The email authentication results showed:

SPF: Fail

DKIM: None

DMARC: Fail

The message also contained the following URL:

https://login-microsoft365.account-security.example/verify

The hostname was:

login-microsoft365.account-security.example

The actual domain was:

account-security.example

The use of "login-microsoft365" as a subdomain could make the link appear related to Microsoft even though the underlying domain was not microsoft.com.

The message also used urgency by warning that the account would be suspended within 24 hours unless the user verified their identity.

The combination of the sender mismatch, failed email authentication, suspicious domain, and urgent account-suspension language made the email highly suspicious and consistent with phishing.

## IOC Analysis

The Python script extracted the following indicators from the email:

URL:

https://login-microsoft365.account-security.example/verify

Hostname:

login-microsoft365.account-security.example

IP Address:

198.51.100.23

Email addresses:

security@microsoft.com

helpdesk@account-security.example

bounce@account-security.example

gideon@company.example

The domain account-security.example appeared in the Reply-To address, Return-Path, sending server, and phishing URL.

This made account-security.example the main suspicious domain in the investigation.

The address security@microsoft.com was the visible sender address, but the other message infrastructure did not support the Microsoft identity.

The address gideon@company.example was the recipient and was not considered a suspicious IOC.

The domain and IP used in this project are reserved synthetic values, so live reputation results were not used to determine whether they were malicious.

Instead, I practiced the IOC investigation process using safe real-world examples with DNS, WHOIS, RDAP, VirusTotal, urlscan.io, and AbuseIPDB.

## Assessment

The email was assessed as highly suspicious and consistent with phishing.

The visible sender claimed to be Microsoft, but the Reply-To, Return-Path, sending server, and URL all pointed to account-security.example.

SPF failed for the envelope sender domain, DKIM was not present, and DMARC failed because there was no aligned SPF or DKIM pass supporting the visible microsoft.com From domain.

The message also used urgency and threatened account suspension to pressure the recipient into clicking the link.

These findings supported the phishing assessment, but the analysis was based on a controlled synthetic sample and did not involve a real malicious domain or IP.

## Recommended Response

If this occurred in a real environment, I would follow the organization's incident response process.

Possible next steps would include identifying whether other users received the same message, checking whether anyone clicked the link or submitted credentials, blocking the suspicious domain and URL where appropriate, reviewing related endpoint or authentication activity, and escalating the incident if further evidence of compromise was found.

## Conclusion

The email contained multiple indicators consistent with phishing, including sender mismatches, failed email authentication, a suspicious URL, and urgency designed to pressure the recipient.

The investigation showed the importance of reviewing both the visible email content and the underlying technical headers before reaching a conclusion.
