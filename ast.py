NR=0
DR=1
AR=2
def UtoS(n):
	if n<0x80:
		return n
	return -(0x100-n)
class Node2():
	def __init__(self,a,b):
		self.a=a
		self.b=b
	def _replacevars(self,block):
		addops=[]
		rep,cr=self.a._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.a.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.a=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.a))
					self.a=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		rep,cr=self.b._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.b.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.b=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.b))
					self.b=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		return self.repvar(),addops
	def output(self):
		return None
	def inputs(self):
		oa=[]
		if isinstance(self.a,NodeVariable):
			oa.append(self.a.id)
		else:
			oa+=self.a.inputs()
		if isinstance(self.b,NodeVariable):
			oa.append(self.b.id)
		else:
			oa+=self.b.inputs()
		return oa
class Node1():
	def __init__(self,a):
		self.a=a
	def _replacevars(self,block):
		addops=[]
		rep,cr=self.a._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.a.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.a=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.a))
					self.a=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		return self.repvar(),addops
	def output(self):
		return None
	def inputs(self):
		if isinstance(self.a,NodeVariable):
			return [self.a.id]
		return self.a.inputs()
class NodeIf(Node2):
	def __repr__(self):
		return 'IF '+repr(self.a)+' THEN '+repr(self.b)
	def clone(self):
		return NodeIf(self.a.clone(),self.b.clone())
	def repvar(self):
		return False
	def outputs(self):
		return -1
class NodeAssign(Node2):
	def __repr__(self):
		return repr(self.a)+'<-'+repr(self.b)
	def clone(self):
		return NodeAssign(self.a.clone(),self.b.clone())
	def repvar(self):
		return False
	def _replacevars(self,block):
		addops=[]
		rep,cr=self.b._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.b.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.b=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.b))
					self.b=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		rep,cr=self.a._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.a.uniqstr()
			newvar=NodeVariable(block.nvid)
			self.a=newvar
			block.vardict[ust]=block.nvid
			block.nvid+=1
		return False,addops
	def outputs(self):
		if isinstance(self.a,NodeVariable):
			return self.a.id
		if isinstance(self.a,NodeTempVar):
			return str(self.a.id)+'.'+str(self.a.addr)
	def inputs(self):
		if isinstance(self.b,NodeVariable):
			return [self.b.id]
		if isinstance(self.b,NodeTempVar):
			return [str(self.b.id)+'.'+str(self.b.addr)]
		return self.b.inputs()

class NodeRead():
	def __init__(self,a):
		self.a=a
		self.newa=None
	def __repr__(self):
		return 'in '+repr(self.a)+(':'+repr(self.newa) if self.newa is not None else '')
	def clone(self):
		return NodeRead(self.a.clone())
	def _replacevars(self,block):
		ust=self.a.uniqstr()
		block.params.add(ust)
		self.newa=self.a.clone()
		addops=[]
		rep,cr=self.newa._replacevars(block)
		if not rep:
			assert False
			addops+=cr
		else:
			ust=self.newa.uniqstr()
			if ust is not None:
				block.params.add(ust)
				newvar=NodeVariable(block.nvid)
				addops.append(NodeAssign(newvar,self.a))
				self.a=newvar
				block.vardict[ust]=block.nvid
				block.nvid+=1
			else:
				assert False
		return False,addops
		return False,[]
		addops=[]
		ust=self.a.uniqstr()
		if ust is not None:
			newvar=NodeVariable(block.nvid)
			self.newa=newvar
			block.vardict[ust]=block.nvid
			block.nvid+=1
		return False,addops
	def outputs(self):
		return -1
	def inputs(self):
		if isinstance(self.a,NodeVariable):
			return [self.a]
		return self.a.inputs()
class NodeWrite():
	def __init__(self,a):
		self.a=a
		self.newa=None
	def __repr__(self):
		return 'out '+repr(self.a)+(':'+repr(self.newa) if self.newa is not None else '')
	def clone(self):
		return NodeWrite(self.a.clone())
	def _replacevars(self,block):
		addops=[]
		rep,cr=self.a._replacevars(block)
		if not rep:
			assert False
			addops+=cr
		else:
			ust=self.a.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.newa=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.a))
					self.a=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
			else:
				assert False
		return False,addops
	def outputs(self):
		return -1
		if self.newa is not None:
			return self.newa.id
	def inputs(self):
		if isinstance(self.a,NodeVariable):
			return [self.a]
		return self.a.inputs()
class NodeRead(NodeAssign):
	def __repr__(self):
		return repr(self.a)+'<r-'+repr(self.b)
	def outputs(self):
		return -1
class NodeWrite(NodeAssign):
	def __repr__(self):
		return repr(self.a)+'<w-'+repr(self.b)
	def outputs(self):
		return -1
