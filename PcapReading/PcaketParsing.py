import socket
from struct import unpack


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
            self.ttl = int(data[22])
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