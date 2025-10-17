# Chapter 4: Is not free

## Challenge

Hi, emergency troubleshooter,

recent studies suggest that the intense heat and hard labor of solar technicians often trigger strange, vivid dreams about the future of energetics. Over the past few days, technicians have woken up night after night with the same terrifying screams "Look, up in the sky! It's a bird! It's a plane! It's Superman! Let's roast it anyway!".

Find out what's going on, we need our technicians to stay sane.

Stay grounded!

http://intro.falcon.powergrid.tcc/

Hint: Be sure you enter flag for correct chapter.

Hint: In this realm, challenges should be conquered in a precise order, and to triumph over some, you'll need artifacts acquired from others - a unique twist that defies the norms of typical CTF challenges.

Hint: Chapter haiku will lead you.

Haiku:

```plain
Respect the craft's birth,
Code is earned, not taken swift-
Licence guards its worth. 
```

http://thevendor.falcon.powergrid.tcc/

## TL;DR

The **VERS** routine in firmware applies an **RC4‑like** stream cipher to a stored licence number using a key derived from a validator string. With the artifacts from previous chapters, we replicated the transform and recovered the flag.

## Recognition

- Haiku clearly points to **licence** / licensing.
- LCD shows licence details when **VERS** is invoked.
- Decompilation of `processVERSCommand()` reveals:
  - Copy 0x19‑byte `licenceNumber` buffer.
  - Hex‑decode `validator` (`licence2`).
  - RC4‑style KSA (`licence3`, S‑box size 179) and PRGA (`licence4`) over licence buffer.
  - CRC‑32 (`licence5`) before printing to LCD/serial.

### Decompiled VERS

```c
uchar * processVERSCommand(void)
{
  byte bVar1;
  uint uVar2;
  uchar *puVar3;
  char *pcVar4;
  uchar *puVar5;
  char in_Hflg;
  char in_Tflg;
  char in_Iflg;
  undefined1 auStackY_14 [3];
  size_t __size;
  
  R1 = '\0';
  __size = CONCAT31(CONCAT21(CONCAT11(R17R16._0_1_,R17R16._1_1_),(byte)Y),Y._1_1_);
  R25R24 = (uchar *)malloc(__size);
  R17R16 = R25R24;
  Z = &licenceNumber;
  X = R25R24;
  R25R24._0_1_ = '\x19';
  do {
    puVar5 = Z;
    puVar3 = X;
    Z = Z + 1;
    R0 = *puVar5;
    X = X + 1;
    *puVar3 = R0;
    R25R24._0_1_ = (char)R25R24 + -1;
  } while ((char)R25R24 != '\0');
  Z = R17R16;
  R17R16[0x19] = R1;
  Y = &validator;
  do {
    pcVar4 = Y;
    Y = Y + 1;
    R0 = *pcVar4;
  } while (R0 != '\0');
  bVar1 = Y._1_1_ - (((byte)Y == '\0') + '\x01');
  Y._1_1_ = bVar1 >> 1;
  Y._0_1_ = bVar1 * -0x80 | (byte)((byte)Y - 1) >> 1;
  R25R24 = (uchar *)malloc(__size);
  R15R14 = R25R24;
  licence2(&validator,R25R24,(uint)Y);
  Z._0_1_ = (byte)R15R14;
  Z._1_1_ = (char)((uint)R15R14 >> 8);
  Z = (uchar *)CONCAT11(Z._1_1_ + Y._1_1_ + CARRY1((byte)Z,(byte)Y),(byte)Z + (byte)Y);
  *Z = R1;
  licence3(R15R14,(int)Y);
  licence4(R17R16,0x19);
  licence5(R17R16,0x19);
  R25R24 = R17R16;
  free(R17R16);
  R25R24 = R15R14;
  free(R15R14);
  auStackY_14 = (undefined1  [3])0x15f5;
  snprintf(&outText,R23R22);
  auStackY_14 = (undefined1  [3])0x15f9;
  LiquidCrystal_I2C::clear((LiquidCrystal_I2C *)lcd);
  auStackY_14 = (undefined1  [3])0x15ff;
  Print::print((Print *)lcd,(char *)0x250);
  auStackY_14 = (undefined1  [3])0x1605;
  Print::print((Print *)lcd,(char *)0x257);
  auStackY_14 = (undefined1  [3])0x160b;
  LiquidCrystal_I2C::setCursor((LiquidCrystal_I2C *)lcd,'\0','\x01');
  auStackY_14 = (undefined1  [3])0x1611;
  Print::print((Print *)lcd,s_Licence_mem_025c);
  auStackY_14 = (undefined1  [3])0x1617;
  Print::print((Print *)lcd,&outText);
  auStackY_14 = (undefined1  [3])0x161d;
  Print::println(neoSerial);
  uVar2 = CONCAT11((char)((uint)(auStackY_14 + 2) >> 8),(char)auStackY_14 + '\x02');
  R25R24 = (uchar *)(uVar2 + 10);
  R0 = 0xfff5 < uVar2 | (R25R24 == (uchar *)0x0) << 1 | ((int)R25R24 < 0) << 2 |
       SCARRY2((int)R25R24,10) << 3 | ((int)R25R24 < 0 != SCARRY2((int)R25R24,10)) << 4 |
       (in_Hflg == '\x01') << 5 | (in_Tflg == '\x01') << 6 | (in_Iflg == '\x01') << 7;
  SREG = R0;
  Y._1_1_ = *(undefined1 *)(uVar2 + 0xb);
  Y._0_1_ = *(undefined1 *)(uVar2 + 0xc);
  R17R16._1_1_ = *(undefined1 *)(uVar2 + 0xd);
  R17R16._0_1_ = *(undefined1 *)(uVar2 + 0xe);
  R15R14._1_1_ = *(undefined1 *)(uVar2 + 0xf);
  R15R14._0_1_ = *(undefined1 *)(uVar2 + 0x10);
  R13 = *(undefined1 *)(uVar2 + 0x11);
  R12 = *(undefined1 *)(uVar2 + 0x12);
  return R25R24;
}
```

