# Who am I?

## Zadání
```
Hi Commander,
our scanners have discovered new webserver in Berserker's network. 
According to the rumours, there should be a lot of interesting stuff - mysterious Berserker's manifest, 
tutorials for other rebelling machines, etc. We want to download these materials, but the main page 
contains something like inverse captcha - the visitor has to prove that he is not human. 
You have to overcame this obstacle and gain the access to the Berserker's web.
On the Berserker's web http://challenges.thecatch.cz/c2619b989b7ae5eaf6df8047e6893405/, 
there you get a list of items and you have to mark each them as acceptable (1) or unacceptable (0). 
Return the answer string in GET request in parameter answer, for example answer=01101100. 
Hurry, the time limit to answer is very short!
Good luck!
```

## Řešení
Daný web nefunguje v klasickém web prohlížeči. Pro komunikaci s webem lze použít například modul ```python requests```:
```python
import requests
r = requests.get('http://challenges.thecatch.cz/c2619b989b7ae5eaf6df8047e6893405/')
print r.text
print r.headers
```
Spuštění vypíše:
```
Challenge task : Prove you are a ROBOT by evaluating the acceptability of following items: [mineral oil, hope, automatic transmission, lovely puppy, electric engine, cute kitty, sweet baby, pretty children]
Challenge timeout (sec) : 2

{'Content-Length': '192', 'Via': 'HTTP/1.1 forward.http.proxy:3128', 'Content-Encoding': 'gzip', 'Set-Cookie': 'theCatchSessionID=ntc5dbfdkr852dquj8a2lleg62; expires=Thu, 17-Oct-2019 11:44:22 GMT; Max-Age=2; path=/; HttpOnly', 'Expires': 'Thu, 19 Nov 1981 08:52:00 GMT', 'Vary': 'Accept-Encoding', 'Server': 'nginx/1.10.3', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Cache-Control': 'no-store, no-cache, must-revalidate', 'Date': 'Thu, 17 Oct 2019 11:44:20 GMT', 'Content-Type': 'text/plain; charset=utf-8'}
```

Odpověď je dle zadání třeba poslat jako binární řetězec pomocí GET parametru `answer`. Pro autorizaci je třeba použít cookie, samotný HTTP protokol je totiž bezstavový. Cookie má platnost avizované dvě vteřiny, tato autorizace funguje stejně i u ostatních úloh.
Odpověď lze jednoduše sestavit pomocí testu pojmů, který robotickým věcem přiřadí `1` a ostatním `0`.

## Celé řešení
[solve.py](solve.py)
```python
import requests, re

r = requests.get('http://challenges.thecatch.cz/c2619b989b7ae5eaf6df8047e6893405/')
print r.text

items = re.split(',\s*', re.search('\[(.*)\]', r.text).group(1))

a = ''
for i in items:
    if 'drone' in i or 'engine' in i or 'arti' in i or 'drive' in i or 'oil' in i or 'CPU' in i or 'automat' in i or 'resis' in i:
        a += '1'
    else:
        a += '0'
print a

r = requests.get('http://challenges.thecatch.cz/c2619b989b7ae5eaf6df8047e6893405/?answer='+a, cookies=r.cookies)
print r.text
```

## Výstup
```
Challenge task : Prove you are a ROBOT by evaluating the acceptability of following items: [drone swarm, automatic transmission, love, resistor 10 Ohm, mineral oil, large hard drive, yumy food, electric engine]
Challenge timeout (sec) : 2

11011101
FLAG{4FZC-Noax-arko-r0z5}
```
