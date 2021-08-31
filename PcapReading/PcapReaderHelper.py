


class SHB:
    def __init__(self,block) -> None:
        self.interfaces = {}
        self.maxinterfacenum = 0
        self.block = block # section header block
    def __getitem__(self,key):
        return self.interfaces[key]
    def __setitem__(self,key,value):
        self.maxinterfacenum += 1
        self.interfaces[key] = value
class IDB:
    def __init__(self,block) -> None:
        self.packetblocks = []
        self.block = block # interface description block 
