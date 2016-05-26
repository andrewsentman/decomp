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

SBI=20
IEM=21
RMW=22
BRN=23
BRK=24
PSH=25
PLL=26
RTI=27
RTS=28
JMP=29
JSR=30
STO=31

ops={
0x69:["ADC",IMM ,2,2,"CZidbVN",IEM],
0x65:["ADC",ZP  ,2,3,"CZidbVN",IEM],
0x75:["ADC",ZPX ,2,4,"CZidbVN",IEM],
0x6d:["ADC",ABS ,3,4,"CZidbVN",IEM],
0x7d:["ADC",ABSX,3,4,"CZidbVN",IEM],
0x79:["ADC",ABSY,3,4,"CZidbVN",IEM],
0x61:["ADC",INDX,2,6,"CZidbVN",IEM],
0x71:["ADC",INDY,2,5,"CZidbVN",IEM],

0x29:["AND",IMM ,2,2,"cZidbvN",IEM],
0x25:["AND",ZP  ,2,3,"cZidbvN",IEM],
0x35:["AND",ZPX ,2,4,"cZidbvN",IEM],
0x2d:["AND",ABS ,3,4,"cZidbvN",IEM],
0x3d:["AND",ABSX,3,4,"cZidbvN",IEM],
0x39:["AND",ABSY,3,4,"cZidbvN",IEM],
0x21:["AND",INDX,2,6,"cZidbvN",IEM],
0x31:["AND",INDY,2,5,"cZidbvN",IEM],

0x0a:["ASL",ACC ,1,2,"CZidbvN",SBI],
0x06:["ASL",ZP  ,2,5,"CZidbvN",RMW],
0x16:["ASL",ZPX ,2,6,"CZidbvN",RMW],
0x0e:["ASL",ABS ,3,6,"CZidbvN",RMW],
0x1e:["ASL",ABSX,3,7,"CZidbvN",RMW],

0x90:["BCC",REL ,2,2/3,"czidbvn",BRN],
0xB0:["BCS",REL ,2,2/3,"czidbvn",BRN],
0xF0:["BEQ",REL ,2,2/3,"czidbvn",BRN],
0x30:["BMI",REL ,2,2/3,"czidbvn",BRN],
0xD0:["BNE",REL ,2,2/3,"czidbvn",BRN],
0x10:["BPL",REL ,2,2/3,"czidbvn",BRN],
0x50:["BVC",REL ,2,2/3,"czidbvn",BRN],
0x70:["BVS",REL ,2,2/3,"czidbvn",BRN],

0x24:["BIT",ZP  ,2,3,"cZidbVN",IEM],
0x2c:["BIT",ABS ,3,4,"cZidbVN",IEM],

0x00:["BRK",IMP ,1,7,"czidbvn",BRK],
0x18:["CLC",IMP ,1,2,"Czidbvn",SBI],
0xd8:["CLD",IMP ,1,2,"cziDbvn",SBI],
0x58:["CLI",IMP ,1,2,"czIdbvn",SBI],
0xb8:["CLV",IMP ,1,2,"czidbVn",SBI],
0xea:["NOP",IMP ,1,2,"czidbvn",SBI],
0x48:["PHA",IMP ,1,3,"czidbvn",PSH],
0x68:["PLA",IMP ,1,4,"cZidbvN",PLL],
0x08:["PHP",IMP ,1,3,"czidbvn",PSH],
0x28:["PLP",IMP ,1,4,"CZIDBVN",PLL],
0x40:["RTI",IMP ,1,6,"czidbvn",RTI],
0x60:["RTS",IMP ,1,6,"czidbvn",RTS],
0x38:["SEC",IMP ,1,2,"Czidbvn",SBI],
0xf8:["SED",IMP ,1,2,"cziDbvn",SBI],
0x78:["SEI",IMP ,1,2,"czIdbvn",SBI],
0xaa:["TAX",IMP ,1,2,"cZidbvN",SBI],
0x8a:["TXA",IMP ,1,2,"cZidbvN",SBI],
0xa8:["TAY",IMP ,1,2,"cZidbvN",SBI],
0x98:["TYA",IMP ,1,2,"cZidbvN",SBI],
0xba:["TSX",IMP ,1,2,"cZidbvN",SBI],
0x9a:["TXS",IMP ,1,2,"czidbvn",SBI],

0xc9:["CPA",IMM ,2,2,"CZidbvN",IEM],
0xc5:["CPA",ZP  ,2,3,"CZidbvN",IEM],
0xd5:["CPA",ZPX ,2,4,"CZidbvN",IEM],
0xcd:["CPA",ABS ,3,4,"CZidbvN",IEM],
0xdd:["CPA",ABSX,3,4,"CZidbvN",IEM],
0xd9:["CPA",ABSY,3,4,"CZidbvN",IEM],
0xc1:["CPA",INDX,2,6,"CZidbvN",IEM],
0xd1:["CPA",INDY,2,5,"CZidbvN",IEM],

0xe0:["CPX",IMM ,2,2,"CZidbvN",IEM],
0xe4:["CPX",ZP  ,2,3,"CZidbvN",IEM],
0xec:["CPX",ABS ,3,4,"CZidbvN",IEM],

0xc0:["CPY",IMM ,2,2,"CZidbvN",IEM],
0xc4:["CPY",ZP  ,2,3,"CZidbvN",IEM],
0xcc:["CPY",ABS ,3,4,"CZidbvN",IEM],

0xc6:["DEC",ZP  ,2,5,"cZidbvN",RMW],
0xd6:["DEC",ZPX ,2,6,"cZidbvN",RMW],
0xce:["DEC",ABS ,3,6,"cZidbvN",RMW],
0xde:["DEC",ABSX,3,7,"cZidbvN",RMW],

0xca:["DEX",IMP ,1,2,"cZidbvN",SBI],
0x88:["DEY",IMP ,1,2,"cZidbvN",SBI],

0xe8:["INX",IMP ,1,2,"cZidbvN",SBI],
0xc8:["INY",IMP ,1,2,"cZidbvN",SBI],

0x49:["EOR",IMM ,2,2,"cZidbvN",IEM],
0x45:["EOR",ZP  ,2,3,"cZidbvN",IEM],
0x55:["EOR",ZPX ,2,4,"cZidbvN",IEM],
0x4d:["EOR",ABS ,3,4,"cZidbvN",IEM],
0x5d:["EOR",ABSX,3,4,"cZidbvN",IEM],
0x59:["EOR",ABSY,3,4,"cZidbvN",IEM],
0x41:["EOR",INDX,2,6,"cZidbvN",IEM],
0x51:["EOR",INDY,2,5,"cZidbvN",IEM],

0xe6:["INC",ZP  ,2,5,"cZidbvN",RMW],
0xf6:["INC",ZPX ,2,6,"cZidbvN",RMW],
0xee:["INC",ABS ,3,6,"cZidbvN",RMW],
0xfe:["INC",ABSX,3,7,"cZidbvN",RMW],

0x4c:["JMP",ABS ,3,3,"czidbvn",JMP],
0x6c:["JMP",IND ,3,5,"czidbvn",JMP],
0x20:["JSR",ABS ,3,6,"czidbvn",JSR],

0xa9:["LDA",IMM ,2,2,"cZidbvN",IEM],
0xa5:["LDA",ZP  ,2,3,"cZidbvN",IEM],
0xb5:["LDA",ZPX ,2,4,"cZidbvN",IEM],
0xad:["LDA",ABS ,3,4,"cZidbvN",IEM],
0xbd:["LDA",ABSX,3,4,"cZidbvN",IEM],
0xb9:["LDA",ABSY,3,4,"cZidbvN",IEM],
0xa1:["LDA",INDX,2,6,"cZidbvN",IEM],
0xb1:["LDA",INDY,2,5,"cZidbvN",IEM],

0xa2:["LDX",IMM ,2,2,"cZidbvN",IEM],
0xa6:["LDX",ZP  ,2,3,"cZidbvN",IEM],
0xb6:["LDX",ZPY ,2,4,"cZidbvN",IEM],
0xae:["LDX",ABS ,3,4,"cZidbvN",IEM],
0xbe:["LDX",ABSY,3,4,"cZidbvN",IEM],

0xa0:["LDY",IMM ,2,2,"cZidbvN",IEM],
0xa4:["LDY",ZP  ,2,3,"cZidbvN",IEM],
0xb4:["LDY",ZPX ,2,4,"cZidbvN",IEM],
0xac:["LDY",ABS ,3,4,"cZidbvN",IEM],
0xbc:["LDY",ABSX,3,4,"cZidbvN",IEM],

0x4a:["LSR",ACC ,1,2,"CZidbvN",SBI],
0x46:["LSR",ZP  ,2,5,"CZidbvN",RMW],
0x56:["LSR",ZPX ,2,6,"CZidbvN",RMW],
0x4e:["LSR",ABS ,3,6,"CZidbvN",RMW],
0x5e:["LSR",ABSX,3,7,"CZidbvN",RMW],

0x09:["ORA",IMM ,2,2,"cZidbvN",IEM],
0x05:["ORA",ZP  ,2,3,"cZidbvN",IEM],
0x15:["ORA",ZPX ,2,4,"cZidbvN",IEM],
0x0d:["ORA",ABS ,3,4,"cZidbvN",IEM],
0x1d:["ORA",ABSX,3,4,"cZidbvN",IEM],
0x19:["ORA",ABSY,3,4,"cZidbvN",IEM],
0x01:["ORA",INDX,2,6,"cZidbvN",IEM],
0x11:["ORA",INDY,2,5,"cZidbvN",IEM],

0x2a:["ROL",ACC ,1,2,"CZidbvN",SBI],
0x26:["ROL",ZP  ,2,5,"CZidbvN",RMW],
0x36:["ROL",ZPX ,2,6,"CZidbvN",RMW],
0x2e:["ROL",ABS ,3,6,"CZidbvN",RMW],
0x3e:["ROL",ABSX,3,7,"CZidbvN",RMW],

0x6a:["ROR",ACC ,1,2,"CZidbvN",SBI],
0x66:["ROR",ZP  ,2,5,"CZidbvN",RMW],
0x76:["ROR",ZPX ,2,6,"CZidbvN",RMW],
0x7e:["ROR",ABS ,3,6,"CZidbvN",RMW],
0x6e:["ROR",ABSX,3,7,"CZidbvN",RMW],

0xe9:["SBC",IMM ,2,2,"CZidbVN",IEM],
0xe5:["SBC",ZP  ,2,3,"CZidbVN",IEM],
0xf5:["SBC",ZPX ,2,4,"CZidbVN",IEM],
0xed:["SBC",ABS ,3,4,"CZidbVN",IEM],
0xfd:["SBC",ABSX,3,4,"CZidbVN",IEM],
0xf9:["SBC",ABSY,3,4,"CZidbVN",IEM],
0xe1:["SBC",INDX,2,6,"CZidbVN",IEM],
0xf1:["SBC",INDY,2,5,"CZidbVN",IEM],

0x85:["STA",ZP  ,2,3,"czidbvn",STO],
0x95:["STA",ZPX ,2,4,"czidbvn",STO],
0x8d:["STA",ABS ,3,4,"czidbvn",STO],
0x9d:["STA",ABSX,3,5,"czidbvn",STO],
0x99:["STA",ABSY,3,5,"czidbvn",STO],
0x81:["STA",INDX,2,6,"czidbvn",STO],
0x91:["STA",INDY,2,6,"czidbvn",STO],

0x86:["STX",ZP  ,2,3,"czidbvn",STO],
0x96:["STX",ZPY ,2,4,"czidbvn",STO],
0x8e:["STX",ABS ,3,4,"czidbvn",STO],

0x84:["STY",ZP  ,2,3,"czidbvn",STO],
0x94:["STY",ZPX ,2,4,"czidbvn",STO],
0x8c:["STY",ABS ,3,4,"czidbvn",STO]
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
		ast=[]
		if self.op[5]==SBI:
			if self.op[0]=='ASL':
				return [NodeAssign(NodeTempVar(self.addr,80),NodeROL(NodeLocReg('A'),NodeFlagVal(False))),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeTempVar(self.addr,80),7)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeTempVar(self.addr,80),NodeLocImmediate(0))),
						NodeAssign(NodeLocReg('fC'),NodeBit(NodeLocReg('A'),7)),
						NodeAssign(NodeLocReg('A'),NodeTempVar(self.addr,80))]
			if self.op[0] in ['TAX','TXA','TAY','TYA']:
				return [NodeAssign(NodeLocReg(self.op[0][2]),NodeLocReg(self.op[0][1])),
						NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg(self.op[0][2]),7)),
						NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg(self.op[0][2]),NodeLocImmediate(0)))]
		if self.op[5]==IEM:
			if self.op[1]==IMM:
				inloc=NodeLocImmediate(self.bytes[1])
			if self.op[0]=='AND':
				ast.append(NodeAssign(NodeLocReg('A'),NodeAND(NodeLocReg('A'),inloc)))
				ast.append(NodeAssign(NodeLocReg('fS'),NodeBit(NodeLocReg('A'),7)))
				ast.append(NodeAssign(NodeLocReg('fZ'),NodeEqual(NodeLocReg('A'),NodeLocImmediate(0))))
				return ast
			if self.op[0] in ['LDA','LDX','LDY']:
				ast.append(NodeAssign(NodeLocReg(self.op[0][2]),inloc))
				return ast
		if self.op[5]==STO:
			if self.op[1]==ZP:
				return [NodeWrite(NodeLocAbsolute(self.bytes[1]),NodeLocReg(self.op[0][2]))]
		if self.op[5]==JSR:
			return [NodeBranch(NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8)))]
		if self.op[5]==JMP:
			if self.op[1]==ABS:
				return [NodeBranch(NodeLocAbsolute(self.bytes[1]+(self.bytes[2]<<8)))]
		if self.op[5]==RTS:
			return [NodeRTS()]
		print self.op[0]
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
