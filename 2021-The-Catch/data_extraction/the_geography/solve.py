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
