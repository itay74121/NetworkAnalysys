from PcapReading.PcapBlock import Block
from PcapReading.readpcap import PcapReader
from Statistics.Statistics import Statistics

def f(b:Block):
    return hasattr(b.packet,'tcp')  and b.packet.ipversion == 6 and (b.packet.tcp.src_port == 443 or b.packet.tcp.dest_port == 443 )
def main():
    reader = PcapReader("ubuntu_sample.pcapng")
    s = Statistics(reader)
    fil = s.filter(f)
    stat = s.get_statistics(fil)
    for key in stat:
        print(key," :=  ",stat[key])



if __name__ == "__main__":
    main() 