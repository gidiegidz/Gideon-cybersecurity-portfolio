# SSH Brute-Force Investigation

## Goal

For this project I investigated simulated SSH authentication activity on a Linux server.

The goal was to identify failed login attempts, find the source IP addresses, see which usernames were targeted, check for successful authentication, and build a timeline of the activity.

## Lab Setup

I used Ubuntu through WSL (Windows Subsystem for Linux) for the investigation.

The authentication log was synthetically generated using generative AI to simulate SSH login activity.

No real credentials, production systems, or private network data were used.

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

## Failed Login Analysis

I first checked how many failed SSH login attempts were in the log.

I used:

grep -c "Failed password" logs/auth.log

The result was:

20

There were 20 failed login attempts in total.

## Source IP Analysis

I checked which IP addresses were the source of the failed login attempts.

I used:

grep "Failed password" logs/auth.log | awk '{print $(NF-3)}' | sort | uniq -c

The results were:

18 185.73.44.21

2 203.0.113.45

The IP address 185.73.44.21 was the source of 18 of the 20 failed attempts.

The other 2 failed attempts came from 203.0.113.45.

## Targeted Usernames

I then checked which usernames were targeted by 185.73.44.21.

I used:

grep "Failed password" logs/auth.log | grep "185.73.44.21" | awk '{print $(NF-5)}' | sort | uniq -c

The results were:

5 admin

3 backup

5 gideon

5 root

The IP address targeted admin, root, gideon, and backup.

The 2 failed attempts from 203.0.113.45 targeted the test username.

## Successful Login

I checked whether 185.73.44.21 also had any successful authentication.

I used:

grep "Accepted password" logs/auth.log | grep "185.73.44.21"

The result showed:

Sep 18 08:18:01 server01 sshd[1225]: Accepted password for gideon from 185.73.44.21 port 44192 ssh2

There were 15 failed attempts from the same IP before the successful login to gideon.

Five of those failed attempts targeted gideon between 08:17:03 and 08:17:15.

The successful login happened at 08:18:01, which was 46 seconds after the last failed attempt against gideon.

After the successful login, the same IP generated 3 more failed attempts against backup.

## Timeline Validation

I created a separate file containing only events from 185.73.44.21.

grep "185.73.44.21" logs/auth.log > logs/suspicious-ip-events.txt

I counted the events using:

wc -l logs/suspicious-ip-events.txt

The result was:

19 logs/suspicious-ip-events.txt

This showed 19 total authentication events from 185.73.44.21.

18 were failed login attempts and 1 was a successful login.

I also checked the first and last events using:

grep "185.73.44.21" logs/auth.log | head -1

grep "185.73.44.21" logs/auth.log | tail -1

The first event occurred at 08:15:22.

The last event occurred at 08:19:20.

The activity lasted 3 minutes and 58 seconds.

## Timeline

08:15 - 5 failed attempts for admin

08:16 - 5 failed attempts for root

08:17 - 5 failed attempts for gideon

08:18 - Successful login to gideon

08:19 - 3 failed attempts for backup

## Findings

There were 20 failed SSH login attempts in the log.

Most of the activity came from 185.73.44.21, which generated 18 failed attempts and 1 successful authentication.

The failed attempts targeted multiple usernames.

The part that stood out the most was the 5 failed attempts against gideon followed 46 seconds later by a successful login from the same IP.

The pattern is consistent with repeated password guessing, but the log alone does not prove that the gideon account was compromised.

I would need more evidence to determine whether the successful login was authorized and what happened after the login.

## Further Investigation

If this were a real environment, I would check:

Activity after the successful login

Commands run during the session

Files or folders that were accessed or changed

Account activity

Running processes

Network activity

Other authentication and system logs

I would also follow the organization's incident response process and preserve the relevant evidence before making changes.

Depending on the findings, possible actions could include resetting the account password, blocking the source IP if it was confirmed to be unauthorized, enabling MFA, and reviewing SSH authentication settings.

## Conclusion

This project helped me practice using Linux command-line tools to investigate authentication logs.

I was able to identify the main source IP, targeted usernames, failed and successful authentication events, and build a timeline of the activity.

I also learned that a successful login after multiple failures is something that should be investigated further, but it does not automatically prove that an account was compromised.
