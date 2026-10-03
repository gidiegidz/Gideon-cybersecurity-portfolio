import re
from pathlib import Path
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
from urllib.parse import urlparse

sample_path = Path("samples/phishing-sample.eml")

with sample_path.open("rb") as f:
    message = BytesParser(policy=policy.default).parse(f)

print("Email Headers:")
print("From:", message["From"])
print("To:", message["To"])
print("Subject:", message["Subject"])
print("Reply-To:", message["Reply-To"])
print("Return-Path:", message["Return-Path"])

email_text = sample_path.read_text(encoding="utf-8")

urls = sorted(set(re.findall(r'https?://[^\s<>"]+', email_text)))

url_hosts = []

for url in urls:
    hostname = urlparse(url).hostname

    if hostname:
        url_hosts.append(hostname)

url_hosts = sorted(set(url_hosts))

ips = sorted(set(re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', email_text)))

address_headers = [
    message["From"],
    message["To"],
    message["Reply-To"],
    message["Return-Path"],
]

valid_headers = []

for header in address_headers:
    if header:
        valid_headers.append(header)

parsed_addresses = getaddresses(valid_headers)

emails = []

for name, address in parsed_addresses:
    emails.append(address)

emails = sorted(set(emails))

email_domains = []

for address in emails:
    if "@" in address:
        parts = address.split("@", 1)
        domain = parts[1]
        domain = domain.lower()
        email_domains.append(domain)

email_domains = sorted(set(email_domains))

print("\nURLs:")
for url in urls:
    print(url)

print("\nURL Hostnames:")
for host in url_hosts:
    print(host)

print("\nIP Addresses:")
for ip in ips:
    print(ip)

print("\nEmail Addresses:")
for address in emails:
    print(address)

print("\nEmail Domains:")
for domain in email_domains:
    print(domain)
