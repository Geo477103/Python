# Plan is to implement ECDSA (Elliptic curve Digital Signature Algorithm) which uses the 
# Secp256k1 curve. This algorithm / curve is commonly used for bitcoin signatures.

# E: y^2 = x^3 + 7 this will be the only curve that is used in this file

from Rsa_code import invMod
import random as rd
import hashlib

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  #115792089237316195423570985008687907853269984665640564039457584007908834671663
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  #115792089237316195423570985008687907852837564279074904382605163141518161494337
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798 #55066263022277343669578718895168534326250603453777594175500187360389116729240
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8 #32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (Gx, Gy)

# Public Key
qA = 0

def ToBinary(n):
    return bin(n)[2:]


def Double_point(Point, prime):
    if Point == -1:
        return -1
    #print("start")
    x, y = Point
    if y == 0:
        return -1
    quot = invMod(2*y, prime)
    m = ( (3*pow(x, 2)) * quot) % prime
    c = (y - (m * x)) % prime
    x_cord = ( ((c**2) - 7) * invMod(x**2, prime)) % prime
    y_cord = (( m * (x - x_cord) ) - y) % prime         
    return (x_cord, y_cord)

def Add_points(P, Q, prime):
    if P == -1:
        return Q
    elif Q == -1:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        if y1 == y2:
            return(Double_point(P, prime))
        else:
            return -1
    else:
        m = ((y2 - y1) * invMod(x2 - x1, prime)) % prime
        x = (m**2 - x1 - x2) % prime
        y = ((m * (x1 - x)) - y1) % prime
        return (x, y)

def Mult_point(n, P, prime):
    powers = ToBinary(n)[::-1]
    run = -1
    for i in powers:
        if i == '1':
            run = Add_points(run, P, prime) 
        P = Double_point(P, prime)
    return run

def Sign(message, G, p, n):
    global qA
    E = int(hashlib.sha256(message.encode("UTF-8")).hexdigest(), 16)
    dA = rd.randint(1, n-1)
    qA = Mult_point(dA, G, p)
    k = rd.randint(1, n-1)
    x, y = Mult_point(k, G, p)
    r = x % n
    s = (invMod(k, n) * (E + (r * dA))) % n
    while r == 0 or s == 0:
        k = rd.randint(1, n-1)
        x, y = Mult_point(k, G, p)
        r = x % n
        s = (invMod(k, n) * (E + (r * dA))) % n
    return r, s

def Verify(message, r, s):
    if (r < 1) or (r >= n) or (s < 1) or (s >= n):
        return False
    E = int(hashlib.sha256(message.encode("UTF-8")).hexdigest(), 16)
    inv = invMod(s, n)
    u = (E * inv) % n
    v = (r * inv) % n
    R1 = Add_points(Mult_point(u, G, p), Mult_point(v, qA, p), p)
    if R1 == -1:
        return False
    x, _ = R1
    if x % n == r:
        return True
    else:
        return False

if __name__ == "__main__":
    r, s = Sign('Hello world', G, p, n)
    print(Verify('Hello World', r, s))



