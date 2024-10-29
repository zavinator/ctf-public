# Long Secure Password

## Challenge

Hi, TCC-CSIRT analyst,

A new colleague came up with a progressive way of creating a memorable password and would like to implement it as a new standard at TCC. Each user receives a TCC-CSIRT password card and determines the password by choosing the starting coordinate, direction, and number of characters. For skeptics about the security of such a solution, he published the card with a challenge to log in to his SSH server.

Verify if the card method has any weaknesses by logging into the given server.

Download the password card  
(sha256 checksum: 9a35dc6284c8bde03118321b86476cf835a3b48a5fcf09ad6d64af22b9e555ca)  
The server has the domain name `password-card-rules.cypherfix.tcc` and the colleague's username is `futurethinker`.

See you in the next incident!

Hint: The entropy is at first glance significantly lower than that of a randomly generated password.  
Hint: We know that the colleague's favorite number is 18, so it can be assumed that the password has this length as well.

## Solution

This challenge was solved with the help of ChatGPT, which facilitated the processing and automation of the password card logic, enabling us to generate and test potential passwords efficiently. Below are the steps taken, including the prompts used in ChatGPT to achieve the solution.

### 1. Convert the Password Card to Text

We first uploaded the password card into ChatGPT and used the following prompt to convert the image into text:

**Prompt:** 

```
Convert this password card to text (include chars and also *)
```

ChatGPT provided a first draft of the card, and we made some necessary corrections, resulting in the following password card:

```
SQUIRELL*JUDGE*NEWS*LESSON
WORRY*UPDATE*SEAFOOD*CROSS
CHAPTER*SPEEDBUMP*CHECKERS
PHONE*HOPE*NOTEBOOK*ORANGE
CARTOONS*CLEAN*TODAY*ENTER
ZEBRA*PATH*VALUABLE*MARINE
VOLUME*REDUCE*LETTUCE*GOAL
BUFFALOS*THE*CATCH*SUPREME
LONG*OCTOPUS*SEASON*SCHEME
CARAVAN*TOBACCO*WORM*XENON
PUPPYLIKE*WHATEVER*POPULAR
SALAD*UNKNOWN*SQUATS*AUDIT
HOUR*NEWBORN*TURN*WORKSHOP
USEFUL*OFFSHORE*TOAST*BOOK
COMPANY*FREQUENCY*NINETEEN
AMOUNT*CREATE*HOUSE*FOREST
BATTERY*GOLDEN*ROOT*WHEELS
SHEEP*HOLIDAY*APPLE*LAWYER
SUMMER*HORSE*WATER*SULPHUR
```

### 2. Python Solver Implementation

To automate the password guessing process, we used the following prompt in ChatGPT to generate the core of a Python program using `pwntools`:

**Prompt:**

```
Implement a program in python using pwntools that will try to ssh to account futurethinker@password-card-rules.cypherfix.tcc. 
Try all passwords with these rules:
- try all starting points in the password card
- choose a direction (left, right, up, down, 2xdiagonal) and go straight in any direction until you reach the edge or the length of password is 18
- do not check passwords that you've already checked
- include only passwords of length 18
- the passwords consists of chars or *
```

### 3. Fixing Code Issues

Some minor issues in the initial code output were resolved, and with ChatGPT's assistance, the program was fine-tuned to handle connection retries.

[solver.py](solver.py)

### 4. Running the Program

Once the final version of the program was ready, we ran it to try all possible 18-character passwords from the card. Here's a snippet of the output showing successful login:

```bash
Trying password: SHEEP*HOLIDAY*APPL
[-] Connecting to password-card-rules.cypherfix.tcc on port 22: Failed
Authentication failed.
Trying password: SAOPUNUKTPHCANEMFW
[+] Connecting to password-card-rules.cypherfix.tcc on port 22: Done
[!] Only Linux is supported for ASLR checks.
[!] Only Linux is supported for userspace shadow stack checks.
[!] Only Linux is supported for kernel indirect branch tracking checks.
[*] futurethinker@password-card-rules.cypherfix.tcc:
    Distro    Unknown Unknown
    OS:       Unknown
    Arch:     Unknown
    Version:  0.0.0
    ASLR:     Disabled
    SHSTK:    Disabled
    IBT:      Disabled
    Note:     Susceptible to ASLR ulimit trick (CVE-2016-3672)
Successful login with password: SAOPUNUKTPHCANEMFW
[+] Opening new channel: 'shell': Done
[*] Switching to interactive mode
Nobody will ever read this message anyway, because the TCC password card is super secure. Even my lunch access-code is safe here: FLAG{uNZm-GGVK-JbxV-1DIx}
[*] Got EOF while reading in interactive
```

## Flag

```
FLAG{uNZm-GGVK-JbxV-1DIx}
```
