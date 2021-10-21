import sys 

def get_bits(n):
    s = ''
    while(n>0):
        s += '1' if (n&1) else '0'
        n = n>>1
    return s[::-1]

def isbigendian():
    n = 8
    print(get_bits(n))
    if (n >> 1) < n:
        return True
    else: 
        return False



def main():
    print(isbigendian())
    print(sys.byteorder)

if __name__ == "__main__":
    main()
