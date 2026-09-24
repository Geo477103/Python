# Use 'textbook RSA' to encrypt message, this method is insecure to certain attacks 

from Prime_Test import Fermat_test 
import random as rd
import math
import sympy
import time

def invMod(a, n): # inverse of a mod n, given (a, n) = 1, a < n
    if a == 0:
        print('here8')
    a = a % n
    if a == 0:
        print('here6')
    N = n
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    q = n // a
    r = a
    while r != 1:
        u2 = u0 - (q * u1) 
        v2 = v0 - (q * v1) 
        u0, v0 = u1, v1
        u1, v1 = u2, v2
        r = n % a
        n = a
        a = r
        q = n // a       
        #print(r, u1, v1, q)
         
    return v1 % N

def hcf(a, b):
    x, y = max(a, b), min(a, b)
    r = x % y
    if r == 0:
        return y
    while r != 0:
        x = y
        y = r
        r = x % y
    return(y)

def Generate_prime(bits, fermat_tests = 1000):
    num = rd.randint(1 << (bits - 1), (2 << (bits - 1)) - 1) # [2, 3]    
    while not Fermat_test(num, fermat_tests):
        num = rd.randint(1 << (bits - 1), (2 << (bits - 1)) - 1)
    return num

def RSA(message, key_bits): # general method of RSA 
    p, q = Generate_prime(key_bits // 2), Generate_prime(key_bits // 2)
    n = p*q
    totient_n = (p - 1) * (q - 1)
    e = rd.randint(2, totient_n - 1)
    while hcf(e, totient_n) != 1:
        e = rd.randint(2, totient_n - 1)
    d = invMod(e, totient_n)
    d_check = pow(e, -1, totient_n)
    if d != d_check:
        print("Inverse calculation is wrong")
    c = pow(message, e, n)
    return c

# Alice sending message to Bob 

def Bob(key_size):
    p, q = Generate_prime(key_size // 2), Generate_prime(key_size // 2)
    n = p * q
    n_totient = (p - 1) * (q - 1)
    e = rd.randint(2, n_totient - 1)
    while hcf(e, n_totient) != 1:
        e = rd.randint(2, n_totient - 1)
    d = invMod(e, n_totient)
    
    return n, e, d

def Alice(mes, e, n):
    c = pow(mes, e, n)
    return c

def Bob_decrypt(cipher, d, n):
    mes_decrypt = pow(cipher, d, n)
    return mes_decrypt

def RSA_process(key_size, message, Show_Ciphertext = True, Show_Decryption = True):
    #print("start")
    n, e, d = Bob(key_size)
    ciphertext = Alice(message, e, n)
    if Show_Ciphertext:
        print("Cipher Text:", ciphertext)
    decrypted = Bob_decrypt(ciphertext, d, n)
    if Show_Decryption:
        print("Decrypted Message:", decrypted)
    return

if __name__ == "__main__":
    key_size = 16
    mes = rd.randint(0, 1 << key_size)
    print("Mes:", mes)
    n, e, _ = Bob(32)
    cipher = Alice(mes, e, n) 
    print("Cipher Text:", cipher) 
    #RSA_process(128, 7327432965485)
