# SSH Brute-Force Attack Investigation

## Investigation Overview

This project is a simulated investigation of suspicious SSH login activity on a Linux server.

I analyzed the authentication log to find failed login attempts, identify the source IP addresses, see which accounts were targeted, and check if any login was successful.

I used Linux command-line tools such as `grep`, `awk`, `sort`, `uniq`, `head`, `tail`, and `wc`.


## Lab Environment & Data

I used Ubuntu through WSL (Windows Subsystem for Linux) for this project.

The authentication log was created by me to simulate SSH login activity. It includes both failed and successful login attempts.

No real credentials or production systems were used.

### Tools Used

- Ubuntu Linux
- WSL
- grep
- awk
- sort
- uniq
- head
- tail
- wc


## Investigation Objectives

For this investigation, I wanted to:

1. Find the total number of failed SSH login attempts.
2. Find the IP addresses that were responsible for the failed attempts.
3. See which user accounts were targeted.
4. Check if any login was successful from a suspicious IP.
5. Build a timeline of what happened.
6. Identify what other evidence I would need to determine whether the account was compromised.


## Failed Authentication Analysis

I started by checking how many failed SSH login attempts were in the log.

I used:

    grep -c "Failed password" ../logs/auth.log

The result was:

    20

There were 20 failed login attempts in total.

I then checked where these attempts came from to see if there was a pattern.


## Source IP Analysis

Next, I wanted to see which IP addresses were behind the failed login attempts.

I used:

    grep "Failed password" ../logs/auth.log | awk '{print $(NF-3)}'

This showed the IP address for each failed login attempt.

I then sorted and counted the IP addresses:

    grep "Failed password" ../logs/auth.log | awk '{print $(NF-3)}' | sort | uniq -c

The results were:

    18 185.73.44.21
     2 203.0.113.45

The IP address `185.73.44.21` was responsible for 18 of the 20 failed attempts.

The IP address `203.0.113.45` was responsible for the other 2 failed attempts.


## Targeted Account Analysis

Next, I wanted to see which accounts were being targeted by the suspicious IP address `185.73.44.21`.

I used:

    grep "Failed password" ../logs/auth.log | grep "185.73.44.21" | awk '{print $(NF-5)}' | sort | uniq -c

The results were:

     5 admin
     3 backup
     5 gideon
     5 root

The IP address `185.73.44.21` targeted four different accounts: `admin`, `root`, `gideon`, and `backup`.

The other two failed login attempts in the log came from `203.0.113.45` and targeted the `test` account.

## Successful Authentication Analysis

Next, I checked if the suspicious IP address had any successful logins.

I used:

    grep "Accepted password" ../logs/auth.log | grep "185.73.44.21"

The result was:

    Sep 18 08:18:01 server01 sshd[1225]: Accepted password for gideon from 185.73.44.21 port 44192 ssh2

This caught my attention because the same IP address had 15 failed login attempts before a successful login to `gideon`. The IP generated 18 failed attempts in total, with three additional failed attempts against `backup` occurring after the successful login.

There were five failed attempts against `gideon` between 08:17:03 and 08:17:15. The successful login happened at 08:18:01, which was 46 seconds after the last failed attempt.

The log shows that the login was accepted, but it does not prove that the account was compromised. I would need to check other logs to see what happened after the login.

## Incident Timeline

The suspicious activity from `185.73.44.21` happened between 08:15 and 08:19.

- 08:15 — 5 failed attempts for `admin`
- 08:16 — 5 failed attempts for `root`
- 08:17 — 5 failed attempts for `gideon`
- 08:18 — Successful login to `gideon`
- 08:19 — 3 failed attempts for `backup`

The main thing I noticed was the successful login to `gideon` after several failed attempts from the same IP.


## Findings

There were 20 failed login attempts in the log. Most of them came from `185.73.44.21`, which was responsible for 18 attempts.

The IP address `185.73.44.21` targeted four accounts: `admin`, `root`, `gideon`, and `backup`.

The `gideon` account stood out because there were five failed login attempts only a few seconds apart. The last failed attempt was at 08:17:15, followed by a successful login from the same IP at 08:18:01.

This does not prove that the `gideon` account was compromised. It gives us a reason to investigate the account and the activity from that IP further.

I would check what happened after the successful login, including files or folders that were accessed or changed, account activity, and network activity.


## Remediation

If this were a real environment, my first step would be to report the activity to my supervisor or security team.

I would then follow the organization's incident response playbook and preserve the relevant logs and evidence before making changes to the system.

Depending on what is found, possible actions could include:

- Reset the `gideon` account password if unauthorized access is suspected.
- Review the account and system activity after the successful login.
- Block or restrict the suspicious IP address if it is confirmed to be unauthorized.
- Enable MFA if it is available.
- Consider using SSH keys instead of password authentication.
- Review other accounts and systems for similar login activity.

The exact response would depend on the organization's procedures and what is found during the investigation. Since this is a simulated lab, no real systems or accounts were changed.


## Limitations

This investigation was based mainly on the simulated `auth.log` file, so there are some things I cannot determine from the available data.

The successful login does not prove that the `gideon` account was compromised. The log only shows that password authentication was accepted. It does not tell us how the credentials were obtained or whether the login was authorized.

I would need to check additional information such as:

- Activity after the successful login.
- Commands that were run during the session.
- Files or folders that were accessed or changed.
- Network activity from the account.
- The geographic location of the source IP and whether it matches the expected location of the user.
- Other authentication or system logs that could provide more information.

