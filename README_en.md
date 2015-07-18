# what is libtanka?
libtanka is japanese tanka style assembly programming framework.  
Tanka is 5-7-5-7-7 style japanese short poem. (see [Tanka(Wikipedia)](https://en.wikipedia.org/wiki/Tanka)
)  

most tanka style programming to optimal CPU is Intel x86.  
assembly tanka is opcode exactly 31 bytes.  

# What can this program
* Check 5-7-5-7-7 style.
* Compiled into the execution of the mnemonic is not required.
* Tanka form of program is also directly executable.

# setup
* build  
```
git clone https://github.com/segfo/libtanka
cd libtanka
./configure CFLAGS='-g -O0';make
```

* tanka execution module(tanka32) execute.  
```
qira -s ./src/tanka32
```

* sample tanka execution  
```
chmod 755 ./bin/tanka.py
./bin/tanka.py
```

# API
libtanka.composeTanka( code, host = "localhost", port = 4000,  strict = True )
* `code` : tanka binary(string)
* `host` : host name qira is running (default localhost)
* `port` : port number qira is running (default 4000)  
* `strict` : strict with an extra syllable (default True(bad tanka is do not execute))

# usage example( hexdump )
```
import libtanka
import binascii

code = """
b8 57 61 6b 61
53 50 ba 04 00 00 00
bb 01 00 00 00
b8 04 00 00 00 89 e1
cd 80 58 31 c0 5b c3
"""
# ASCII -> binary
code = binascii.unhexlify(code.translate(None,' \n'))
result = libtanka.composeTanka(code)
print result
```

# usage example( mnemonic )
```
import libtanka
import binascii

code = """
mov eax,0x21216e6f
push eax
mov eax,0x68747950
push eax
xor edx,edx
inc edx
mov ebx,edx
shl edx,2
mov eax,edx
shl edx,1
mov ecx,esp
int 0x80
pop eax
pop eax
ret
"""
code = asm(code) # assemble

result = libtanka.composeTanka(code)
print result
```

# tanka example
## Good tanka  
mnemonic(x86 assembly)
```
mov eax,0x21216e6f (5 bytes)

push eax           (1 bytes)
mov eax,0x68747950 (5 bytes)
push eax           (1 bytes (1+5+1 = 7 bytes))

xor edx,edx        (2 bytes)
inc edx            (1 bytes)
mov ebx,edx        (2 bytes (2+1+2 = 5 bytes))

shl edx,2          (3 bytes)
mov eax,edx        (2 bytes)
shl edx,1          (2 bytes (3+2+2 = 7 bytes))

mov ecx,esp        (2 bytes)
int 0x80           (2 bytes)
pop eax            (1 bytes)
pop eax            (1 bytes)
ret                (1 bytes (2+2+1+1+1 = 7 bytes))
```
Machine language(x86)
```
00000000  b8 6f 6e 21 21
00000005  50 b8 50 79 74 68 50
0000000c  31 d2 42 89 d3
00000011  c1 e2 02 89 d0 d1 e2
00000018  89 e1 cd 80 58 58 c3
```

## Bad tanka
mnemonic(x86 assembly)
```
mov    eax, 0x21216e6f (5 bytes)

push    eax            (1 bytes)
mov    eax, 0x68747950 (5 bytes)
push    eax            (1 bytes(1+5+1 = 7 bytes))

mov    edx, 0          (5 bytes)

inc    edx             (1 bytes)
mov    ebx, edx        (2 bytes)
shl    edx, 2          (3 bytes)
mov    eax, edx        (2 bytes(1+2+3+2 = 8 bytes(bad)))

shl    edx, 1          (2 bytes)
mov    ecx, esp        (2 bytes)
int    0x80            (2 bytes)
pop    eax             (1 bytes(2+2+2+1 = 7 bytes))

pop    eax             (1 bytes(total 31bytes over))
ret                    (1 bytes(total 31bytes over))
```

Machine language(x86)
```
b8 6f 6e 21 21
50 b8 50 79 74 68 50
ba 00 00 00 00 <-- too long. very bad...(and also contains a null character, bad as shellcode.)
42 89 d3 c1 e2 02 89 d0 <-- 1 bytes over
d1 e2 89 e1 cd 80 58
58 c3 <-- 2 bytes over
```

# required library
[pwntools](https://github.com/Gallopsled/pwntools)  
[capstone](https://github.com/aquynh/capstone)  
[qira](https://github.com/BinaryAnalysisPlatform/qira)  