class NodeEqual(Node2):
	def __repr__(self):
		return '('+repr(self.a)+') == ('+repr(self.b)+')'
	def clone(self):
		return NodeEqual(self.a.clone(),self.b.clone())
	def repvar(self):
		return False
class NodeNE(Node2):
	def __repr__(self):
		return '('+repr(self.a)+') != ('+repr(self.b)+')'
	def clone(self):
		return NodeNE(self.a.clone(),self.b.clone())
	def repvar(self):
		return False
class NodeGT(Node2):
	def __repr__(self):
		return '('+repr(self.a)+') > ('+repr(self.b)+')'
	def clone(self):
		return NodeGT(self.a.clone(),self.b.clone())
	def repvar(self):
		return False
class NodeBit(Node1):
	def __init__(self,a,value):
		self.a=a
		self.value=value
	def __repr__(self):
		return '('+repr(self.a)+') bit '+str(self.value)
	def clone(self):
		return NodeBit(self.a.clone(),self.value)
	def repvar(self):
		return False
class NodeBranch(Node1):
	ainvar=True
	def __repr__(self):
		return 'BR '+repr(self.a)
	def clone(self):
		return NodeBranch(self.a.clone())
	def repvar(self):
		return False
class NodeJSR(Node1):
	def __repr__(self):
		return 'JSR '+repr(self.a)
	def clone(self):
		return NodeJSR(self.a.clone())
class NodeByte(Node1):
	def __repr__(self):
		return 'm'+repr(self.a)
class NodeCMP(Node2):
	def __repr__(self):
		return repr(self.a)+'-'+repr(self.b)
	def clone(self):
		return NodeCMP(self.a.clone(),self.b.clone())
class NodeEOR(Node2):
	def __repr__(self):
		return repr(self.a)+' XOR '+repr(self.b)
class NodeOR(Node2):
	def __repr__(self):
		return repr(self.a)+' OR '+repr(self.b)
	def clone(self):
		return NodeOR(self.a.clone(),self.b.clone())
class NodeAND(Node2):
	def __repr__(self):
		return repr(self.a)+' AND '+repr(self.b)
	def clone(self):
		return NodeAND(self.a.clone(),self.b.clone())
	def repvar(self):
		return False
class NodeADC():
	def __init__(self,a,b,c):
		self.a=a
		self.b=b
		self.c=c
	def __repr__(self):
		return '('+repr(self.a)+') + ('+repr(self.b)+') + '+repr(self.c)
	def clone(self):
		return NodeADC(self.a.clone(),self.b.clone(),self.c.clone())
	def inputs(self):
		oa=[]
		if isinstance(self.a,NodeVariable):
			oa.append(self.a.id)
		else:
			oa+=self.a.inputs()
		if isinstance(self.b,NodeVariable):
			oa.append(self.b.id)
		else:
			oa+=self.b.inputs()
		if isinstance(self.c,NodeVariable):
			oa.append(self.c.id)
		else:
			oa+=self.c.inputs()
		return oa
	def _replacevars(self,block):
		addops=[]
		rep,cr=self.a._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.a.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.a=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.a))
					self.a=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		rep,cr=self.b._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.b.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.b=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.b))
					self.b=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		rep,cr=self.c._replacevars(block)
		if not rep:
			addops+=cr
		else:
			ust=self.c.uniqstr()
			if ust is not None:
				if ust in block.vardict:
					self.c=NodeVariable(block.vardict[ust])
				else:
					block.params.add(ust)
					newvar=NodeVariable(block.nvid)
					addops.append(NodeAssign(newvar,self.c))
					self.c=newvar
					block.vardict[ust]=block.nvid
					block.nvid+=1
		return False,addops
class NodeSBC():
	def __init__(self,a,b,c):
		self.a=a
		self.b=b
		self.c=c
	def __repr__(self):
		return repr(self.a)+' - '+repr(self.b)+') - '+repr(self.c)
	def clone(self):
		return NodeSBC(self.a.clone(),self.b.clone(),self.c.clone())
class NodeCarry():
	def __repr__(self):
		return 'CARRY'
	def clone(self):
		return NodeCarry()
	def _replacevars(self,block):
		return False,[]
	def inputs(self):
		return [-1]
class NodeASL(Node2):
	def __repr__(self):
		return 'ASL '+repr(self.a)+' c '+repr(self.b)
	def clone(self):
		return NodeASL(self.a.clone(),self.b.clone())
class NodeROR(Node2):
	def __repr__(self):
		return 'ROR '+repr(self.a)+' c '+repr(self.b)
	def clone(self):
		return NodeROR(self.a.clone(),self.b.clone())
class NodeLSR(Node2):
	def __repr__(self):
		return 'LSR '+repr(self.a)+' c '+repr(self.b)
	def clone(self):
		return NodeLSR(self.a.clone(),self.b.clone())
