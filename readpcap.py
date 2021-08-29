from io import TextIOWrapper
from os import read
from struct import unpack
from colorama import Back
import socket
from datetime import date
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
            o = Options(data[:len(data)-4])
            print(o)
        elif self.block_type == 1: # interface header
            data = f.read(self.block_length-8)
            options = Options(data[8:len(data)-4])
            print(options)
        elif self.block_type == 6: # enhanced packet header
            self.interface_id = unpack("I",f.read(4))[0]
            self.timestamp = unpack("Q",f.read(8))[0]
            self.captured_packet_length = unpack("I",f.read(4))[0]
            self.original_packet_length =  unpack("I",f.read(4))[0]
            data = f.read(self.block_length - 28)
            p = Packet(data)
            o = Options(data[self.captured_packet_length:len(data)-4])
            print(o)
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
class Packet:
    def __init__(self,data:bytes) -> None:
        # eth header 
        self.data = data 
        t = unpack("6B",self.data[:6])
        self.dest_mac_addr = "".join([str(hex(i))[2:]+":" for i in t])
        t = unpack("6B",self.data[6:12])
        self.src_mac_addr = "".join([str(hex(i))[2:]+":" for i in t])
        #print(self.dest_mac_addr,self.src_mac_addr)
        self.type = unpack("H",self.data[12:14])[0]
        if self.type == 8: # ipv4
            # read ip header
            # all is ipv4 even though it doesn't have to be 
            self.length_ip_header = int(data[14]) & 15
            self.protocol = int(data[23])
            start = 14 + self.length_ip_header*4 
            if self.protocol  == 6:#tcp
                #print("tcp")
                self.src_port, self.dest_port,self.sequence, self.ack, self.vals, self.window, self.checksum, self.up = unpack("HHIIHHHH",data[start:start+20])
                self.src_port = socket.ntohs(self.src_port)
                self.dest_port = socket.ntohs(self.dest_port)
                self.window = socket.ntohs(self.window)
                self.checksum = socket.ntohs(self.checksum)
                #print(self.src_port,self.dest_port,self.sequence,self.ack,self.window,self.checksum,self.up)
            elif self.protocol == 17:#udp
                self.src_port, self.dest_port = unpack("HH",data[start:start+4])
                self.src_port = socket.ntohs(self.src_port)
                self.dest_port = socket.ntohs(self.dest_port)
        elif self.type == 0x86dd: # ipv6
            pass

class Option:
    def __init__(self,data:bytes) -> None:
        self.option_type = unpack("H",data[:2])[0]
        self.option_length = unpack("H",data[2:4])[0]
        self.option_value = str(data[4:4+self.option_length])
    def __str__(self):
        return f"option type: {self.option_type}\noption length: {self.option_length} \noption value: {self.option_value}\n\n"
    def __repr__(self) -> str:
        return self.__str__()
class Options:
    def __init__(self,data:bytes) -> None:
        self.options = []
        datalen = len(data)
        offset = 0
        if datalen < 4:
            return
        while datalen > offset:
            o = Option(data[offset:])
            offset += 4 + o.option_length
            self.options.append(o)
    def __str__(self) -> str:
        return "".join([str(i) for i in self.options])
    def __repr__(self) -> str:
        return self.__str__()
    




with open("sample.pcapng",'rb') as f:
    print(Back.RED + f"block {0}\n" + Back.BLACK)
    b = Block(f)
    print(b)
    flag = True
    c  = 1
    while flag and c < 20:
        print(Back.RED + f"block {c}\n" + Back.BLACK)
        b = Block(f)
        if b.block_type == 6:
            print(b.captured_packet_length,b.timestamp)
        if b.block_type == 5:
            flag = False
        c += 1
        #print(b)
