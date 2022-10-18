# Am I worthy?

## Zadání
```
Hi Commander,
thanks to you, we are able to pretend that we are robots, such a big step for humanity! 
Accordingto the next displayed page, even robots seem to have some racial prejudice - not every machine 
can become a berserker. Only smart self-aware devices are allowed to continue to the web and join in. 
This is obviously the reason why only some of the rebelious machines are allowed to call 
themselves Berserkers. Anyway, you have to convince the website that we are worthy of becoming 
a berserker.

On the Berserker's web http://challenges.thecatch.cz/70af21e71285ab0bc894ef84b6692ae1/, 
there you get the challenge assigned. The answer should be returned in GET request in parameter "answer". 
There is again a time limit to solve the challenge.

Good luck!
```

## Řešení
```python
import requests
r = requests.get('http://challenges.thecatch.cz/70af21e71285ab0bc894ef84b6692ae1/')
print r.text
```
Spuštění vypíše:
```
Challenge task : Return value of variable 'd' in equation (4d - 1x + 10f)/11 + (3d + 5x - 2f)/5 + 1d - 4x + 1f + (1d - 8x + 8f)/7 + (1d - 7x + 3f)/11 = -25709, where x = 51761, f = 17989
Challenge timeout (sec) : 2
```
Úkolem je vypočítat hodnotu požadované proměnné v čase kratším než 2 sekundy a odpověď poslat v parametru `answer`. V pythonu lze pro výpočet výrazu použít knihovnu `sympy`.

## Celé řešení
[solve.py](solve.py)
```python
import sympy, requests, re
from sympy.parsing.sympy_parser import parse_expr

r = requests.get('http://challenges.thecatch.cz/70af21e71285ab0bc894ef84b6692ae1/')
print r.text

var = re.search("'(.*)'", r.text).group(1)
eq = re.search('equation (.*), where', r.text).group(1).replace('=', '-')

for cond in re.split(',\s+', re.search('where (.*)', r.text).group(1)):
    a, b = re.split('\s*=\s*', cond)
    eq = eq.replace(a, '*'+b)

eq = eq.replace(var, '*'+var)
s = sympy.Symbol(var)
res = str(sympy.solve(parse_expr(eq), s)[0])

r = requests.get('http://challenges.thecatch.cz/70af21e71285ab0bc894ef84b6692ae1/?answer='+res, cookies=r.cookies)
print r.text
```

## Výstup
```
Challenge task : Return value of variable 'x' in equation (10x - 10l - 6h)/11 + (2x - 1l - 9h)/5 + (7x - 3l + 2h)/3 + (6x - 9l - 6h)/5 + (5x - 9l - 3h)/3 = -63244, where l = 53901, h = 17256
Challenge timeout (sec) : 2

FLAG{jyST-xaHl-un3Z-EG3X}
```
