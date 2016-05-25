from rom import ROM
from opcodes import Opcode

CODE=1
DATA=2
JTT=4
JT=8
CC=16
PC=32

def UtoS(n):
	if n<0x80:
		return n
	return -(0x100-n)

disasmd={}
if __name__=="__main__":
	rom=ROM()
	with open('C:\\users\\Andrew.Sentman\\workspace\\AIIEmu\\tests\\pacman.nes','rb') as f:
		rom.load(f)
	labels={rom.read16(0xFFFA):['nmi',CODE,False],rom.read16(0xFFFD):['rst',CODE,False],rom.read16(0xFFFE):['irq',CODE,False]}
	jumptables=[[0xC267,4],[0xC52E,12],[0xC7A1,3],[0xCAD7,9],[0xD40E,4],[0xD596,5],[0xD601,4],[0xD6DE,4]]
	byteflags=[0]*0x10000
	for i in jumptables:
		for j in xrange(i[0],i[0]+i[1]*2):
			byteflags[j]|=JT
		for j in xrange(i[1]):
			taddr=rom.read16(i[0]+j*2)
			if taddr not in labels:
				labels[taddr]=['__'+hex(taddr),CODE|JTT,False]
			else:
				labels[taddr][1]|=CODE|JTT
	#print labels
	plen=0
	while len(labels)>plen:
		plen=len(labels)
		print len([i[0] for i in labels.values()])
		for k,v in labels.items():
			if not v[2] and v[1]:
				addr=k
				lcc=True
				lpc=True
				while True:
					op=Opcode()
					try:
						newaddr=op.load(rom,addr)
					except:
						break
					for i in xrange(addr,newaddr):
						if lcc:
							byteflags[i]|=CC
						if lpc:
							byteflags[i]|=PC
					disasmd[addr]=op
					#print op
					if op.op[0]=='JSR':
						taddr=(op.bytes[1]+(op.bytes[2]<<8))
						if taddr not in labels:
							labels[taddr]=['__'+hex(taddr),CODE,False]
						else:
							labels[taddr][1]|=CODE
						lcc=False
					elif op.op[0] in ['BEQ','BNE','BCS','BCC','BVS','BVC','BPL','BMI']:
						taddr=addr+UtoS(op.bytes[1])
						if taddr not in labels:
							labels[taddr]=['__'+hex(taddr),CODE,False]
						else:
							labels[taddr][1]|=CODE
						lcc=False
						lpc=False
					addr=newaddr
	#print labels
	'''
	for i in xrange(0xC000,0x10000):
		if i in labels:
			print labels[i][0]+':'
		if i in disasmd:
			print '\t'+str(disasmd[i])'''
	for i in xrange(0x8000,0x10000,0x16):
		print str(hex(i))+':',
		for j in xrange(0x16):
			print byteflags[i+j],
		print