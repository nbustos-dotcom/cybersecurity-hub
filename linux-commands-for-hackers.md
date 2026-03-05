# Linux Commands Every Hacker Should Know (Beginner Guide 2026)

Linux is the foundation of cybersecurity. Whether you're doing CTFs,
pentesting, or just setting up a lab, you'll be living in the terminal.
I'm a CS student at Michigan Tech and when I first sat down at a Linux
terminal it was intimidating — this guide is what I wish I had.

The good news: you only need about 20 commands to get started. Here they are.

## Why Linux for Cybersecurity?

- Almost every pentesting tool runs on Linux
- Kali Linux (the standard pentesting OS) is Linux
- Most servers you'll encounter run Linux
- TryHackMe and HackTheBox machines are almost always Linux

If you're not comfortable in a Linux terminal yet, this guide is your
starting point.

## Getting a Linux Terminal to Practice On

Before we dive in, you need somewhere to practice. Options:

- **TryHackMe** — browser-based Linux terminal, no setup needed.
  [Start free →](https://tryhackme.com)
- **VirtualBox** — free software to run Kali Linux on your own machine
- **DigitalOcean** — spin up a Linux VPS for $4/mo,
  [$200 free credits for new users](https://m.do.co/c/a2644c2e88b4)

## Navigation Commands

These are the first commands you need to know — think of them as moving
around your computer through the terminal.

### pwd — Where Am I?
Shows your current location in the filesystem:
```bash
pwd
# Output: /home/user
```

### ls — What's Here?
Lists files and folders in your current directory:
```bash
ls          # basic list
ls -la      # detailed list including hidden files
ls -lh      # human readable file sizes
```
The `-la` flag is the one you'll use most — it shows hidden files
(files starting with `.`) which are important in CTFs.

### cd — Move Around
Change directory:
```bash
cd /home/user        # go to specific path
cd ..                # go up one level
cd ~                 # go to home directory
cd -                 # go back to previous directory
```

### find — Search for Files
One of the most useful commands in CTFs:
```bash
find / -name "flag.txt"           # find a file by name
find / -name "*.txt"              # find all .txt files
find / -perm -4000 2>/dev/null    # find SUID files (privilege escalation)
```

## File Commands

### cat — Read a File
```bash
cat file.txt              # print file contents
cat -n file.txt           # with line numbers
```

### grep — Search Inside Files
Incredibly powerful — search for text inside files:
```bash
grep "password" file.txt          # find "password" in a file
grep -r "password" /var/www/      # search recursively in a directory
grep -i "password" file.txt       # case insensitive search
```
In CTFs, `grep` is how you find flags and passwords hidden in files.

### cp, mv, rm — Copy, Move, Delete
```bash
cp file.txt backup.txt            # copy a file
mv file.txt /tmp/file.txt         # move a file
rm file.txt                       # delete a file
rm -rf /tmp/folder/               # delete a folder (be careful!)
```

### mkdir — Make a Directory
```bash
mkdir myfolder                    # create a folder
mkdir -p tools/nmap/results       # create nested folders
```

## File Permissions

Understanding permissions is essential for privilege escalation in CTFs.

### chmod — Change Permissions
```bash
chmod +x script.sh        # make a script executable
chmod 777 file.txt        # full permissions for everyone
chmod 644 file.txt        # standard file permissions
```

### Reading Permission Output
When you run `ls -la` you see something like:
```
-rwxr-xr-x 1 user group 1234 Jan 1 file.sh
```
Breaking it down:
- `-` = file type (d = directory)
- `rwx` = owner permissions (read, write, execute)
- `r-x` = group permissions
- `r-x` = everyone else

### chown — Change Ownership
```bash
chown user:group file.txt         # change owner and group
sudo chown root file.txt          # give root ownership
```

## Networking Commands

### ifconfig / ip addr — What's My IP?
```bash
ifconfig                  # show network interfaces (older)
ip addr                   # show network interfaces (newer)
ip addr show eth0         # show specific interface
```

### ping — Is the Target Alive?
```bash
ping 10.10.10.1           # send ping packets
ping -c 4 10.10.10.1      # send exactly 4 packets
```
Always ping your target first on TryHackMe to confirm the machine is up.

### netstat / ss — What Connections Are Active?
```bash
netstat -tulpn            # show listening ports
ss -tulpn                 # modern alternative to netstat
```

### curl — Make Web Requests
```bash
curl http://10.10.10.1              # basic GET request
curl -I http://10.10.10.1          # headers only
curl -X POST http://10.10.10.1     # POST request
```
Essential for web application testing.

## Process Management

### ps — What's Running?
```bash
ps aux                    # show all running processes
ps aux | grep apache      # find specific process
```

### kill — Stop a Process
```bash
kill 1234                 # kill process by ID
kill -9 1234              # force kill
killall firefox           # kill by name
```

### top / htop — System Monitor
```bash
top                       # basic system monitor
htop                      # better version (install with apt)
```

## Essential Shortcuts and Tips

### sudo — Run as Administrator
```bash
sudo command              # run single command as root
sudo su                   # switch to root user
sudo -l                   # list what you can run as sudo (CTF gold)
```
`sudo -l` is one of the first things to run in a CTF — it shows if you
can escalate privileges.

### Tab Completion
Press **Tab** to autocomplete commands and filenames. Saves enormous
amounts of typing.

### Command History
```bash
history                   # show command history
!!                        # repeat last command
!nmap                     # repeat last nmap command
```

### Piping — Chain Commands Together
The `|` character sends output from one command to another:
```bash
ps aux | grep apache      # find apache processes
cat file.txt | grep flag  # search file for "flag"
ls -la | sort             # sort directory listing
```

## Quick Reference Cheat Sheet

| Command | What it Does |
|---------|-------------|
| `pwd` | Show current directory |
| `ls -la` | List all files including hidden |
| `cd ..` | Go up one directory |
| `find / -name file` | Search for a file |
| `cat file.txt` | Read a file |
| `grep "text" file` | Search inside a file |
| `chmod +x file` | Make file executable |
| `ifconfig` | Show IP addresses |
| `ping <ip>` | Check if host is alive |
| `ps aux` | Show running processes |
| `sudo -l` | List sudo permissions |
| `history` | Show command history |

## Practice These Commands for Free

The fastest way to learn Linux is hands-on:

- **TryHackMe Linux Fundamentals** — three free rooms dedicated to Linux
  basics. [Start here →](https://tryhackme.com)
- **OverTheWire Bandit** — a wargame that teaches Linux through puzzles.
  Completely free. [Start here →](https://overthewire.org/wargames/bandit/)
- **Your own lab** — set up Kali Linux in
  [VirtualBox](https://virtualbox.org) or on a
  [DigitalOcean VPS](https://m.do.co/c/a2644c2e88b4)

## Final Thoughts

You don't need to memorize every command — you just need to know they exist
and roughly what they do. Google and `man <command>` (the built-in manual)
fill in the rest.

Focus on navigation, grep, find, and networking commands first. Those four
categories cover 80% of what you'll use in CTFs and TryHackMe rooms.
---
*Written from experience as a CS student learning cybersecurity. Some links
are affiliate links which help support this site at no cost to you.*
---
*Written from experience as a CS student learning cybersecurity. Some links
are affiliate links which help support this site at no cost to you.*
