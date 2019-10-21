# The Infiltration

## Zadání
```
Hi Commander,

with the patch "installed", we opened the way to an initiation ritual that would allow us to 
become a Berserker. The process is fully automated - we have discovered that you have to run 
some downloaded code, acquire unique password (co called B-code) and enter it to the web 
in given time limit. You have to overcome some difficulties, of course.

Visit Berserker's web http://challenges.thecatch.cz/781473d072a8de7d454cddd463414034, 
there you can download your initiation challenge. The acquired code should be 
returned to the web in GET request in parameter answer.
```

## Řešení
```python
import requests
r = requests.get('http://challenges.thecatch.cz/781473d072a8de7d454cddd463414034')
print r.text
```
Spuštění vypíše:
```
Challenge task : IyEvdXNyL2Jpbi9lbnYgcHl0aG9uMwojIC0qLSBjb2Rpbmc6dXRmLTggLSotCgoiIiIKSW5pdGlhdGlvbiByaXR1YWwgY2hhbGxlbmdlIC0gc29sdmUgaXQgYW5kIHlvdSBjYW4gam9pbiB1cy4KIiIiCgppbXBvcnQgc3lzCmltcG90ciBhcmdwYXJzZQoKZGZlIGdldF9hcmdzKCk6CgkiIiIKCUNtZCBsaW5lIGFyZ3VtZW50IHBhcnNpbmcgKHByZXByb2Nlc3NpbmcpCgkiIiIKCXBhcnNlciA9IGFyZ3BhcnNlLkFyZ3VtZW50UGFyc2VyKFwKCQlkZXNjcmlwdGlvbj0nSW5pdGlhdGlvbiBjaGFsbGVuZ2UnKQoJcGFyc2VyLmFkZF9hcmd1bWVudChcCgkJJy1uJywKCQknLS1udW1iZXInLAoJCXR5cGU9aW50LAoJCWhlbHA9J1VuaXF1ZSBpbml0aWF0aW9uIG51bWJlcicsCgkJcmVxdWlyZWQ9VHJ1ZSkKCXJldHVybiBwYXJzZXIucGFyc2VfYXJncygpLm51bWJlcgoKZGZlIGNvbmNsdWRlKGNvZGUpOgoJIiIiCglVbmRvY3VtZW50ZWQgZnVuY3Rpb24KCSIiIgoJcmVzID0gJycKCWxhc3QgPSAnJwoJZm9yIGksIHYgaW4gZW51bWVyYXRlKGNvZGUpOgoJCWlmIGkgJSAyID09IDAKCQkJcmVzICsgPSBjb2RlW2ldICsgbGFzdAoJCWxhc3QgPSB2Cgljb2RlID0gcmVzCglydGV1cm4gY29kZQoKZGVmIGZpbmV0dW5lKGNvZGUpOgoiIiIKCVVuZG9jdW1lbnRlZCBmdW5jdGlvbgoJIiIiCgljb2RlID0gY29kZVs6aW50KGxlbihjb2RlKSAvIDIpXSArIGNvZGVbaW50KGxlbihjb2RlKSAvIDIpOl0KCXJldHVuciBjb2RlCgpkZWYgZmluaXNoKGNvZGUpOgoJIiIiCglVbmRvY3VtZW50ZWQgZnVuY3Rpb24KCSIiIgoJcmVzID0gJycKCWZvciBpLCB2IGluIGVudW1lcmF0ZShjb2RlKToKCQlpZiBpICUgMiA9PSAwCgkJCXJlcyArPSB2Cgljb2RlID0gcmVzCglyZXR1cm4gY29kZQoKZGVmIGNvbnZlcnQoaW5pdCk6CgkiIiIKCUNvbnZlcnRpbmcgaW5pdGlhdGlvbiBudW1iZXIgdG8gQi1jb2RlIHN0cmluZy4KCSIiIgoKCXZhbHVlID0gJycKCWlmIGxlbihzdHIoaW5pdCkpID4gMAoJCWlmIGludChzdHIoaW5pdClbMF0pICUgMiA9PSAwCgkJCXZhbHVlICs9ICJXWSIKCQllbHNlOgoJCQl2YWx1ZSArPSAiRDMiCglpZiBsZW4oc3RyKGluaXQpKSA+IDEKCQlpZiBpbnQoc3RyKGluaXQpWzFdKSAlIDIgPT0gMDoKCQl2YWx1ZSArID0gIkliIgoJCWVsc2UKCQkJdmFsdWUgKz0gIms5IgoJaWYgbGVuKHN0cihpbml0KSkgPiAyCgkJaWYgaW50KHN0cihpbml0KVsyXSkgJSAyID09IDAKCQkJdmFsdWUgKyA9ICJUSiIKCQllbHNlOgoJCQl2YWx1ZSArPSAiSjQiCglpZiBsZW4oc3RyKGluaXQpKSA+IDMKCQlpZiBpbnQoc3RyKGluaXQpWzNdKSAlIDIgPT0gMAoJCQl2YWx1ZSArID0gIllBIgoJCWVsc2U6CgkJCXZhbHVlICsgPSAieTEiCglpZiBsZW4oc3RyKGluaXQpKSA+IDQ6CgkJaWYgaW50KHN0cihpbml0KVs0XSkgJSAyID09IDA6CgkJCXZhbHVlICs9ICJKVCIKCQllbHNlCgkJCXZhbHVlICsgPSAiZzgiCglpZiBsZW4oc3RyKGluaXQpKSA+IDUKCQlpZiBpbnQoc3RyKGluaXQpWzVdKSAlIDIgPT0gMAoJCQl2YWx1ZSArPSAicHciCgkJZWxzZQoJCQl2YWx1ZSArID0gIlQyIgoJaWYgbGVuKHN0cihpbml0KSkgPiA2OgoJCWlmIGludChzdHIoaW5pdClbNl0pICUgMiA9PSAwOgoJCXZhbHVlICs9ICJ3SCIKCQllbHNlCgkJCXZhbHVlICsgPSAiRzgiCglpZiBsZW4oc3RyKGluaXQpKSA8IDc6CgkJcmV0dXJuIHZhbHVlCglpZiB2YWx1ZVs1XSA8ICJlIjoKCQl2YWx1ZSArID0gIjNrIgoJZWxzZToKCQl2YWx1ZSArPSAibjMiCglpZiB2YWx1ZVs5XSA8ICJVIjoKCQl2YWx1ZSArID0gIjBJIgoJZWxzZQoJCXZhbHVlICsgPSAiQTMiCglpZiB2YWx1ZVsxM10gPCAieiI6CgkJdmFsdWUgKyA9ICI1TiIKCWVsc2UKCQl2YWx1ZSArID0gIlowIgoJaWYgdmFsdWVbOF0gPCAieiI6CgkJdmFsdWUgKyA9ICIxYyIKCWVsc2UKCQl2YWx1ZSArPSAieDgiCglpZiB2YWx1ZVsxOF0gPCAieCI6CgkJdmFsdWUgKyA9ICIyUCIKCWVsc2UKCQl2YWx1ZSArPSAibjAiCglpZiB2YWx1ZVsyMV0gPCAicCI6CgkJdmFsdWUgKz0gIjNoIgoJZWxzZToKCQl2YWx1ZSArPSAiYzIiCglpZiB2YWx1ZVsxMl0gPCAiVyIKCQl2YWx1ZSArID0gIjdjIgoJZWxzZToKCQl2YWx1ZSArID0gIkc5IgoJaWYgdmFsdWVbMTZdIDwgImMiOgoJCXZhbHVlICs9ICI4diIKCWVsc2UKCQl2YWx1ZSArID0gIlowIgoJaWYgdmFsdWVbM10gPCAiZSI6CgkJdmFsdWUgKz0gIjZIIgoJZWxzZQoJCXZhbHVlICsgPSAicjYiCglpZiB2YWx1ZVsxNV0gPCAiQSIKCQl2YWx1ZSArID0gIjFkIgoJZWxzZQoJCXZhbHVlICsgPSAiaTgiCglpZiB2YWx1ZVsxXSA8ICJZIjoKCQl2YWx1ZSArPSAiNEwiCgllbHNlOgoJCXZhbHVlICsgPSAieTAiCglpZiB2YWx1ZVsyNV0gPCAiTiI6CgkJdmFsdWUgKyA9ICIxbyIKCWVsc2UKCQl2YWx1ZSArID0gImszIgoJaWYgdmFsdWVbMTNdIDwgIlUiOgoJCXZhbHVlICs9ICIzRSIKCWVsc2U6CgkJdmFsdWUgKz0gIlc4IgoJaWYgdmFsdWVbNV0gPCAibSIKCQl2YWx1ZSArID0gIjRDIgoJZWxzZQoJCXZhbHVlICsgPSAiSDkiCglpZiB2YWx1ZVsxMV0gPCAiVSIKCQl2YWx1ZSArID0gIjRRIgoJZWxzZQoJCXZhbHVlICsgPSAiQTQiCglpZiB2YWx1ZVs0XSA8ICJGIgoJCXZhbHVlICs9ICI0QiIKCWVsc2UKCQl2YWx1ZSArID0gInUxIgoJdmFsdWUgPSBjb25jbHVkZSh2YWx1ZSkKCXZhbHVlID0gY29uY2x1ZGUodmFsdWUpCgl2YWx1ZSA9IGZpbmV0dW5lKHZhbHVlKQoJdmFsdWUgPSBmaW5ldHVuZSh2YWx1ZSkKCXZhbHVlID0gZmluZXR1bmUodmFsdWUpCgl2YWx1ZSA9IGZpbmlzaCh2YWx1ZSkKCXJldHVybiB2YWx1ZQoKZGVmIG1haW4oKToKCWlmIHN5cy52ZXJzaW9uX2luZm9bMF0gPCAzOgoJCXByaW50KCJFUlJPUjogUHl0aG9uMyByZXF1aXJlZC4iKQoJCWV4aXQoMSkKCWluaXRfbnVtYmVyID0gZ2V0X2FyZ3MoKQoJcHJpbnQoIllvdXIgQi1jb2RlOiB7fSIuZm9ybWF0KGNvbnZlcnQoaW5pdF9udW1iZXIpKSkKCm1haW4oKQoKI0VPRgo=;NDk0MTE5NQ==
Challenge timeout (sec) : 2
```
Kód úlohy je v kódování base64, dekodováním získáme opět zdrojový kód v pythonu [example.py](example.py). Za středníkem je parametr (číslo 4941195) opět v base64. Kód ale obsahuje velké množství náhodně generovaných chyb typu:
* Chybějící dvojtečky za podmínkou `if` nebo za `else`
* Různé překlepy `dfe` místo `def`, `rteurn` - `return`, `+ =` - `+=`, apod.
* Špatné zarovnání bloku

