class ROM():
	def __init__(self):
		self.banks=[]
	def load(self,f):
		f.seek(4)
		self.prgpages=ord(f.read(1))
		self.chrpages=ord(f.read(1))
		self.flags6=ord(f.read(1))
		self.flags7=ord(f.read(1))
		self.flags8=ord(f.read(1))
		self.flags9=ord(f.read(1))
		self.flagsA=ord(f.read(1))
		self.flagsB=ord(f.read(1))
		self.flagsC=ord(f.read(1))
		self.flagsD=ord(f.read(1))
		self.flagsE=ord(f.read(1))
		self.flagsF=ord(f.read(1))
		self.mapper=((self.flags6&0xF0)>>4)|(self.flags7&0xF0)
		print self.mapper
		f.seek(16)
		if (self.flags6&0x04)!=0:
			f.seek(16+512)
		self.prgbanks=[]
		print self.prgpages
		for i in xrange(self.prgpages):
			self.prgbanks.append([ord(j) for j in f.read(16384)])
				
	def read(self,addr):
		if self.mapper==0:
			if addr<0x8000:
				assert(False)
			if addr<0xC000:
				return self.prgbanks[0][addr-0x8000]
			if addr<0x10000:
				if self.prgpages==1:
					return self.prgbanks[0][addr-0xC000]
				else:
					return self.prgbanks[1][addr-0xC000]
	def read16(self,addr):
		return self.read(addr)|(self.read(addr+1)<<8)
if __name__=="__main__":
	rom=ROM()
	with open('C:\\users\\Andrew.Sentman\\workspace\\AIIEmu\\tests\\pacman.nes','rb') as f:
		rom.load(f)
	print [[hex(j) for j in i[:4]] for i in rom.prgbanks]