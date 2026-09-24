# Goal is to build various primality tests, and compare speeds, here i define speed by timing how long it takes a given algorithm to run on N primes
# and then take an average to obtain running time per prime. Another way to test would be to test on N composites (or just random integer) which i think
#  would also be 'good' definitions however i believe generally for most tests inputting a prime is 'the worst case' and takes a longer running time than
# a composite (or random integer).

import random as rd
import math as m
import time as t
import matplotlib.pyplot as plt
import sympy as sympy
import numpy as ny

first22Primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79]
def fermatTest(n, tests): 
    for i in first22Primes: # check divisability by 'small' primes to try catch easy cases
        if n % i == 0:
            return False
    for i in range(0, tests):
        a = rd.randint(2, n-1)
        while n % a == 0:
            a = rd.randint(2, n-1)
        if pow(a, n-1, n) != 1: # checks if fermat's little thereom holds 
            return(False)
    return(True)


def factorialMod(n, r):
    x = 1
    for i in range(0, n-1):
        x = (x * (n - i)) % r
        if x == 0:
            return 0
    return x

def Wilson(p):
    if factorialMod(p-1, p) == p-1:
        return True
    else:
        print(p)
        return False

def Test_wilson(d, n=50):      #test to find speeds of wilsons test, d = digits
    NUMBERS = n
    primes = []
    for i in range(NUMBERS):
        primes.append(sympy.nextprime(rd.randint(10**(d-1),10**d)))
    START_TIME = t.time()
    for p in primes:
        Wilson(p)
    END_TIME = t.time()
    avg = (END_TIME-START_TIME)/NUMBERS
    return avg

def Exp_fit(x, y):
    y_log = [ny.log(i) for i in y]
    b, c = ny.polyfit(x, y_log, 1)
    a = ny.exp(c)
    return a, b

def Div(p):
    if p < 2 or p % 2 == 0:
        return False
    for i in range(3, int(m.sqrt(p))+1, 2):
        if p % i == 0:
            return False
    return True

def Test_div(d, n=50):
    NUMBERS = n
    primes = []
    for i in range(NUMBERS):
        primes.append(sympy.nextprime(rd.randint(10**(d-1),10**d)))
    START_TIME = t.time()
    for p in primes:
        Div(p)      
    END_TIME = t.time()
    avg = (END_TIME-START_TIME)/NUMBERS
    return avg

def Test_fermat(d, n=50, ts = 100):
    NUMBERS = n
    primes = []
    for i in range(NUMBERS):
        primes.append(sympy.nextprime(rd.randint(10**(d-1),10**d)))
    START_TIME = t.time()
    for p in primes:
        fermatTest(p, ts)      
    END_TIME = t.time()
    avg = (END_TIME-START_TIME)/NUMBERS
    return avg

def Is_power(p, b): # p = a^b, ispower(10, 2) 
    x = 2 << int(ny.ceil(p.bit_length() / b))
    while True:
        y = int(((b - 1) * x + int(p / pow(x, b - 1))) / b)
        if y >= x:
            return x
        x = y

def perfectPower(p):
    for b in range(2, int(ny.log2(float(p)))+1):
        if pow(Is_power(p, b), b) == p: 
            return True
    return False

def orderOfp(p):
    r = 2 # start of working in mod 2 
    c = pow(m.log2(p), 2)
    while True:
        while m.gcd(p, r) != 1: # dont encounter infinite loops 
            r = r + 1
        x = p % r # x = p mod r, think x = p
        count = 1
        while x != 1 and count <= c: # if count > c, we know ord(n) > c
            x = (x * p) % r # computes the powers of p
            count = count + 1
        if x == 1 and count <= c:
            r = r + 1 # discard as ord(p) < c
        else:
            return r 



def divisibilityCheck(p, r):
    for i in range(2, min(p-1, r) + 1 ):
        if p % i == 0:
            return 0 
    return 1

def polyCheck(p, r, a):
    for i in range(0, r):
        init = (p - i) % r 
        coef = 0
        con = pow(a, init, p)
        while init  <= p:
            coef = (coef + (m.comb(p, init) * con )) % p
            init = init + r
            con = con * pow(a, r, p)
        if i % r == 0:
            if coef != a % p:
                return False
        elif i % r == p % r:
            if coef != 1:
                return False
        else:
            if coef != 0:
                return False
    return True

def polyCheckRunner(p, r):
    for j in range(1, int(m.sqrt(sympy.functions.combinatorial.numbers.totient(r)*m.log2(p))+1)):
        if not polyCheck(p, r, j):
            return False
    return True

def AKS(p):
    if perfectPower(p) == True:
        return False
    r = orderOfp(p)
    if divisibilityCheck(p, r) == 0:
        return False
    if p <= r:
        return True
    return polyCheckRunner(p, r)

    