class NodePush(Node1):
	def __repr__(self):
		return 'Push '+repr(self.a)
	def clone(self):
		return NodePush(self.a.clone())
	def outputs(self):
		return -1
	def repvar(self):
		return False
class NodePull():
	def __repr__(self):
		return 'Pull'
	def clone(self):
		return NodePull()
	def _replacevars(self,block):
		return False,[]
	def inputs(self):
		return [-1]
class NodeDecrement(Node1):
	ainvar=True
	def __repr__(self):
		return repr(self.a)+'--'
	def clone(self):
		return NodeDecrement(self.a.clone())
	def repvar(self):
		return False
class NodeIncrement(Node1):
	def __repr__(self):
		return repr(self.a)+'++'
	def clone(self):
		return NodeIncrement(self.a.clone())
	def repvar(self):
		return False
class NodeNop():
	def __repr__(self):
		return 'NOP'
	def clone(self):
		return NodeNop()
	def replacevars(self,block):
		return None
class NodeRTS():
	def __repr__(self):
		return 'RTS'
	def clone(self):
		return NodeRTS()
	def _replacevars(self,block):
		return False,[]
	def inputs(self):
		return [-1]
	def outputs(self):
		return -1
class NodeRTI():
	def __repr__(self):
		return 'RTI'
	def clone(self):
		return NodeRTI()
	def _replacevars(self,block):
		return False,[]
	def inputs(self):
		return [-1]
	def outputs(self):
		return -1
class NodeLocImmediate():
	def __init__(self,value):
		self.value=value
	def clone(self):
		return NodeLocImmediate(self.value)
	def __repr__(self):
		return '#'+str(hex(self.value))[2:]
	def uniqstr(self):
		return None
	def _replacevars(self,block):
		return True,None
	def inputs(self):
		return []
class NodeFlagVal():
	def __init__(self,value):
		self.value=value
	def __repr__(self):
		return str(self.value)
	def clone(self):
		return NodeFlagVal(self.value)
	def uniqstr(self):
		return None
	def _replacevars(self,block):
		return True,None
	def inputs(self):
		return []
class NodeLocReg():
	def __init__(self,value):
		self.value=value
	def __repr__(self):
		return 'r'+str(self.value)
	def clone(self):
		return NodeLocReg(self.value)
	def uniqstr(self):
		return 'r'+str(self.value)
	def _replacevars(self,block):
		return True,None
	def inputs(self):
		return []
class NodeLocAbsolute():
	def __init__(self,value):
		self.value=value
	def __repr__(self):
		return '$'+str(hex(self.value))[2:]
	def clone(self):
		return NodeLocAbsolute(self.value)
	def uniqstr(self):
		return '$'+str(hex(self.value))[2:]
	def _replacevars(self,block):
		return False,[]
	def inputs(self):
		return []
class NodeLocRel():
	def __init__(self,value):
		self.value=value
	def __repr__(self):
		if UtoS(self.value)>0:
			return 'PC+'+str(hex(UtoS(self.value)))[2:]
		return 'PC-'+str(hex(-UtoS(self.value)))[2:]
	def uniqstr(self):
		return None
	def _replacevars(self,block):
		return False,[]
	def clone(self):
		return NodeLocRel(self.value)
	def inputs(self):
		return []
class NodeLocIndirect(Node1):
	def __repr__(self):
		return '<'+repr(self.a)+'>'
	def clone(self):
		return NodeLocIndirect(self.a.clone())
	def uniqstr(self):
		return '<'+self.a.uniqstr()+'>'
	def repvar(self):
		return False
class NodeLocIndexed(Node2):
	def __repr__(self):
		return repr(self.a)+'['+repr(self.b)+']'
	def clone(self):
		return NodeLocIndexed(self.a.clone(),self.b.clone())
	def uniqstr(self):
		return self.a.uniqstr()+'['+self.b.uniqstr()+']'
	def repvar(self):
		return False
class NodeVariable():
	def __init__(self,id):
		self.id=id
	def __repr__(self):
		return 'v'+str(self.id)
	def _replacevars(self,block):
		return False,[]
	def uniqstr(self):
		return 'v'+str(self.id)
class NodeTempVar():
	def __init__(self,addr,id):
		self.addr=addr
		self.id=id
	def __repr__(self):
		return 'tv'+str(self.addr)+'.'+str(self.id)
	def _replacevars(self,block):
		return False,[]
	def uniqstr(self):
		return 'tv'+str(self.addr)+'.'+str(self.id)
	def clone(self):
		return NodeTempVar(self.addr,self.id)
	def inputs(self):
		return [-1]
	def outputs(self):
		return [-1]
def rust(ust):
	if ust[0]=='r':
		return NodeLocReg(ust[1:])
	elif ust[0]=='$':
		return NodeLocAbsolute(int(ust[1:]))
	else:
		print ust
		return 5/0