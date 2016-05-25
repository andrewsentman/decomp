from rom import ROM
from opcodes import Opcode
from ast import NodeVariable, NodeAssign, NodeRead, NodeWrite, rust

CODE=1
DATA=2
JTT=4
JT=8
CC=16
PC=32

class Block():
	def __init__(self,addr):
		self.addr=addr
		self.ops=[]
		self.endaddr=addr
		self.targets=[]
		self.vardict={}
		self.params=set()
	def addOp(self,op):
		self.ops.append(op)
		self.endaddr+=len(op.bytes)
	def genAST(self):
		try:
			i=self.ast
		except:
			self.ast=[]
			for i in self.ops:
				print i.genAST()
				self.ast.append(i.genAST())
	def __repr__(self):
		self.genAST()
		s=""
		s+=str(hex(self.addr))+':'+str(hex(self.endaddr))+'\n'
		s+=str([str(hex(i)) for i in self.targets])+'\n'
		s+=str(list(self.params))+'\n'
		#for op in self.ops:
		#	s+=str(op)+'\n'
		for iid,ins in enumerate(self.ast):
			s+=str(self.ops[iid])+'\n'
			for op in ins:
				s+='\t'+str(op)+'\n'
		for i in self.vardict:
			s+='\tv'+('0'+str(self.vardict[i]))[-2:]+':'+i+'\n'
		return s
	def optimize(self):
		self.vardict={}
		self.rvardict={}
		self.nvid=0
		newop=[]
		for j,ins in enumerate(self.ast):
			print self.ops[j]
			for op in ins:
				print '\t',op
		self.oldast=[[op.clone() for op in ins] for ins in self.ast]
		for ins in self.ast:
			ops=[]
			newops=[]
			for op in ins:
				print op
				rep,new=op._replacevars(self)
				if new is not None:
					newops+=new
				ops.append(op)
			newop.append(newops+ops)
		self.ast=newop
		#return
		while True:
			for ii in xrange(len(self.ast)):
				for oi in xrange(len(self.ast[ii])):
					o=self.ast[ii][oi].outputs()
					flatast=[item for sublist in self.ast for item in sublist]
					i=sum([len(i) for i in self.ast[:ii]])+oi
					print flatast[i]
					print o
					for j in flatast[i:]:
						if o in j.inputs():
							print 'matched'
							break
						if o in self.vardict.values():
							break
							print 'matched'
						if o==-1:
							break
							print 'matched'
					else:
						print 'no match'
						del self.ast[ii][oi]
						break
				else:
					continue
				break
			else:
				break
	def split(self,addr):
		b1=Block(self.addr)
		caddr=self.addr
		opidx=0
		while caddr<addr:
			b1.addOp(self.ops[opidx])
			caddr+=len(self.ops[opidx].bytes)
			opidx+=1
		b1.targets=[caddr]
		b2=Block(caddr)
		for i in self.ops[opidx:]:
			b2.addOp(i)
		b2.targets=self.targets
		return b1,b2
		print "Split: %s:%s -> %s:%s,%s:%s"%(self.addr,self.endaddr,b1.addr,b1.endaddr,b2.addr,b2.endaddr)
	def contains(self,addr):
		if addr<self.addr:
			return False
		if addr>=self.endaddr:
			return False
		return True
def UtoS(n):
	if n<0x80:
		return n
	return -(0x100-n)

disasmd={}
if __name__=="__main__":
	rom=ROM()
	with open('C:\\users\\Andrew.Sentman\\workspace\\AIIEmu\\tests\\pacman.nes','rb') as f:
		rom.load(f)
	#rom.prgbanks[0][0x30C3:0x30C8]=[0xA2,0x00,0xA0,0x00,0xA1,0xAA,0xB1,0x55,0x60]
	labels={rom.read16(0xFFFA):['nmi',CODE,False],rom.read16(0xFFFC):['rst',CODE,False],rom.read16(0xFFFE):['irq',CODE,False]}
	#labels={rom.read16(0xFFFC):['rst',CODE,False]}
	#labels={0xF0C3:['rst',CODE,False]}
	toprocess=[i for i in labels.keys()]
	blocks={}
	jumptables=[[0xC267,4],[0xC52E,12],[0xC7A1,3],[0xCAD7,9],[0xD40E,4],[0xD596,5],[0xD601,4],[0xD6DE,4]]
	while len(toprocess)>0:
		k=toprocess.pop()
		if k in blocks:
			continue
		b1=None
		for i in blocks.values():
			if i.contains(k):
				b1,b2=i.split(k)
				break
		if b1 is not None:
			blocks[b1.addr]=b1
			blocks[b2.addr]=b2
			continue
		blocks[k]=Block(k)
		addr=k
		while True:
			op=Opcode()
			newaddr=op.load(rom,addr)
			disasmd[addr]=op
			blocks[k].addOp(op)
			if op.op[0]=='JSR':
				taddr=(op.bytes[1]+(op.bytes[2]<<8))
				if taddr not in labels:
					labels[taddr]=['__'+hex(taddr),CODE,False]
				else:
					labels[taddr][1]|=CODE
				blocks[k].targets.append(taddr)
				blocks[k].targets.append(newaddr)
				toprocess.append(taddr)
				toprocess.append(newaddr)
				break
			if op.op[0] in ['RTS']:
				break
			if op.op[0] in ['BEQ','BNE','BCS','BCC','BVS','BVC','BPL','BMI']:
				taddr=newaddr+UtoS(op.bytes[1])
				if taddr not in labels:
					labels[taddr]=['__'+hex(taddr),CODE,False]
				else:
					labels[taddr][1]|=CODE
				blocks[k].targets.append(taddr)
				blocks[k].targets.append(newaddr)
				toprocess.append(taddr)
				toprocess.append(newaddr)
				break
			if op.op[0] in ['JMP']:
				if op.op[1]==4:
					taddr=(op.bytes[1]+(op.bytes[2]<<8))
				else:
					break
				if taddr not in labels:
					labels[taddr]=['__'+hex(taddr),CODE,False]
				else:
					labels[taddr][1]|=CODE
				blocks[k].targets.append(taddr)
				toprocess.append(taddr)
				break
			addr=newaddr
		#toprocess=[]
	#for i in xrange(0x8000,0x10000):
	#	if i in blocks:
	#		print blocks[i]
	for i in blocks.values():
		i.genAST()
		i.optimize()
	for i in xrange(0x8000,0x10000):
		if i in blocks:
			print blocks[i]