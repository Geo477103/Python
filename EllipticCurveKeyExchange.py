# Alice and Bob to obtain a shared secret key (can be used in symetric encryption system) by using elliptic curve key exchange / elliptic curve diffe-hellman
# curve they are using is: secp256r1, parameter listed below

from Rsa_code import invMod
from ECDSA import ToBinary
import random as rd

# secp256r1 parameters:
p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
n = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551

def DoublePoint(P, a, b, p):
    if P == -1:
        return -1
    x, y = P
    if y == 0: # If y == 0 the tangent to the point shoots off never to touch the curve again, so return -1.
        return -1
    slope = (((3*(x**2)) + a) * invMod(2*y,p)) % p
    c = (y - (slope * x)) % p
    newX = (c**2 - b) * invMod(x**2,p)
    newX = newX % p
    newY = slope * newX + c
    return newX, - newY % p
    

def AddPoint(P, Q, a, b, p):
    if P == -1:
        return Q
    if Q == -1:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == y2:
        return DoublePoint(P, a, b, p)
    elif x1 == x2:
        return -1
    slope = (y2 - y1) * invMod(x2 - x1,p)
    c = y1 - slope * x1
    newX = (c**2 - b) * invMod(x1*x2,p)
    newX = newX % p
    newY = slope * newX + c
    return newX , - newY % p

def MultPoint(n, P, a, b, p):
    powers = ToBinary(n)[::-1]
    run = -1
    for i in powers:
        if i == '1':
            run = AddPoint(run, P, a, b, p) 
        P = DoublePoint(P, a, b, p)
    return run


# Public Keys/information

#aG:    Alice releases the result of k_a * G 
#bG:    Bob releases the result of k_b * G

def Alice_setup():
    k_a = rd.randint(1, n-1)
    aG = MultPoint(k_a, G, a, b, p)
    return k_a, aG

def Bob_setup():
    k_b = rd.randint(1, n-1)
    bG = MultPoint(k_b, G, a, b, p)
    return k_b, bG

def Alice_calc(k_a, bG):
    return(MultPoint(k_a, bG, a, b, p))

def Bob_calc(k_b, aG):
    return(MultPoint(k_b, aG, a, b, p))

def ECDH_Main():
    k_a, aG = Alice_setup()
    k_b, bG = Bob_setup() 
    K_A = Alice_calc(k_a, bG)
    K_B = Bob_calc(k_b, aG)
    # key currently in the form of a coordinate but can take just the x_coordinate as a key, for example
    print("Alice Obtains K: ", K_A)
    print("Bob Obtains K:   ", K_B)
    if K_A != K_B:
        print("Key Exchange Failed")

if __name__ == "__main__":
    ECDH_Main()