def Test_AKS(d, n=50):
    NUMBERS = n
    primes = []
    for i in range(NUMBERS):
        primes.append(sympy.nextprime(rd.randint(10**(d-1),10**d)))
    START_TIME = t.time()
    for p in primes:
        AKS(p)
    END_TIME = t.time()
    avg = (END_TIME-START_TIME)/NUMBERS
    return avg      

def millerRabin(p, tests = 100):
    if p % 2 == 0: # for p = 2 or 3, b is poorly defined
        if p != 2:
            return False
        else:
            return True
    if p == 3:
        return True
    n = p - 1
    a = 0
    while n % 2 == 0:
        a = a + 1
        n = n // 2 # remove powers of 2, p - 1 = n * 2^k
    for i in range(tests):
        b = rd.randint(2, p - 2)
        z = pow(b, n, p) # z = b ^ n mod p
        if (z == 1) or (z == p - 1):
            continue # as this will always result in z ^ (2^k) = 1
        for j in range(1, a):
            z = pow(z, 2, p)
            if z == p - 1:
                break
            if z == 1:
                return False
        else:
            return False
    return True


def Test_MillerRabin(d, n = 50, ts = 100):
    NUMBERS = n
    primes = []
    for i in range(NUMBERS):
        primes.append(sympy.nextprime(rd.randint(10**(d-1),10**d)))
    START_TIME = t.time()
    for p in primes:
        millerRabin(p, ts)
    END_TIME = t.time()
    avg = (END_TIME-START_TIME)/NUMBERS
    return avg     



def Plot_Test(tests=50, wilson = True, div = True, fermat = True, AKS = True, MillerRabin = True, wilson_d = 5, div_d = 5, fermat_d = 8, AKS_d = 3, MillerRabin_d = 8):
    L = max(div_d, wilson_d, fermat_d)
    x_smooth = ny.linspace(1, 1.01*L, 200)
    x = [i for i in range(1, L+1)]
    H = 1
    h = 1
    if wilson == True:
        y_Wilson = [Test_wilson(i, tests) for i in range(1, 1 + wilson_d)]
        H = max(y_Wilson)
        h = min(y_Wilson)
        A_w, B_w = Exp_fit([i for i in range(1, 1 + wilson_d)], y_Wilson)
        plt.scatter([i for i in range(1, 1 + wilson_d)], y_Wilson, color = 'green', label = 'Wilson', marker = 'o', s = 4)
        plt.plot(x_smooth, [A_w*(ny.exp(B_w*z)) for z in x_smooth], color = 'green', label = 'Fitted Wilson')
    print("Wilson")
    if div == True:
        y_div = [Test_div(i, tests) for i in range(1, 1 + div_d)]
        plt.scatter([i for i in range(1, 1 + div_d)], y_div, marker = 'o', color = 'orange', label = 'Divisability', s = 4)
        A_d, B_d = Exp_fit([i for i in range(1, 1 + div_d)], y_div)
        plt.plot(x_smooth, [A_d*(ny.exp(B_d*z)) for z in x_smooth], color = 'orange', label = 'Fitted Divisability')
        H = max(max(y_div), H)
        h = min(min(y_div), h)
    print("Div")
    if fermat == True:
        y_fermat = [Test_fermat(i, tests) for i in range(1, 1 + fermat_d)]
        plt.scatter([i for i in range(1, 1 + fermat_d)], y_fermat, color = 'purple', label = 'Fermat', marker = 'o', s = 4)
        H = max(max(y_fermat), H)
        h = min(min(y_fermat), h)
    print("Fermat")
    if MillerRabin == True:
        y_MillerRabin = [Test_MillerRabin(i, tests) for i in range(1, 1 + MillerRabin_d)]
        plt.scatter([i for i in range(1, 1 + MillerRabin_d)], y_MillerRabin, marker = 'o', color = 'red', label = 'Miller Rabin', s = 4)
        H = max(max(y_MillerRabin), H)
        h = min(min(y_MillerRabin), h)
    print("MillerRabin")
    if AKS == True:
        y_AKS = [Test_AKS(i, tests) for i in range(1, 1 + AKS_d)]
        plt.scatter([i for i in range(1, 1 + AKS_d)], y_AKS, marker = 'o', color = 'blue', label = 'AKS (D)', s = 4)
        A_a, B_a = Exp_fit([i for i in range(1, 1 + AKS_d)], y_AKS)
        plt.plot(x_smooth, [A_a*(ny.exp(B_a*z)) for z in x_smooth], color = 'blue', label = 'Fitted AKS')
        H = max(max(y_AKS), H)
        h = min(min(y_AKS), h)
    print("AKS")
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Number of Digits')
    plt.ylim([0.9*h, 10*H])
    plt.ylabel('Average time taken per number tested (seconds)')
    plt.title('Efficiency of different methods for verifying primes')
    plt.legend()
    plt.show()
    
if __name__== "__main__":
    Plot_Test(tests = 60, # takes a while to run
            wilson_d = 6,
            div_d = 7,
            fermat_d = 220,
            AKS_d = 3,
            MillerRabin_d = 220)
    # The function produced GraphPrimeTestSpeeds
    pass
