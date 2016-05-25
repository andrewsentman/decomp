from rom import ROM
from ast import *

IMM =0
ZP  =1
ZPX =2
ZPY =3
ABS =4
ABSX=5
ABSY=6
INDX=7
INDY=8
ACC =9
REL =10
IMP =11
IND =12

ops={
0x69:["ADC",IMM,2,2,"CZidbVN"],
0x65:["ADC",ZP,2,3,"CZidbVN"],
0x75:["ADC",ZPX,2,4,"CZidbVN"],
0x6d:["ADC",ABS,3,4,"CZidbVN"],
0x7d:["ADC",ABSX,3,4,"CZidbVN"],
0x79:["ADC",ABSY,3,4,"CZidbVN"],
0x61:["ADC",INDX,2,6,"CZidbVN"],
0x71:["ADC",INDY,2,5,"CZidbVN"],

0x29:["AND",IMM,2,2,"cZidbvN"],
0x25:["AND",ZP,2,3,"cZidbvN"],
0x35:["AND",ZPX,2,4,"cZidbvN"],
0x2d:["AND",ABS,3,4,"cZidbvN"],
0x3d:["AND",ABSX,3,4,"cZidbvN"],
0x39:["AND",ABSY,3,4,"cZidbvN"],
0x21:["AND",INDX,2,6,"cZidbvN"],
0x31:["AND",INDY,2,5,"cZidbvN"],

0x0a:["ASL",ACC,1,2,"CZidbvN"],
0x06:["ASL",ZP,2,5,"CZidbvN"],
0x16:["ASL",ZPX,2,6,"CZidbvN"],
0x0e:["ASL",ABS,3,6,"CZidbvN"],
0x1e:["ASL",ABSX,3,7,"CZidbvN"],

0x90:["BCC",REL,2,2/3,"czidbvn"],
0xB0:["BCS",REL,2,2/3,"czidbvn"],
0xF0:["BEQ",REL,2,2/3,"czidbvn"],
0x30:["BMI",REL,2,2/3,"czidbvn"],
0xD0:["BNE",REL,2,2/3,"czidbvn"],
0x10:["BPL",REL,2,2/3,"czidbvn"],
0x50:["BVC",REL,2,2/3,"czidbvn"],
0x70:["BVS",REL,2,2/3,"czidbvn"],

0x24:["BIT",ZP,2,3,"cZidbVN"],
0x2c:["BIT",ABS,3,4,"cZidbVN"],

0x00:["BRK",IMP,1,7,"czidbvn"],
0x18:["CLC",IMP,1,2,"Czidbvn"],
0xd8:["CLD",IMP,1,2,"cziDbvn"],
0x58:["CLI",IMP,1,2,"czIdbvn"],
0xb8:["CLV",IMP,1,2,"czidbVn"],
0xea:["NOP",IMP,1,2,"czidbvn"],
0x48:["PHA",IMP,1,3,"czidbvn"],
0x68:["PLA",IMP,1,4,"cZidbvN"],
0x08:["PHP",IMP,1,3,"czidbvn"],
0x28:["PLP",IMP,1,4,"CZIDBVN"],
0x40:["RTI",IMP,1,6,"czidbvn"],
0x60:["RTS",IMP,1,6,"czidbvn"],
0x38:["SEC",IMP,1,2,"Czidbvn"],
0xf8:["SED",IMP,1,2,"cziDbvn"],
0x78:["SEI",IMP,1,2,"czIdbvn"],
0xaa:["TAX",IMP,1,2,"cZidbvN"],
0x8a:["TXA",IMP,1,2,"cZidbvN"],
0xa8:["TAY",IMP,1,2,"cZidbvN"],
0x98:["TYA",IMP,1,2,"cZidbvN"],
0xba:["TSX",IMP,1,2,"cZidbvN"],
0x9a:["TXS",IMP,1,2,"czidbvn"],

0xc9:["CPA",IMM,2,2,"CZidbvN"],
0xc5:["CPA",ZP,2,3,"CZidbvN"],
0xd5:["CPA",ZPX,2,4,"CZidbvN"],
0xcd:["CPA",ABS,3,4,"CZidbvN"],
0xdd:["CPA",ABSX,3,4,"CZidbvN"],
0xd9:["CPA",ABSY,3,4,"CZidbvN"],
0xc1:["CPA",INDX,2,6,"CZidbvN"],
0xd1:["CPA",INDY,2,5,"CZidbvN"],

0xe0:["CPX",IMM,2,2,"CZidbvN"],
0xe4:["CPX",ZP,2,3,"CZidbvN"],
0xec:["CPX",ABS,3,4,"CZidbvN"],

0xc0:["CPY",IMM,2,2,"CZidbvN"],
0xc4:["CPY",ZP,2,3,"CZidbvN"],
0xcc:["CPY",ABS,3,4,"CZidbvN"],

0xc6:["DEC",ZP,2,5,"cZidbvN"],
0xd6:["DEC",ZPX,2,6,"cZidbvN"],
0xce:["DEC",ABS,3,6,"cZidbvN"],
0xde:["DEC",ABSX,3,7,"cZidbvN"],

0xca:["DEX",IMP,1,2,"cZidbvN"],
0x88:["DEY",IMP,1,2,"cZidbvN"],
0xe8:["INX",IMP,1,2,"cZidbvN"],
0xc8:["INY",IMP,1,2,"cZidbvN"],

0x49:["EOR",IMM,2,2,"cZidbvN"],
0x45:["EOR",ZP,2,3,"cZidbvN"],
0x55:["EOR",ZPX,2,4,"cZidbvN"],
0x4d:["EOR",ABS,3,4,"cZidbvN"],
0x5d:["EOR",ABSX,3,4,"cZidbvN"],
0x59:["EOR",ABSY,3,4,"cZidbvN"],
0x41:["EOR",INDX,2,6,"cZidbvN"],
0x51:["EOR",INDY,2,5,"cZidbvN"],

0xe6:["INC",ZP,2,5,"cZidbvN"],
0xf6:["INC",ZPX,2,6,"cZidbvN"],
0xee:["INC",ABS,3,6,"cZidbvN"],
0xfe:["INC",ABSX,3,7,"cZidbvN"],

0x4c:["JMP",ABS,3,3,"czidbvn"],
0x6c:["JMP",IND,3,5,"czidbvn"],
0x20:["JSR",ABS,3,6,"czidbvn"],

0xa9:["LDA",IMM,2,2,"cZidbvN"],
0xa5:["LDA",ZP,2,3,"cZidbvN"],
0xb5:["LDA",ZPX,2,4,"cZidbvN"],
0xad:["LDA",ABS,3,4,"cZidbvN"],
0xbd:["LDA",ABSX,3,4,"cZidbvN"],
0xb9:["LDA",ABSY,3,4,"cZidbvN"],
0xa1:["LDA",INDX,2,6,"cZidbvN"],
0xb1:["LDA",INDY,2,5,"cZidbvN"],

0xa2:["LDX",IMM,2,2,"cZidbvN"],
0xa6:["LDX",ZP,2,3,"cZidbvN"],
0xb6:["LDX",ZPY,2,4,"cZidbvN"],
0xae:["LDX",ABS,3,4,"cZidbvN"],
0xbe:["LDX",ABSY,3,4,"cZidbvN"],

0xa0:["LDY",IMM,2,2,"cZidbvN"],
0xa4:["LDY",ZP,2,3,"cZidbvN"],
0xb4:["LDY",ZPX,2,4,"cZidbvN"],
0xac:["LDY",ABS,3,4,"cZidbvN"],
0xbc:["LDY",ABSX,3,4,"cZidbvN"],

0x4a:["LSR",ACC,1,2,"CZidbvN"],
0x46:["LSR",ZP,2,5,"CZidbvN"],
0x56:["LSR",ZPX,2,6,"CZidbvN"],
0x4e:["LSR",ABS,3,6,"CZidbvN"],
0x5e:["LSR",ABSX,3,7,"CZidbvN"],

0x09:["ORA",IMM,2,2,"cZidbvN"],
0x05:["ORA",ZP,2,3,"cZidbvN"],
0x15:["ORA",ZPX,2,4,"cZidbvN"],
0x0d:["ORA",ABS,3,4,"cZidbvN"],
0x1d:["ORA",ABSX,3,4,"cZidbvN"],
0x19:["ORA",ABSY,3,4,"cZidbvN"],
0x01:["ORA",INDX,2,6,"cZidbvN"],
0x11:["ORA",INDY,2,5,"cZidbvN"],

0x2a:["ROL",ACC,1,2,"CZidbvN"],
0x26:["ROL",ZP,2,5,"CZidbvN"],
0x36:["ROL",ZPX,2,6,"CZidbvN"],
0x2e:["ROL",ABS,3,6,"CZidbvN"],
0x3e:["ROL",ABSX,3,7,"CZidbvN"],

0x6a:["ROR",ACC,1,2,"CZidbvN"],
0x66:["ROR",ZP,2,5,"CZidbvN"],
0x76:["ROR",ZPX,2,6,"CZidbvN"],
0x7e:["ROR",ABS,3,6,"CZidbvN"],
0x6e:["ROR",ABSX,3,7,"CZidbvN"],

0xe9:["SBC",IMM,2,2,"CZidbVN"],
0xe5:["SBC",ZP,2,3,"CZidbVN"],
0xf5:["SBC",ZPX,2,4,"CZidbVN"],
0xed:["SBC",ABS,3,4,"CZidbVN"],
0xfd:["SBC",ABSX,3,4,"CZidbVN"],
0xf9:["SBC",ABSY,3,4,"CZidbVN"],
0xe1:["SBC",INDX,2,6,"CZidbVN"],
0xf1:["SBC",INDY,2,5,"CZidbVN"],

0x85:["STA",ZP,2,3,"czidbvn"],
0x95:["STA",ZPX,2,4,"czidbvn"],
0x8d:["STA",ABS,3,4,"czidbvn"],
0x9d:["STA",ABSX,3,5,"czidbvn"],
0x99:["STA",ABSY,3,5,"czidbvn"],
0x81:["STA",INDX,2,6,"czidbvn"],
0x91:["STA",INDY,2,6,"czidbvn"],

0x86:["STX",ZP,2,3,"czidbvn"],
0x96:["STX",ZPY,2,4,"czidbvn"],
0x8e:["STX",ABS,3,4,"czidbvn"],
0x84:["STY",ZP,2,3,"czidbvn"],
0x94:["STY",ZPX,2,4,"czidbvn"],
0x8c:["STY",ABS,3,4,"czidbvn"]
}

