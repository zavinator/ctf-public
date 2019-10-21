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

