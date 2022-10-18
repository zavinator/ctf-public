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