class Opcode():
	def load(self,rom,addr):
		self.addr=addr
		self.opid=rom.read(addr)
		self.op=ops[self.opid]
		self.bytes=[rom.read(addr+i) for i in xrange(self.op[2])]
		return addr+self.op[2]
	def __repr__(self):
		return str(hex(self.addr))+':'+self.op[0]+str(self.bytes)
	def genAST(self):
		print self.op
		if self.op[0] in ['LDA','LDX','LDY']:
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			print sourcenode
			return snr+[
						NodeAssign(NodeLocReg(self.op[0][2]),sourcenode),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(sourcenode,NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(sourcenode,7))
					]
		if self.op[0] in ['STA','STX','STY']:
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return [
						NodeAssign(sourcenode,NodeLocReg(self.op[0][2]))
					]+snw
		if self.op[0] in ['SEI','SEC']:
			return [
						NodeAssign(NodeLocReg('f'+self.op[0][2]),NodeFlagVal(True))
					]
		if self.op[0] in ['CLD','CLC']:
			return [
						NodeAssign(NodeLocReg('f'+self.op[0][2]),NodeFlagVal(False))
					]
		if self.op[0] in ['DEX','DEY']:
			return [
						NodeAssign(NodeLocReg(self.op[0][2]),
						NodeDecrement(NodeLocReg(self.op[0][2]))),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg(self.op[0][2]),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg(self.op[0][2]),7))
					]
		if self.op[0] in ['INC']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(sourcenode,NodeIncrement(sourcenode)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(sourcenode,NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(sourcenode,7)),
					]+snw
		if self.op[0] in ['DEC']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(sourcenode,NodeDecrement(sourcenode)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(sourcenode,NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(sourcenode,7)),
					]
		if self.op[0] in ['INX','INY']:
			return [
						NodeAssign(NodeLocReg(self.op[0][2]),NodeIncrement(NodeLocReg(self.op[0][2]))),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg(self.op[0][2]),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg(self.op[0][2]),7))
					]
		if self.op[0] in ['TXS']:
			return [
						NodeAssign(NodeLocReg(self.op[0][2]),NodeLocReg(self.op[0][1]))
					]
		if self.op[0] in ['TAY','TAX','TXA','TYA']:
			return [
						NodeAssign(NodeLocReg(self.op[0][2]),NodeLocReg(self.op[0][1])),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg(self.op[0][2]),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg(self.op[0][2]),7))
					]
		if self.op[0] in ['CPA','CPX','CPY']:
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg(self.op[0][2]),sourcenode)),
						NodeAssign(NodeLocReg('fC'),NodeGT(NodeLocReg(self.op[0][2]),sourcenode)),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg(self.op[0][2]),7))
					]
		if self.op[0] in ['EOR']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(NodeLocReg('A'),NodeEOR(NodeLocReg('A'),sourcenode)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg('A'),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg('A'),7))
					]
		if self.op[0] in ['ORA']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(NodeLocReg('A'),NodeOR(NodeLocReg('A'),sourcenode)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg('A'),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg('A'),7))
					]
		if self.op[0] in ['AND']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(NodeLocReg('A'),NodeAND(NodeLocReg('A'),sourcenode)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg('A'),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg('A'),7))
					]
		if self.op[0] in ['ADC']:
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeAssign(NodeTempVar(self.addr,80),NodeADC(NodeLocReg('A'),sourcenode,NodeLocReg('fC'))),
						NodeAssign(NodeLocReg('fV'),NodeAND(NodeEqual(NodeBit(NodeLocReg('A'),7),NodeBit(sourcenode,7)),NodeNE(NodeBit(NodeLocReg('A'),7),NodeBit(NodeTempVar(self.addr,80),7)))),
						NodeAssign(NodeLocReg('fC'),NodeGT(NodeTempVar(self.addr,80),NodeLocImmediate(0xFF))),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeTempVar(self.addr,80),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeTempVar(self.addr,80),7)),
						NodeAssign(NodeLocReg('A'),NodeTempVar(self.addr,80))
					]
		if self.op[0] in ['SBC']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(NodeLocReg('fV'),NodeAND(NodeEqual(NodeBit(NodeLocReg('A'),7),NodeBit(sourcenode,7)),NodeNE(NodeBit(NodeLocReg('A'),7),NodeBit(NodeSBC(sourcenode,NodeLocReg('A'),NodeLocReg('fC')),7)))),
						NodeAssign(NodeLocReg('A'),NodeSBC(NodeLocReg('A'),sourcenode,NodeLocReg('fC'))),
						NodeAssign(NodeLocReg('fC'),NodeCarry()),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg('A'),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg('A'),7))
					]
		if self.op[0] in ['ASL']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(sourcenode,NodeASL(sourcenode,NodeLocReg('fC'))),
						NodeAssign(NodeLocReg('fC'),NodeCarry()),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(sourcenode,NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(sourcenode,7))
					]+snw
		if self.op[0] in ['ROR']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(sourcenode,NodeROR(sourcenode,NodeLocReg('fC'))),
						NodeAssign(NodeLocReg('fC'),NodeCarry()),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(sourcenode,NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(sourcenode,7))
					]+snw
		if self.op[0] in ['LSR']:
			sourcenode,snr,snw=self.makeSourceNode()
			return snr+[
						NodeAssign(sourcenode,NodeLSR(sourcenode,NodeLocReg('fC'))),
						NodeAssign(NodeLocReg('fC'),NodeCarry()),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(sourcenode,NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(sourcenode,7)),
					]+snw
		if self.op[0] in ['PHA']:
			return [
						NodePush(NodeLocReg(self.op[0][2]))
					]
		if self.op[0] in ['PLA']:
			return [
						NodeAssign(NodeLocReg('A'),NodePull()),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg('A'),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg('A'),7))
					]
		if self.op[0]=='BPL':
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeIf(NodeEqual(NodeLocReg('fN'),NodeFlagVal(False)),NodeBranch(sourcenode))
					]
		if self.op[0]=='BNE':
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeIf(NodeEqual(NodeLocReg('fZ'),NodeFlagVal(False)),NodeBranch(sourcenode))
					]
		if self.op[0]=='BEQ':
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeIf(NodeEqual(NodeLocReg('fZ'),NodeFlagVal(True)),NodeBranch(sourcenode))
					]
		if self.op[0]=='BCS':
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeIf(NodeEqual(NodeLocReg('fC'),NodeFlagVal(True)),NodeBranch(sourcenode))
					]
		if self.op[0]=='BCC':
			sourcenode,snr,snw=self.makeSourceNode(self.addr)
			return snr+[
						NodeIf(NodeEqual(NodeLocReg('fC'),NodeFlagVal(False)),NodeBranch(sourcenode))
					]
		if self.op[0]=='JSR':
			sourcenode,snr,snw=self.makeSourceNode()
			return [
						NodeJSR(sourcenode)
					]
		if self.op[0]=='JMP':
			sourcenode,snr,snw=self.makeSourceNode()
			return [
						NodeBranch(sourcenode)
					]
		if self.op[0]=='NOP':
			return [
						NodeNop()
					]
		if self.op[0] in ['RTS']:
			return [
						NodeRTS()
					]
		if self.op[0] in ['RTI']:
			return [
						NodeRTI()
					]
		print self.op[0]
		print 5/0
	def makeSourceNode(self,addr):
		if self.op[1]==IMM:
			return NodeLocImmediate(self.bytes[1]),[],[]
		if self.op[1]==ZP:
			return NodeTempVar(addr,0),[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1]))],[NodeWrite(NodeLocAbsolute(self.bytes[1]),NodeTempVar(addr,0))]
		#if self.op[1]==ZPX:
		#	return NodeLocIndexed(NodeLocAbsolute(self.bytes[1]),NodeLocReg('X'))
		if self.op[1]==ABS:
			return NodeTempVar(addr,0),[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8)))],[NodeWrite(NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8)),NodeTempVar(addr,0))]
		if self.op[1]==ABSX:
			return NodeTempVar(addr,1),[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8))),NodeRead(NodeTempVar(addr,1),NodeLocIndexed(NodeTempVar(addr,0),NodeLocReg('X')))],[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8))),NodeWrite(NodeLocIndexed(NodeTempVar(addr,0),NodeLocReg('X')),NodeTempVar(addr,1))]
		#	return NodeLocIndexed(NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8)),NodeLocReg('X'))
		if self.op[1]==ABSY:
			return NodeTempVar(addr,1),[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8))),NodeRead(NodeTempVar(addr,1),NodeLocIndexed(NodeTempVar(addr,0),NodeLocReg('X')))],[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8))),NodeWrite(NodeLocIndexed(NodeTempVar(addr,0),NodeLocReg('Y')),NodeTempVar(addr,1))]
		#if self.op[1]==IND:
		#	return NodeLocIndirect(NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8)))
		if self.op[1]==INDX:
			return NodeTempVar(addr,2),[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1])),NodeRead(NodeTempVar(addr,1),NodeLocIndexed(NodeTempVar(addr,0),NodeLocReg('X'))),NodeRead(NodeTempVar(addr,2),NodeLocIndirect(NodeTempVar(addr,1)))],[]
			#NodeLocIndirect(NodeLocIndexed(NodeLocAbsolute(self.bytes[1]),NodeLocReg('X')))
		if self.op[1]==INDY:
			return NodeTempVar(addr,2),[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1])),NodeRead(NodeTempVar(addr,1),NodeLocIndirect(NodeTempVar(addr,0))),NodeRead(NodeTempVar(addr,2),NodeLocIndexed(NodeTempVar(addr,1),NodeLocReg('Y')))],[NodeRead(NodeTempVar(addr,0),NodeLocAbsolute(self.bytes[1])),NodeRead(NodeTempVar(addr,1),NodeLocIndirect(NodeTempVar(addr,0))),NodeWrite(NodeLocIndexed(NodeTempVar(addr,1),NodeLocReg('Y')),NodeTempVar(addr,2))]
			#NodeLocIndexed(NodeLocIndirect(NodeLocAbsolute(self.bytes[1])),NodeLocReg('Y'))
		if self.op[1]==REL:
			return NodeLocRel(self.bytes[1]),[],[]
		#if self.op[1]==ACC:
		#	return NodeLocReg("A"),[],[]
		print self.op[1]
		print 5/0
if __name__=="__main__":
	rom=ROM()
	with open('C:\\users\\Andrew.Sentman\\workspace\\AIIEmu\\tests\\pacman.nes','rb') as f:
		rom.load(f)
	addr=0xc033
	while True:
		op=Opcode()
		addr=op.load(rom,addr)
		print op.genAST()