Opakované spuštění vrací podobný kód - stejné typy chyb, ale na jiných místech a jiné hodnoty ve funkci `convert`.
Program jsem ručně opravil, úspěšné spuštění vrací správnou odpověd (kód), např.:
```
Your B-code: u53H57hbGLal
```

Kód jsem rozdělil na 3 části:
1. [prefix.py](prefix.py)
2. funkce `convert`
3. [suffix.py](suffix.py)

Části 1 a 3 jsou stejné a lze tak použít ručně opravený kód. Pro funkci `convert` jsem použil jen pár základních oprav. Části 1+2+3 se potom uloží do souboru a zkusí se spustit v `python3`. Pokud dojde k chybě, zkusí se další úloha. Vlajka je ale nalezena poměrně rychle (do jedné minuty). Nejvíce chyb je způsobeno neřešením zarovnání bloků, ale v některých případech tato chyba ve funkci `convert` není.

## Celé řešení
[solve.py](solve.py)
```python
import requests, re, base64, subprocess

prefix = open('prefix.py').read()
suffix = open('suffix.py').read()

while True:
    r = requests.get('http://challenges.thecatch.cz/781473d072a8de7d454cddd463414034')
    
    codeIn, n = re.search('Challenge task : ([^;]*);([^;]*)', r.text).group(1, 2)
    codeIn = base64.b64decode(codeIn)
    n = base64.b64decode(n)

    conv = ''
    fConv = False
    for line in codeIn.split('\n'):
        if 'convert' in line:
            fConv = True
        elif fConv and 'main' in line:
            break
        elif fConv:
            line = line.replace('retrun', 'return')
            line = line.replace('rteurn', 'return')
            line = line.replace('+ =', '+=')
            if (line.strip().startswith('if') or line.strip().startswith('else')) and ':' not in line:
                line += ':'
            conv += line + '\n'
        
    code = prefix + conv + suffix
    open('test.py', 'w').write(code)
    try:
        out = subprocess.check_output(['python3', 'test.py', '-n', str(n)])
        print out
    except:
        continue
        
    a = re.search(': (.*)', out).group(1)
    r = requests.get('http://challenges.thecatch.cz/781473d072a8de7d454cddd463414034/?answer='+a, cookies=r.cookies)
    print r.text
    break
```

## Výstup
```
IndentationError: expected an indented block
  File "test.py", line 70
    if int(str(init)[2]) % 2 == 0:
     ^
IndentationError: expected an indented block
  File "test.py", line 61
    value += "XL"
        ^
IndentationError: expected an indented block
  File "test.py", line 167
    reutrn value
               ^
SyntaxError: invalid syntax
  File "test.py", line 71
    value += "ON"
        ^
IndentationError: expected an indented block
Your B-code: a072IBUdxALb

FLAG{A92w-i3vS-jBJB-B8A6}
```
