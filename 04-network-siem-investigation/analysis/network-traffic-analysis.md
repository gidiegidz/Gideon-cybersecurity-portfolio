# Network Traffic Analysis

## Objective

Analyze controlled TCP SYN reconnaissance traffic generated from a Kali Linux host against an Ubuntu sensor and verify the activity at the packet level using tcpdump and Wireshark.

## Lab Systems

- Kali Linux: `192.168.166.10`
- Ubuntu sensor: `192.168.166.20`
- Network: isolated `192.168.166.0/24` lab
- Scan type: TCP SYN scan
- Target ports: TCP `1-100`

## Packet Capture

The controlled scan traffic was preserved in:

`captures/nmap-scan.pcap`

tcpdump analysis confirmed exactly **100 TCP SYN probes** originating from `192.168.166.10` and targeting `192.168.166.20`.

The capture also showed different responses depending on port state. Closed ports returned TCP RST/ACK responses, while TCP port 22 returned SYN/ACK, consistent with SSH being open on the Ubuntu system.

## tcpdump Analysis

The packet capture was first inspected from the command line using tcpdump.

Filtering for TCP packets with only the SYN flag set showed rapid probes from `192.168.166.10` to multiple destination ports on `192.168.166.20`.

The SYN probes were counted using:

`tcpdump -nn -r captures/nmap-scan.pcap 'tcp[tcpflags] == tcp-syn' | grep '192.168.166.10' | wc -l`

The result was exactly **100 SYN packets**, confirming that the capture contained the controlled scan of TCP ports 1-100.

Further inspection of TCP port 22 showed:

1. `192.168.166.10` sent a SYN to TCP port 22.
2. `192.168.166.20` responded with SYN/ACK.
3. `192.168.166.10` responded with RST.

The SYN/ACK response indicated that TCP port 22 was open. The reset from the scanning host was consistent with the half-open behavior of an Nmap SYN scan.

Closed ports observed elsewhere in the capture responded with RST/ACK.

## Wireshark Analysis

The packet capture was also examined in Wireshark.

Using the display filter:

`tcp.flags.syn == 1 && tcp.flags.ack == 0`

Wireshark displayed exactly **100 initial SYN packets** from `192.168.166.10` to `192.168.166.20`. The destination ports varied across TCP ports 1-100, confirming the behavior of the controlled port scan.

### Open Port Behavior

Filtering the capture with:

`tcp.port == 22`

showed the following sequence:

1. Kali sent a TCP SYN to port 22.
2. Ubuntu responded with SYN/ACK.
3. Kali responded with RST instead of completing the TCP handshake.

The SYN/ACK response indicated that TCP port 22 was open. The subsequent reset was consistent with the half-open behavior of the Nmap SYN scan.

Closed ports observed elsewhere in the capture responded with RST/ACK rather than SYN/ACK.

## Packet-Level Findings

- 100 TCP SYN probes were observed from the Kali system.
- The probes targeted TCP ports 1-100 on the Ubuntu system.
- TCP port 22 responded with SYN/ACK and was identified as open.
- Closed ports returned RST/ACK responses.
- Packet-level evidence was consistent with the Nmap scan results.
