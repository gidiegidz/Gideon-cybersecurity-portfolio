# Network Reconnaissance & SIEM Investigation

## Overview

This project demonstrates an end-to-end investigation of controlled network reconnaissance activity in an isolated security lab.

A TCP SYN scan was generated from a Kali Linux system against an Ubuntu sensor. The traffic was captured and analyzed at the packet level using tcpdump and Wireshark, detected with a custom Suricata rule, and investigated in Splunk using Suricata EVE JSON telemetry.

The investigation identified excessive alert generation in the original Suricata rule. The detection was then tuned and retested using controlled positive and negative tests.

For the tested 100-port SYN scan, tuning reduced the observed alert volume from **80 alerts per scan to 1 alert per scan** while preserving the detection behavior tested in the lab.

## Lab Architecture

- **Kali Linux:** `192.168.166.10` — controlled reconnaissance source
- **Ubuntu Linux:** `192.168.166.20` — target and Suricata sensor
- **Network:** isolated `192.168.166.0/24` lab network
- **Windows host:** Splunk Enterprise and Wireshark analysis
- **Scan:** Nmap TCP SYN scan against TCP ports 1-100

## Tools Used

- Nmap
- tcpdump
- Wireshark
- Suricata IDS
- Splunk Enterprise
- SPL (Search Processing Language)
- Linux
- VMware

## Investigation Summary

The controlled Nmap SYN scan generated **100 TCP SYN probes** against ports 1-100 on the Ubuntu system.

Packet analysis confirmed:

- 100 initial SYN probes from `192.168.166.10` to `192.168.166.20`
- TCP port 22 responded with SYN/ACK, indicating that SSH was open
- The scanning host responded to the SYN/ACK with RST, consistent with Nmap's half-open SYN scan behavior
- Closed ports observed in the capture responded with RST/ACK

A custom Suricata rule using SID `100001` detected the scanning activity. The original Rev 1 rule generated **80 alerts from one controlled 100-port scan**, creating excessive redundant alert volume.

The rule was tuned and validated with additional controlled testing. Rev 2 generated **one alert per tested 100-port scan**, generated a new alert when the scan was repeated after the configured time window, and did not generate an additional alert during a below-threshold 10-port scan.

Splunk was then used to investigate the Suricata telemetry and quantify the difference between the two rule revisions.

## Key Findings

The packet capture confirmed exactly 100 TCP SYN probes during the controlled scan.

The original Suricata Rev 1 rule detected the scanning activity but generated 80 alerts from one controlled 100-port scan.

After tuning, Rev 2 generated one alert per tested 100-port scan.

A second 100-port scan generated a new Rev 2 alert after the configured time window.

A below-threshold 10-port scan did not generate an additional Rev 2 alert.

Splunk was used to investigate the Suricata telemetry and compare the behavior of the two rule revisions.

## Evidence

The packet capture is included in:

captures/nmap-scan.pcap

The original and tuned Suricata EVE JSON logs are included in:

logs/eve.json

logs/eve-tuned-scan.json

Screenshots and other evidence are stored in the screenshots folder.

## Detailed Investigation

Detailed investigation notes are available in:

analysis/network-traffic-analysis.md

analysis/suricata-detection-analysis.md

analysis/splunk-siem-analysis.md
