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

