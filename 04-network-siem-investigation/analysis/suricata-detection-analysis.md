# Suricata Detection Analysis

## Objective

Analyze how Suricata detected the controlled TCP SYN scan and determine how the custom detection rule behaved during the test.

## Original Detection Rule

Suricata monitored traffic on the Ubuntu sensor interface `ens33`.

The original custom rule used SID `100001`, revision `1`, with the signature:

`LOCAL Possible TCP SYN Port Scan`

The rule used a detection filter that tracked matching traffic by source IP and evaluated whether 20 matching TCP SYN packets occurred within 5 seconds.

Relevant rule logic:

`detection_filter:track by_src, count 20, seconds 5;`

The purpose of the rule was to identify a source generating a rapid number of TCP SYN packets consistent with port-scanning activity.

## Alert Investigation

The original Suricata EVE JSON log was preserved as:

`logs/eve.json`

Inspection of an alert event showed:

- Source IP: `192.168.166.10`
- Destination IP: `192.168.166.20`
- Protocol: TCP
- Interface: `ens33`
- Signature ID: `100001`
- Revision: `1`
- Signature: `LOCAL Possible TCP SYN Port Scan`
- Action: `allowed`

The `allowed` action indicates that Suricata generated an alert but did not block the traffic. Suricata was operating as a detection mechanism in this lab rather than preventing the scan.

## Alert Count

Analysis of `eve.json` identified exactly **80 alert events** associated with the custom detection.

All 80 alerts were verified as:

- Signature ID `100001`
- Revision `1`
- Signature `LOCAL Possible TCP SYN Port Scan`

Packet analysis independently confirmed that the controlled scan generated **100 TCP SYN probes**.

The difference between the 100 observed SYN packets and 80 Suricata alerts was caused by the original rule's detection-filter behavior. Matching SYN packets first contributed toward satisfying the configured rate condition of 20 packets within 5 seconds. Once the condition was satisfied, subsequent matching packets generated alerts while the condition remained satisfied.

In this controlled test, the 100-port SYN scan therefore resulted in 80 alert events.

## Initial Finding

The rule successfully detected the controlled SYN scan, but a single scan generated 80 alerts.

Although the detection worked, this produced excessive redundant alert volume for one scanning event. Repeated alerts describing the same activity could increase analyst workload and contribute to alert fatigue.

This finding led to tuning the rule to preserve detection while reducing duplicate alert generation.

## Rule Tuning

The original rule successfully detected the controlled SYN scan, but generating 80 alerts for a single scanning event created unnecessary alert volume.

The rule was therefore tuned to reduce redundant alerts while preserving the original detection condition.

The original revision used:

`detection_filter:track by_src, count 20, seconds 5;`

Revision 2 replaced this with:

`threshold:type both, track by_src, count 20, seconds 5;`

The source IP continued to be tracked, and the detection condition remained based on 20 matching SYN packets within a 5-second window. The change was intended to control repeated alert generation after the condition was satisfied.

The rule revision was incremented from `rev:1` to `rev:2`.

## Tuning Validation

The tuned rule was tested using multiple controlled scans.

### Test 1 - 100-Port SYN Scan

A TCP SYN scan of ports 1-100 was performed against the Ubuntu sensor.

The scan exceeded the configured detection condition and generated **1 Rev 2 alert**.

This demonstrated that the tuned rule continued to detect the scanning activity while substantially reducing the redundant alerts observed with Rev 1.

### Test 2 - Repeated 100-Port SYN Scan

A second 100-port SYN scan was performed after the five-second window.

Suricata generated **1 additional Rev 2 alert**.

The two controlled 100-port scans therefore produced:

- 2 scans
- 2 Rev 2 alerts
- 1 alert per scan

This demonstrated that alert suppression from the first scan did not prevent a later scan outside the time window from generating a new alert.

### Test 3 - Below-Threshold Scan

A smaller scan targeting TCP ports 1-10 was performed.

This generated only 10 SYN probes and therefore did not satisfy the configured condition of 20 matching SYN packets within five seconds.

No additional Rev 2 alert was generated.

This provided a negative test showing that traffic below the configured threshold did not trigger the detection.

## Tuning Results

### Rev 1 - Original

- Controlled 100-port scans: 1
- Total alerts: 80
- Observed alerts per scan: 80

### Rev 2 - Tuned

- Controlled 100-port scans: 2
- Total alerts: 2
- Observed alerts per scan: 1

For the controlled 100-port SYN scan, the original rule generated 80 alerts for a single scanning event. After tuning, the same type of scan generated 1 alert.

This substantially reduced redundant alerting while preserving detection of the tested scanning activity.

## Detection Engineering Finding

The original rule successfully identified the simulated reconnaissance activity but produced excessive duplicate alerts.

After tuning, the detection continued to identify scans that exceeded the configured rate condition, generated a new alert for a later scan, and did not alert on the below-threshold 10-port test.

The tuning therefore improved the usability of the detection in this controlled environment by reducing redundant alert volume while preserving the tested detection behavior.
