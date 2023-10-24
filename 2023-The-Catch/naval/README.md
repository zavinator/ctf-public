# Naval chef's recipe

## Zadání

```
Ahoy, officer,

some of the crew started behaving strangely after eating the chef's speciality of the day - they apparently have hallucinations, because they are talking about sirens wailing, kraken on starboard, and accussed the chef being reptilian spy. Paramedics are getting crazy, because the chef refuses to reveal what he used to make the food. Your task is to find his secret recipe. It should be easy as the chef knows only security by obscurity and he has registered domain chef-menu.galley.cns-jv.tcc. May you have fair winds and following seas!

The chef's domain is chef-menu.galley.cns-jv.tcc.
```

## Řešení

```bash
nmap -T4 -A -v chef-menu.galley.cns-jv.tcc

Discovered open port 80/tcp on 10.99.0.32
Discovered open port 443/tcp on 10.99.0.32

PORT    STATE SERVICE VERSION
80/tcp  open  http    Apache httpd (PHP 8.2.10)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache
|_http-title: 301 Moved Permanently
443/tcp open  ssl/ssl Apache httpd (SSL-only mode)
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
```

```
curl http://chef-menu.galley.cns-jv.tcc

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
  <title>301 Moved Permanently</title>
  <meta http-equiv="refresh" content="0;url=https://chef-menu.galley.cns-jv.tcc">
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="https://chef-menu.galley.cns-jv.tcc">here</a>.</p>
<p style="display: none">The secret ingredient is composed of C6H12O6, C6H8O6, dried mandrake, FLAG{ytZ6-Pewo-iZZP-Q9qz}, and C20H25N3O. Shake, do not mix.</p>
<script>window.location.href='https://chef-menu.galley.cns-jv.tcc'</script>
</body></html>
```

Web HTTP na portu 80 obsahuje přesměrování na HTTPS, takže klasický grafický browser zobrazí ihned https web, kde ale vlajka není.

## Vlajka

```
FLAG{ytZ6-Pewo-iZZP-Q9qz}
```
