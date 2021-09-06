
from typing import Callable

def avg(l):
    return sum(l)/len(l)
def std(l):
    a = avg(l)
    return (sum([(i - a)**2 for i in l])/len(l)) **-2

class DICT(dict):
    def __init__(self,**kwargs):
        self.dic = kwargs
        super().__init__(self.dic)
    def __add__(self,other):
        new  = {}
        for key in self.dic:
            new[key] = self.dic[key]
        for key in other:
            new[key] = other[key]
        return new
    

class Statistics:
    def __init__(self,reader) -> None:
        self.reader =  reader
    def filter (self,func:Callable) -> list:
        packetsblocks = []
        for section in self.reader.sections:
            shb = self.reader.sections[section]
            for interfacenum in shb.interfaces:
                idb = shb.interfaces[interfacenum]
                for b in idb.packetblocks:
                    if func(b):
                        packetsblocks.append(b)
        return packetsblocks
    def extract_times(self,packetblocks):
        times = []
        for b in packetblocks:
            if b.block_type == 6:
                times.append(b.timestamp)
        return times
    def get_times_statistics(self,times):
        l  = []
        for i in range(len(times)-1):
            time1 = times[i] 
            time2 = times[i+1]
            delta = abs(time2 - time1)
            l.append(delta)
        packets_persecond = []
        start = times[0]
        count = 0
        for time in times:
            if time - start > 10**6:
                packets_persecond.append(count)
                count = 1
                start = time
            else:
                count += 1
        return DICT(min_time = min(l) * 10**-6,max_time = max(l)* 10**-6,avg_time = avg(l)* 10**-6,
        std_time = std(l)* 10**-6,avg_packets = avg(packets_persecond),std_packets = std(packets_persecond)**2)

    def get_packet_statistics(self,packetblocks):
        ttls = []
        sizes = []
        total_packets = len(packetblocks)
        for block in packetblocks:
            if block.packet.type == 8:
                ttls.append(block.packet.ttl)
                sizes.append(block.captured_packet_length)
        total_bytes = sum(sizes)
        avg_size = avg(sizes)
        var_sizes = std(sizes)**2
        avg_ttl = avg(ttls)
        min_ttl = min(ttls)
        max_ttl = max(ttls)
        min_size = min(sizes)
        max_size = max(sizes)
        return DICT(total_packets =total_packets , total_bytes=total_bytes, avg_size=avg_size,
        var_sizes=var_sizes, avg_ttl=avg_ttl,min_ttl=min_ttl,max_ttl=max_ttl,min_size=min_size,max_size=max_size)

    def get_statistics(self,packetblocks):
        times = self.extract_times(packetblocks)
        return self.get_times_statistics(times) + self.get_packet_statistics(packetblocks)

# def main():
#     reader = PcapReader("ubuntu_sample.pcapng")
#     statistics = Statistics(reader)
#     def f(x:Block):
#         return True #x.block_type == 6 #and x.packet.type == 8 and x.packet.protocol == 17
#     filtered = statistics.filter(f)
#     # d = {}
#     # for b in filtered:
#     #     f = b.packet.dest_mac_addr
#     #     if f in d:
#     #         d[f] += 1
#     #     else:
#     #         d[f] = 1
#     #     f = b.packet.src_mac_addr
#     #     if f in d:
#     #         d[f] += 1
#     #     else:
#     #         d[f] = 1
#     # times = statistics.extract_times(filtered)
#     # print(times[:5])
#     # for i in d:
#     #     print(i,d[i])
#     print(statistics.get_statistics(filtered))

# if __name__ == "__main__":
#     main()