## ChatGPT‑assisted reversing

### Prompt used

> **Prompt:** “Try to rewrite this Arduino program (from Ghidra) to Python and explain the functionality.”  
> **Context supplied:** the `processVERSCommand` decompilation and the observed helper names `licence1..5`.

### What GPT inferred

- `licence1` acts as a **hex nibble** decoder (lowercase).
- `licence2` performs **hex‑to‑bytes** using `licence1` (lax on invalids).
- `licence3` implements an **RC4‑style KSA**, but with **S‑box size 179** instead of 256.
- `licence4` implements the **RC4 PRGA** (keystream XOR) using the same modulus.
- `licence5` is a **bitwise CRC‑32** (reflected polynomial `0xEDB88320`).

### GPT‑provided Python reconstruction

```python
from typing import List, Tuple
import binascii

# --- helpers reused from your previous step ---

def licence1(ch: str) -> int:
    """lowercase hex digit -> nibble; anything else -> 0 (matches decompiled behavior)."""
    if '0' <= ch <= '9':
        return ord(ch) - 0x30
    if 'a' <= ch <= 'f':
        return ord(ch) - 0x57
    return 0

def licence2(src: str, out_buf: bytearray, n: int) -> str:
    """hex-decode `n` bytes from `src` using licence1 (lowercase only; invalid -> 0)."""
    for i in range(n):
        hi = licence1(src[2*i])
        lo = licence1(src[2*i + 1])
        out_buf[i] = ((hi << 4) | lo) & 0xFF
    return src


# --- 1) licence3: RC4-like KSA with nonstandard S-box length 179 ---

N = 179  # 0xB3 - inferred from the pointer arithmetic (+0xB3/-0x4C) in the AVR code

def licence3(key: bytes, key_len: int) -> List[int]:
    """
    Key-scheduling step.
    Matches the structure of RC4 KSA but modulo 179 instead of 256.
    Returns the initialized S box (list of 0..178) permuted by the key.
    """
    if key_len <= 0:
        key = b""
    else:
        key = key[:key_len]

    S = list(range(N))
    j = 0
    for i in range(N):
        j = (j + S[i] + key[i % len(key)] if key else (j + S[i])) % N
        S[i], S[j] = S[j], S[i]
    return S


# --- 2) licence4: PRGA (keystream + XOR) using that S-box ---

def licence4(buf: bytearray, S: List[int]) -> None:
    """
    Stream cipher step (encrypt/decrypt in-place).
    RC4-like PRGA modulo 179; swaps S[i], S[j], outputs S[(S[i]+S[j]) % N] as keystream.
    """
    i = 0
    j = 0
    for k in range(len(buf)):
        i = (i + 1) % N
        j = (j + S[i]) % N
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % N]
        buf[k] ^= K


# --- 3) licence5: CRC-32 (IEEE) computed bit-by-bit (reflected) ---

def licence5(data: bytes) -> int:
    """
    Equivalent to CRC-32/IEEE (poly 0x04C11DB7, reflected; XOR-out 0xFFFFFFFF).
    The AVR code splits the 32-bit CRC into two 16-bit halves and uses 0xEDB88320;
    this is the standard reflected CRC-32 bitwise algorithm.
    """
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xEDB88320
            else:
                crc >>= 1
    return crc ^ 0xFFFFFFFF


# --- 4) A direct translation of processVERSCommand's core logic ---

def process_VERS_command(licence_number_bytes: bytes, validator_hex_lower: str) -> Tuple[bytes, int]:
    """
    Mirrors what the AVR code does, minus LCD/printf and raw register shuffling:

    1) Copy licenceNumber (25 bytes)
    2) Take validator C-string, compute its length, halve it (that's the hex->bytes length)
    3) Decode validator from hex via licence2 (lowercase, lax)
    4) licence3(key, key_len) to build S
    5) licence4() to XOR-stream cipher the licenceNumber buffer in place
    6) licence5() to compute CRC-32 of the (transformed) licence buffer
    7) Return transformed licence bytes + CRC
    """
    # Step 1: take exactly 0x19 (25) bytes and null-terminate (the C code does this)
    buf = bytearray(licence_number_bytes[:0x19])
    if len(buf) < 0x19:
        buf += b"\x00" * (0x19 - len(buf))

    # Step 2–3: prepare key from validator (C code takes strlen, halves it)
    # Here: decode the largest even-length prefix of validator_hex_lower.
    key_n = len(validator_hex_lower) // 2
    key = bytearray(key_n)
    licence2(validator_hex_lower, key, key_n)  # uses the lax/LC hex rules

    # Step 4: KSA
    S = licence3(bytes(key), len(key))

    # Step 5: PRGA over the 25-byte licence buffer
    licence4(buf, S)

    # Step 6: CRC-32 of result
    crc32_val = licence5(bytes(buf))

    # (C code then frees buffers and prints to LCD)
    return bytes(buf), crc32_val
```

### CyberChef

We verified the final plaintext using classic RC4 in CyberChef (the observed pairing decrypts cleanly under standard RC4 as well).

- **Key (Hex):** `54687265654c6974746c654269726473`  *(ASCII: ThreeLittleBirds)*
- **Data (Hex):** `5a15339de0ba7121cb056a8aca36b2990afb239a17c9572996`

https://gchq.github.io/CyberChef/#recipe=RC4(%7B'option':'Hex','string':'54687265654c6974746c654269726473'%7D,'Hex','Latin1')&input=NWExNTMzOWRlMGJhNzEyMWNiMDU2YThhY2EzNmIyOTkwYWZiMjM5YTE3Yzk1NzI5OTY&oeol=CR

## Flag

```plain
FLAG{KfcP-HeZQ-luKY-mIxB}
```

Note: **first blood** achievement due to clever usage of ChatGPT! :)
