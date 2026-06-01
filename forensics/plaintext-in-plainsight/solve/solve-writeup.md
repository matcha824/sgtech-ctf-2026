# Plaintext in Plainsight - Solve Writeup

## Challenge Summary
A PCAP file is provided containing network traffic captured from a busy
internal network. The goal is to dig through the noise, find an HTTP login
request, and retrieve credentials being transmitted in plaintext.

---

## Step 1 - Open the PCAP in Wireshark
Open `challenge.pcap` in Wireshark. You will be greeted with roughly 4700
packets of mixed network traffic including:

- ICMP ping sweeps
- UDP floods
- DNS queries
- NTP time sync requests
- ARP broadcasts
- DHCP discoveries
- Syslog messages
- Multicast traffic
- TCP handshakes
- HTTP GET and POST requests across multiple internal domains

The sheer volume of traffic is intentional real networks are noisy.

---

## Step 2 - Notice the traffic is HTTP not HTTPS
Scan the Protocol column. You will see HTTP traffic on port 80 with no TLS
or SSL handshakes. This means every HTTP request and response is transmitted
completely unencrypted. Any credential sent over this connection is fully
readable by anyone capturing traffic on the same network.

This is the core vulnerability the challenge is built around.

---

## Step 3 - Filter down to POST requests
Use the Wireshark display filter bar to cut through the noise and isolate
all HTTP POST requests: 

filter expression = **http.request.method == "POST"**

You will immediately see POST requests hitting many different paths and
internal domains such as:

- `shop.corp/cart` - add to cart requests
- `shop.corp/checkout` - purchase forms with card details
- `mail.corp/compose` - outgoing emails
- `api.corp/v1/users` - user management API calls
- `dashboard.corp/reports` - report generation requests
- `login.corp/login` - login attempts with wrong credentials

There are many POST requests. This alone is not enough to find the flag.

---

## Step 4 - Filter to the login path
Multiple domains have a `/login` endpoint and multiple clients are hitting
them with wrong credentials as noise. Narrow the filter down to only POST
requests targeting the `/login` path: 

filter expression = **http.request.method == "POST" && http.request.uri == "/login"**

You will still see several failed login attempts returning `401 Unauthorized`
from various spoofed source IPs.

---

## Step 5 - Filter to the admin user
The account we care about is `admin`. Add one more condition to match the
username field inside the POST body: 

filter expression = **http.request.method == "POST" && http.request.uri == "/login" && http contains "username=admin"**

This isolates a single packet which is the one we are looking for.

---

## Step 6 - Read the plaintext credentials
Right-click the packet and select **Follow → TCP Stream** for the full conversation. You will see:

POST /login HTTP/1.1
Host: internalapp.corp
Content-Type: application/x-www-form-urlencoded
username=admin&password=pl41nt3xt_p4ssw0rds_4r3_b4d