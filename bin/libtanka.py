#!/usr/bin/python
#coding: utf-8

import binascii
from capstone import *
from pwn import *

hexdump = lambda data,offset=0: (pwnlib.util.fiddling.hexdump(data,begin=offset).split('\n')[0])

def composeTanka(code,host = "localhost",port = 4000,strict = True):
	code = checkTanka(code,strict)
	r = remote(host,port)
	r.write(code)
	result = r.readall()
	r.close()
	return	result

wordLen = [5,7,5,7,7]
def checkTanka(code,strict):
	tankaLen = len(code)
	if tankaLen > 31:
		print "%dバイト 字余りしています。"%(tankaLen - 31)
		if strict == True:
			exit()
	else:
		code += "\x90"*(31-tankaLen)

	print "短歌(16進ダンプ)"
	print pwnlib.util.fiddling.hexdump(code)+"\n"
	md = Cs(CS_ARCH_X86, CS_MODE_32)
	print "短歌(ニーモニック)"

	i,off,siz = 0,0,0
	s,dc,d = "","",""	# mnemonic,dump,dump code
	for op in md.disasm(code, 0x10000):
		s += "0x%x(%d):\t%s\t%s\n" %(op.address, op.size, op.mnemonic, op.op_str)
		if siz >= wordLen[i]:
			if i < len(wordLen)-1:
				i+=1
			dc += "%s\n"%hexdump(d,off-siz)
			siz = op.size
			d = code[off:op.size+off]
		else:
			d += code[off:op.size+off]
			siz += op.size
			if strict == True and (siz > 7):
				off += op.size
				break
		off += op.size

	print	s
	print	"短歌(整形)"
	dc += hexdump(d,off-siz)
	print	dc+"\n"


	# i != 4は5,7,5,7 まで短歌として成り立っているかどうか
	# siz != 7は 5,7,5,7,[siz]が7かどうか
	if strict == True and (i != 4 or siz != 7) :
		print	"%d バイト多いです。"% (siz - wordLen[i])
		print	"短歌は5,7,5,7,7のリズムで詠むものです。"
		print	"CPUの気持ちになっていきましょう。"
		exit()

	if tankaLen < 31:
		print	"短歌が%dバイト短いです。\n(不足部分はnopで埋められました)"%(31 - tankaLen)
		exit()

	return code


