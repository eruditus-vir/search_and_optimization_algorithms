import math
import time


class TausWorth:

    def __init__(self,tausi1=None, tausi2=None):
        "initialize the tausworth random number generator"

        if tausi1 is not None and tausi2 is not None:
            self.tausi1 = tausi1
            self.tausi2 = tausi2
        else:

            frac, integer = math.modf(time.time())
            self.tausi1 = int(integer)
            self.tausi2 = int(frac*1000)

        self.invvalue = 1.0/2147483647.0

        print("\nTausWorth RNG initialized with %d %d" % (self.tausi1,self.tausi2))

    def get(self):
        "return a pseudo random number 0 < x < 1"

        self.tausi1 =  ( ( self.tausi1 << 12 )^( ( ((self.tausi1 << 13)^self.tausi1 ) & 2147483647 ) >> 19 ) ) & 2147483647
        self.tausi2 =  ( ( self.tausi2 << 17 )^( ( ((self.tausi2 <<  2)^self.tausi2 ) &  536870911 ) >> 12 ) ) &  536870911

        return( ((self.tausi2 << 2)^self.tausi1)*self.invvalue)


rng = TausWorth(123456, 456789)

for i in range(10):
    print(rng.get())

rng2 = TausWorth()

for i in range(10):
    print(rng2.get())

"""
reference results:

tausi1 = 123456;
tausi2 = 456789;

0.7230225567
0.6168235962
0.0644189902
0.6051129599
0.7633173888
0.2233510363
0.1674663742
0.9320537946
0.8163341739
0.5693673690
"""
