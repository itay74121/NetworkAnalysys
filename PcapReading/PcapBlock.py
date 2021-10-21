from io import TextIOWrapper
from struct import unpack
from .PcapOptions import Options,Option
from .PcaketParsing import Packet



class Block:
    def __init__(self,f:TextIOWrapper) -> None:
        data = f.read(8)
        t = unpack("II",data)
        self.block_type = t[0]
        self.block_length = t[1]
        if self.block_type == 0xa0d0d0a: # section header
            data = f.read(16)
            t = unpack("IHHq",data)
            self.byte_order_magic = t[0]
            self.major_ver = t[1]
            self.minor_ver = t[2]
            self.section_length = t[3]
            data = f.read(self.block_length-24)
            self.options = Options(data[:len(data)-4])
            #print(o)
        elif self.block_type == 1: # interface header
            data = f.read(self.block_length-8)
            self.options = Options(data[8:len(data)-4])
            if self.options.look_for_option(2)[0].any:
                self.any = True
            self.time_format = self.options.look_for_option(9)[0].option_value[0]
            # for opt in self.options.options:
            #     opt:Option
            #     if opt.option_type == 9: # timestamp resolution
            #         #val  = struct.unpack("bbbb",opt.option_value)[0]
            #         self.timeformat = opt.option_value[0]    
        elif self.block_type == 6: # enhanced packet header
            self.interface_id = unpack("I",f.read(4))[0]
            d = f.read(8)
            i1,i2 = unpack("II",d)
            self.timestamp = (i1 << 32) | i2
            self.captured_packet_length = unpack("I",f.read(4))[0]
            self.original_packet_length =  unpack("I",f.read(4))[0]
            self.data = f.read(self.block_length - 28)
            #self.packet = Packet(self.data)
            self.options = Options(self.data[self.captured_packet_length:len(self.data)-4])
        else:
            f.read(self.block_length-8)

    def __repr__(self) -> str:
        return self.__str__()
    def __str__(self):
        s = f"type: {self.block_type} in hex {hex(self.block_type)}\n"
        s += f"length: {self.block_length}\n"
        # s += f"order: {self.byte_order_magic} in hex {hex(self.byte_order_magic)}\n"
        # s += f"major: {self.major_ver}\n"
        # s += f"minor: {self.minor_ver}\n"
        # s += f"section length: {self.section_length}"
        return s
    def reread_packet(self,flag):
        self.packet = Packet(self.data,any=flag)