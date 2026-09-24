# Goal is to build my own pow() function, more specifically one that computes a ^ b mod % p efficiently

import time as t


def LargestTwo(n):
    x = 1
    c = 0
    while n >= x:
        x = x << 1
        c = c + 1    
    return x >> 1, c - 1

def To_Binary(n):
    if n == 0:
        return ['0']
    x, L = LargestTwo(n)
    n = n - x
    res = ['1'] + (L*['0'])
    #print(res)
    while n != 0:
        x, c = LargestTwo(n)
        n = n - x
        res[L - c] = '1'
    return res
    
def powerMod(a, b, p):
    binary = To_Binary(b)[::-1]
    if a == 0:
        return 0
    res = 1
    for i in binary:
        if i == '1':
            res = (res * a) % p
        a = (a * a) % p
    return res

a, b, p = 16647851478 + (10**80), 7**71, 11 ** 79

if __name__ == "__main__":
    start = t.time()
    print(powerMod(a, b, p))
    done = t.time()
    print("Made:", done - start)

    start = t.time()    
    print(pow(a, b, p))
    done = t.time()
    print("pow:", done - start)


