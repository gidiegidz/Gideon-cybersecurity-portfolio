# Active Directory Security Investigation

## Goal

For this project I built an Active Directory lab so I can understand how domain authentication works and how Windows records failed and successful logins.

I also wanted to see the difference between what gets logged on the workstation and what gets logged on the domain controller.

## Lab Setup

I used VMware Workstation with 2 virtual machines.

GIDEONLAB-DC01 - Windows Server 2025

GIDEONLAB-WS01 - Windows 11 Enterprise

Domain - gideonlab.test

DC01 IP - 192.168.62.10

WS01 IP - 192.168.62.129

DC01 was configured as the domain controller and DNS server.

WS01 was joined to the gideonlab.test domain and used DC01 as its DNS server.

## Configuration

### Active Directory Setup

I created OUs for Users, Groups, Workstations, Servers, and Service Accounts.

Under Users I created separate OUs for IT, HR, and Finance.

I created 3 Global Security Groups:

GG_IT

GG_HR

GG_Finance

I also created 3 test users:

arivera - IT

mchen - HR

dbrooks - Finance

WS01 was joined to the domain and moved to the Workstations OU.

### Audit Policy

For WS01 I created a GPO called GPO - Workstation Security Baseline and linked it to the Workstations OU.

I enabled Audit Logon for Success and Failure.

I used these commands to verify that the policy was applied:

gpupdate /force

gpresult /r /scope computer

auditpol /get /subcategory:"Logon"

For DC01 I created another GPO called GPO - Domain Controller Audit Policy and linked it to the Domain Controllers OU.

I enabled Credential Validation for Success and Failure.

I also enabled Kerberos Authentication Service for Success and Failure.

I verified the settings using:

auditpol /get /subcategory:"Credential Validation"

auditpol /get /subcategory:"Kerberos Authentication Service"

## Authentication Testing

I used runas on WS01 to create failed and successful login attempts for the arivera account.

The command I used was:

runas /user:GIDEONLAB\arivera cmd

For the failed attempts I intentionally entered the wrong password.

Windows returned:

RUNAS ERROR: Unable to run - cmd

1326: The user name or password is incorrect.

I also tested it using the correct password and a new Command Prompt opened successfully.

## Findings

### Failed Logins

On WS01 I found Event ID 4625 for the failed login attempts.

The event showed:

Account Name - arivera
Account Domain - GIDEONLAB
Logon Type - 2
Failure Reason - Unknown user name or bad password
Status - 0xC000006D
Sub Status - 0xC000006A
Workstation - GIDEONLAB-WS01
Source Address - ::1

The Sub Status 0xC000006A showed that the password entered was incorrect.

I generated 5 failed login attempts and found matching 4625 events on WS01 at:

8:01:37 AM
8:01:40 AM
8:01:42 AM
8:01:44 AM
8:01:46 AM

### Domain Controller Events

On DC01 I found matching Event ID 4771 events at the same times.

Event 4771 showed:

Account Name - arivera
Client Address - 192.168.62.129
Failure Code - 0x18

The client address matched WS01 and the failure code showed that Kerberos pre-authentication failed. In this test, it matched the wrong password I entered.

This allowed me to match the failed login events on WS01 with the Kerberos authentication failures recorded on DC01.

### Successful Login

After the failed attempts I tested the same account using the correct password.

On WS01 I found Event ID 4624.

The event showed:

Account Name - arivera
Account Domain - GIDEONLAB
Logon Type - 2
Logon Process - seclogo
Source Address - ::1

On DC01 I found the matching Event ID 4768.

The event showed:

Account Name - arivera
Client Address - 192.168.62.129
Result Code - 0x0

The 4768 event showed that the Kerberos authentication ticket request was successful.

### Correlation

The failed login on WS01 appeared as Event ID 4625 and the matching Kerberos failure on DC01 appeared as Event ID 4771.

The successful login on WS01 appeared as Event ID 4624 and the matching Kerberos event on DC01 appeared as Event ID 4768.

I also generated 5 failed login attempts within a few seconds. The timestamps on WS01 matched the 4771 events on DC01, which helped confirm that the same authentication attempts were being recorded on both systems.

I also found another failed login at around 8:08:04 AM on WS01 followed by a successful login at 8:08:11 AM. On DC01 the matching Kerberos events appeared at 8:08:03 AM and 8:08:10 AM.

This showed me how the workstation and domain controller record different parts of the same authentication activity.

## Conclusion

In this project I learned how Active Directory authentication events can be investigated from both the workstation and domain controller.

I was able to generate failed and successful login attempts, identify the related Windows Security events, and match the activity between WS01 and DC01 using the account, timestamps, IP address, and event details.

I also learned the basic role of Kerberos in domain authentication and how Event IDs 4768 and 4771 can help investigate authentication activity.
