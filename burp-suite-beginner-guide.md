# Burp Suite Beginner Guide: Web App Hacking in 2026

Burp Suite is the industry standard tool for web application security
testing. If you're doing any kind of web hacking — CTFs, bug bounty, or
professional pentesting — you need to know Burp Suite.

I first used it on TryHackMe and it completely changed how I understood
web applications. This guide covers everything a beginner needs to get
started with the free Community Edition.

## What is Burp Suite?

Burp Suite is a web application security testing platform made by
PortSwigger. It sits between your browser and the internet as a proxy,
letting you intercept, inspect, and modify web traffic in real time.

Think of it as a man-in-the-middle tool for your own browser — you can
see exactly what your browser sends to a server and what the server sends
back, and you can modify any of it.

**Two versions:**
- **Community Edition** — Free, covers everything a beginner needs
- **Professional Edition** — $449/yr, adds automated scanner and advanced
  tools (not needed when starting out)

## Installing Burp Suite

### On Kali Linux (already installed)
```bash
burpsuite
```
Or find it in Applications → Web Application Analysis

### On Windows
1. Go to [portswigger.net/burp/communitydownload](https://portswigger.net/burp/communitydownload)
2. Download the Windows installer
3. Run it — all defaults are fine
4. Launch Burp Suite and select **Temporary Project** → **Use Burp Defaults**

## Setting Up Your Browser Proxy

Burp Suite works by intercepting your browser traffic. You need to tell
your browser to send traffic through Burp first.

### Step 1: Check Burp's Proxy Port
In Burp Suite go to **Proxy** → **Options**
Default listener is `127.0.0.1:8080` — note this down.

### Step 2: Configure Firefox (Recommended)
Firefox is the best browser for Burp Suite because you can set a
proxy just for Firefox without affecting your whole system.

1. Open Firefox
2. Go to **Settings** → search "proxy"
3. Click **Settings** under Network Settings
4. Select **Manual proxy configuration**
5. HTTP Proxy: `127.0.0.1` Port: `8080`
6. Check **Also use this proxy for HTTPS**
7. Click OK

### Step 3: Install Burp's CA Certificate
Without this step HTTPS sites will show certificate errors.

1. With Firefox proxy configured, go to `http://burpsuite`
2. Click **CA Certificate** to download it
3. In Firefox go to **Settings** → search "certificates"
4. Click **View Certificates** → **Import**
5. Select the downloaded certificate
6. Check both trust boxes → OK

Now Burp Suite can intercept HTTPS traffic without errors.

## The Main Tools You Need to Know

### 1. Proxy — Intercept Traffic

The Proxy tab is where most beginners spend their time. It lets you
intercept requests before they reach the server.

**How to use it:**
1. Go to **Proxy** → **Intercept**
2. Make sure **Intercept is on** is showing
3. Visit any website in Firefox
4. The request appears in Burp — you can read or modify it
5. Click **Forward** to send it, or **Drop** to block it

**What to look for in requests:**
- Parameters being sent (`?id=1`, `?user=admin`)
- Cookies
- Hidden form fields
- Authentication tokens

### 2. Repeater — Modify and Resend Requests

Repeater lets you take a captured request, modify it, and resend it
as many times as you want. This is the tool you'll use most for manual
testing.

**How to use it:**
1. Intercept a request in Proxy
2. Right-click → **Send to Repeater**
3. Go to the **Repeater** tab
4. Modify the request (change parameters, headers, etc.)
5. Click **Send** to send it
6. See the response on the right

**Common uses:**
- Testing SQL injection manually
- Trying different parameter values
- Bypassing client-side validation

### 3. Intruder — Automated Attack Tool

Intruder automates sending many requests with different payloads. Think
of it as a fuzzer — useful for brute forcing login forms or finding
hidden parameters.

**Note:** In Community Edition Intruder is rate-limited (slow). It's
still useful but much faster in Pro.

**How to use it:**
1. Send a request to Intruder (right-click → Send to Intruder)
2. Go to **Intruder** → **Positions**
3. Click **Clear §** to remove default markers
4. Highlight the value you want to fuzz
5. Click **Add §** to mark it
6. Go to **Payloads** tab
7. Add your payload list
8. Click **Start Attack**

### 4. Decoder — Encode and Decode Data

Decoder lets you encode and decode data in common formats:
- Base64
- URL encoding
- HTML encoding
- Hex

**How to use it:**
1. Go to **Decoder** tab
2. Paste your data
3. Select encoding/decoding type
4. See the result instantly

Super useful in CTFs when you find encoded strings.

### 5. Target — Site Map

The Target tab builds a map of everything you've browsed through Burp.
Useful for understanding an application's structure before testing it.

## Your First Web App Test Walkthrough

Here's a simple workflow for testing a web application:

**Step 1: Browse the application normally**
With Intercept OFF, browse through the entire application. Burp builds
a site map automatically in the Target tab.

**Step 2: Identify interesting functionality**
Look for:
- Login forms
- Search boxes
- URL parameters (`?id=1`)
- File uploads
- Any user input

**Step 3: Test with Repeater**
For each interesting input, send the request to Repeater and try:
- SQL injection: `' OR '1'='1`
- XSS: `<script>alert(1)</script>`
- Parameter manipulation: change `id=1` to `id=2`

**Step 4: Document findings**
Note anything unusual in responses — error messages, different content,
unexpected behavior.

## Practice Burp Suite for Free

### TryHackMe Burp Suite Rooms
TryHackMe has dedicated Burp Suite rooms in the Jr Penetration Tester
path — these are the best structured way to learn it:
- Burp Suite: The Basics
- Burp Suite: Repeater
- Burp Suite: Intruder
- Burp Suite: Other Modules

[Start TryHackMe Free →](https://tryhackme.com)

### PortSwigger Web Security Academy
PortSwigger (makers of Burp Suite) have a completely free web security
training platform with hundreds of labs:
- Free forever
- Covers SQL injection, XSS, CSRF, and more
- Labs designed specifically for Burp Suite practice

[Web Security Academy →](https://portswigger.net/web-security)

### DVWA (Damn Vulnerable Web App)
Set up DVWA locally for offline practice:
```bash
# On Kali Linux
sudo apt install dvwa
```
Or run it in a [DigitalOcean VPS](https://m.do.co/c/a2644c2e88b4) —
new users get $200 free credits.

## Burp Suite Cheat Sheet

| Tool | Use Case |
|------|---------|
| Proxy → Intercept | Capture and modify requests |
| Proxy → HTTP History | Review all past requests |
| Repeater | Manual testing and modification |
| Intruder | Automated fuzzing and brute force |
| Decoder | Encode/decode Base64, URL, Hex |
| Target → Site Map | Map application structure |

## Community vs Professional — Do You Need Pro?

For learning and CTFs — **no**. Community Edition has everything you
need for your first 6-12 months.

The main things Pro adds:
- Automated vulnerability scanner
- Faster Intruder
- Advanced Repeater features
- Save projects between sessions

When you're doing professional engagements or bug bounty seriously,
Pro is worth it. For now stick with Community.

## Final Thoughts

Burp Suite has a steep learning curve but once it clicks everything
about web security makes more sense. The best way to learn it is
hands-on — work through the TryHackMe Burp Suite rooms and the
PortSwigger Web Security Academy labs.

Both are completely free and will take you from confused beginner to
confident web tester.

---
*Written from personal TryHackMe experience. Some links are affiliate
links which help support this site at no cost to you.*
