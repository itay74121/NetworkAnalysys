from os import path
from .PcapReaderHelper import IDB,SHB
from .PcapBlock import Block
from colorama import Back


class PcapReader:
    def __init__(self,filename:str) -> None:
        self.filename = filename
        self.isfile =  path.isfile(self.filename)
        self.sections = {}
        self.read()
        print(len(self.sections[1][0].packetblocks))
    def read(self):
        if not self.isfile:
            print("No such file")
            return
        
        current_section = 0

        with open(self.filename,'rb') as f:
            if not f.readable():
                return
            flag = True
            while flag:
                b = Block(f)
                if b.block_type == 168627466: # section header block
                    current_section += 1
                    self.sections[current_section] = SHB(b)
                elif b.block_type == 1: # interface block
                    s = self.sections[current_section]
                    s[s.maxinterfacenum] = IDB(b)
                elif b.block_type == 6:
                    self.sections[current_section][b.interface_id].packetblocks.append(b)
                    
                elif b.block_type == 5:
                    flag = False


def main():
    PcapReader("sample.pcapng")
if __name__ == "__main__":
    main()
