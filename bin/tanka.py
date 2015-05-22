#!/usr/bin/python
#coding: utf-8

import libtanka
import binascii
from pwn import *

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

# code = """
# b8 57 61 6b 61
# 53 50 ba 04 00 00 00
# bb 01 00 00 00
# b8 04 00 00 00 89 e1
# cd 80 58 31 c0 5b c3
# """
# 引用元
# http://kozos.jp/asm-tanka/

# code = binascii.unhexlify(code.translate(None,' \n'))

result = libtanka.composeTanka(code)
print "===短歌を詠んだ結果==="
print result

