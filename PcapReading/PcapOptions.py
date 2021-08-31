from struct import unpack

class Option:
    def __init__(self,data:bytes) -> None:
        self.option_type = unpack("H",data[:2])[0]
        self.option_length = unpack("H",data[2:4])[0]
        self.isend = False
        if self.option_length == 0 and self.option_type == 0:
            self.isend = True
            return
        if self.option_length%4 != 0:
            d = self.option_length // 4
            self.option_length = d*4 + 4
        self.option_value = data[4:4+self.option_length]
    def __str__(self):
        return f"option type: {self.option_type}\noption length: {self.option_length} \noption value: {str(self.option_value)}\n\n"
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
            if not o.isend:
                self.options.append(o)
    def __str__(self) -> str:
        return "".join([str(i) for i in self.options])
    def __repr__(self) -> str:
        return self.__str__()
    