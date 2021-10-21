import socket
from struct import unpack
from sys import byteorder

ARROW = '>' if byteorder == 'little' else '<'

class TCPHEADER:
    def __init__(self,data) -> None:
        self.data = data
        self.src_port, self.dest_port,self.sequence, self.ack, self.vals, self.window, self.checksum, self.up = unpack("HHIIHHHH",self.data[0:20])
        self.src_port = socket.ntohs(self.src_port)
        self.dest_port = socket.ntohs(self.dest_port)
        self.window = socket.ntohs(self.window)
        self.checksum = socket.ntohs(self.checksum)
        self.data_offset = self.vals & 15


class UDPHEADER:
    def __init__(self,data) -> None:
        self.data = data
        self.src_port, self.dest_port = unpack("HH",self.data[:4])
        self.src_port = socket.ntohs(self.src_port)
        self.dest_port = socket.ntohs(self.dest_port)

class Packet:
    def __init__(self,data:bytes,any=False) -> None:
        self.any = any 
        self.data = data 
        # eth header 
        if not any:
            t = unpack("6B",self.data[:6])
            self.dest_mac_addr = "".join([str(hex(i))[2:]+":" for i in t])
            t = unpack("6B",self.data[6:12])
            self.src_mac_addr = "".join([str(hex(i))[2:]+":" for i in t])
            #print(self.dest_mac_addr,self.src_mac_addr)
            self.type = unpack("H",self.data[12:14])[0]
            self.start = 14
        else:
            self.packet_type, self.hdr_type,self.link_addrlen = unpack("3H",self.data[:6])
            arr = [hex(i) for i in self.data]
            self.packet_type = socket.ntohs(self.packet_type)
            self.hdr_type = socket.ntohs(self.hdr_type)
            self.link_addrlen = socket.ntohs(self.link_addrlen)
            self.start = 16
            '''Need to read the address according to the length'''
            self.link_addr = "".join([hex(i)[2:]+":" for i in unpack(f"{self.link_addrlen}B",self.data[6:6+self.link_addrlen])])
            self.type = unpack(f"{ARROW}H",self.data[14:16])[0]
            
        if self.type == 2048: # ipv4
            # read ip header
            # all is ipv4 even though it doesn't have to be 
            self.ipversion = 4
            self.length_ip_header = int(self.data[self.start]) & 15
            self.protocol = int(self.data[self.start+9])
            self.ttl = int(self.data[self.start + 8])
            start = self.start + self.length_ip_header*4 
            if self.protocol  == 6:#tcp
                self.tcp = TCPHEADER(self.data[start:])
            elif self.protocol == 17:#udp
                self.udp = UDPHEADER(self.data[start:])

        elif self.type == 0x86dd: # ipv6
            self.ipversion = 6
            temp = unpack(f"{ARROW}I",self.data[self.start:self.start+4])[0]
            s = hex(temp)
            self.version = (temp & 0xF0000000) >> 28
            self.traffic_class = (temp & 0xFF00000) >> 20 
            self.flow_label = temp & 0xFFFFF
            self.payload_length, self.protocol, self.ttl = unpack(f"{ARROW}HBB",self.data[self.start+4:self.start+8])
            start = self.start + 40
            if self.protocol  == 6:#tcp
                self.tcp = TCPHEADER(self.data[start:])
            elif self.protocol == 17:#udp
                self.udp = UDPHEADER(self.data[start:])
        elif self.type == 0x608:
            pass 