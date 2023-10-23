# Ship web server

## Zadání

```
Ahoy, deck cadet,

there are rumors that on the ship web server is not just the official presentation. Your task is to disprove or confirm these rumors.

May you have fair winds and following seas!

Ship web server is available at http://www.cns-jv.tcc.

Hint: Check the content of the certificate of the web.
Hint2: Visit the other web sites hosted on the same server. Don't let non-existent DNS records to stop you.
```

## Řešení

Docela obtížná úloha, která i podle průběhu soutěže dělala spoustu lidem problémy - později se proto objevil Hint2.
Ve zdrojovém kódu webu http://www.cns-jv.tcc je na konci:

```html
<small class="text-secondary" style="font-size: 7pt">ver. RkxBR3sgICAgLSAgICAtICAgIC0gICAgfQ==</small>
```

Dekódování base64: `FLAG{    -    -    -    }`

Takže vlajka asi bude mít čtyři části. Neplatný certifikát webu obsahuje v alternativním názvu subjektu:

```
Název DNS: www.cns-jv.tcc
Název DNS: documentation.cns-jv.tcc
Název DNS: home.cns-jv.tcc
Název DNS: pirates.cns-jv.tcc
Název DNS: structure.cns-jv.tcc
```

Ovšem kromě `www.cns-jv.tcc` (10.99.0.64) ostatní adresy nejsou v DNS. 
Tady jsem se na docela dlouho zasekl a asi jen díky tomu, že jsem hrál i minulé ročníky [Torso of Web Server](2021-The-Catch/system_access
/torso_of_web_server) jsem na to nakonec přišel.

Řešení je buď doplnit záznamy do `/etc/hosts` nebo podvrhnout `Host` přes `curl`:

```
curl -k -H "Host: documentation.cns-jv.tcc" https://10.99.0.64/

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Ship Portal</title>
  <link href="/bootstrap.min.css" rel="stylesheet">
    <link href="/style.css" rel="stylesheet">
  </head>
  <body>
    <div class="container">
      <main>
        <div class="alert alert-danger mt-5" role="alert">
  Unauthorized access to documentation!
</div>

<footer class="text-center p-1 position-absolute" style="left: 50%; bottom: 0; transform: translate(-50%);">
  <small class="text-secondary" style="font-size: 7pt"></small>
</footer>
      </main>
    </div>

      </body>
</html>
```

Část vlajky je v souboru `style.css`:

```
curl -k -H "Host: documentation.cns-jv.tcc" https://10.99.0.64/style.css

small::before{content:"ver. RkxBR3sgICAgLSAgICAtICAgIC1nTXdjfQ=="}
```

Dekódování base64: `FLAG{    -    -    -gMwc}`

Ostatní části:

```
curl -k -H "Host: home.cns-jv.tcc" https://10.99.0.64/?user 
curl -k -H "Host: pirates.cns-jv.tcc" https://10.99.0.64/
curl -k -H "Host: structure.cns-jv.tcc" https://10.99.0.64/
```

```
RkxBR3tlamlpLSAgICAtICAgIC0gICAgfQ==     FLAG{ejii-    -    -    }
RkxBR3sgICAgLSAgICAtUTUzQy0gICAgfQ==     FLAG{    -    -Q53C-    }
RkxBR3sgICAgLXBsbVEtICAgIC0gICAgfQ==     FLAG{    -plmQ-    -    }
```


### Vlajka

```
FLAG{ejii-plmQ-Q53C-gMwc}
```
