# Chapter 1: Operator

## Challenge

Hi, emergency troubleshooter,

recent studies suggest that the intense heat and hard labor of solar technicians often trigger strange, vivid dreams about the future of energetics. Over the past few days, technicians have woken up night after night with the same terrifying screams "Look, up in the sky! It's a bird! It's a plane! It's Superman! Let's roast it anyway!".

Find out what's going on, we need our technicians to stay sane.

Stay grounded!

http://intro.falcon.powergrid.tcc/

Hint: Be sure you enter flag for correct chapter.

Hint: In this realm, challenges should be conquered in a precise order, and to triumph over some, you'll need artifacts acquired from others - a unique twist that defies the norms of typical CTF challenges.

Hint: Chapter haiku will lead you.

Haiku:

```plain
Soft winds gently blow,
answers drift through open minds-
ease lives in the search.
```

http://roostguard.falcon.powergrid.tcc/

## TL;DR

We enumerated the host, discovered several HTTP endpoints on **RoostGuard**, and extracted the flag directly from the `/operator` page’s HTML using `curl` + `grep`.

## Scope & Targets

- Target host (from context):
  - `roostguard.falcon.powergrid.tcc`
  - IP (from scan): `10.99.25.154`
- Relevant services discovered: HTTP (80/tcp), RTMP (1935/tcp)

## Enumeration

### Full TCP Port Scan

```bash
nmap -p1-65535 10.99.25.154
```

```plain
Starting Nmap 7.95 ( https://nmap.org ) at 2025-10-16 23:25 CEST
Nmap scan report for 10.99.25.154
Host is up (0.025s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
80/tcp   open  http
1935/tcp open  rtmp
```

### HTTP Content Discovery

```bash
dirb http://roostguard.falcon.powergrid.tcc/ /usr/share/dirb/wordlists/big.txt
```

```plain
-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Thu Oct 16 23:29:18 2025
URL_BASE: http://roostguard.falcon.powergrid.tcc/
WORDLIST_FILES: /usr/share/dirb/wordlists/big.txt

-----------------

GENERATED WORDS: 20458             

---- Scanning URL: http://roostguard.falcon.powergrid.tcc/ ----
+ http://roostguard.falcon.powergrid.tcc/command (CODE:405|SIZE:153)        
+ http://roostguard.falcon.powergrid.tcc/login (CODE:200|SIZE:2213)         
+ http://roostguard.falcon.powergrid.tcc/logout (CODE:302|SIZE:199)         
+ http://roostguard.falcon.powergrid.tcc/operator (CODE:200|SIZE:3783)      
+ http://roostguard.falcon.powergrid.tcc/radar (CODE:302|SIZE:199)          
+ http://roostguard.falcon.powergrid.tcc/stats (CODE:200|SIZE:47)           
```

## Retrieving the Flag

```bash
curl -fsSL http://roostguard.falcon.powergrid.tcc/operator | grep -oE 'FLAG\{[^}]+\}'
```

## Flag

```plain
FLAG{AjQ6-NgLU-lQT7-XePG}
```
