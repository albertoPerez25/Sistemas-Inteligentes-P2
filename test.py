from functools import lru_cache

def AEstrella(i):
        print("1.DENTRO DENTRO a AESTRELLA")
        return i+1

def aestrellaCache(i):
        @lru_cache(maxsize=128000)
        def Cache(i):
            print("2.DENTRO a AESTRELLA")
            return AEstrella(i)
        return Cache(i)

for i in range(10):
    print(aestrellaCache(1))
