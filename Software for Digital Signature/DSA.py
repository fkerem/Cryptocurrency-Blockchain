"""
DSA.py

GROUP MEMBERS:
Faik Kerem Ors
Mustafa Aydin

"""

from random import *
import sys
import pyprimes
import warnings
import hashlib

if sys.version_info < (3, 6):
    import sha3

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m): # Modular inverse function
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist.
    else:
        return x % m

def bitGenerator(boundary): # Random Number Generator
    bits = randint(0, boundary)
    return bits

def generateG(p, q): # Generating g using p and q.
    g = 0
    while True:
        alpha = randint(2, p-1)
        g = pow(alpha, (p-1)/q, p)
        if g != 1:
            break
    return g

def DL_Param_Generator(small_bound, large_bound): #Parameter Generation
    q = 0
    p = 0
    while(True):
        q = bitGenerator(small_bound)

        warnings.simplefilter('ignore')
        check = pyprimes.isprime(q)
        warnings.simplefilter('default')
        if check == True:
            break
    while(True):
        k = randrange(1, large_bound/small_bound)
        p = q * k + 1
        warnings.simplefilter('ignore')
        check = pyprimes.isprime(p)
        warnings.simplefilter('default')
        if check == True:
                break

    g = generateG(p, q)
    return (q, p, g) #Returns q, p and g.

def KeyGen(p, q, g): # Key generation using p, q and g.
    alpha = randint(1, q-1)
    beta = pow(g, alpha, p)
    return (alpha, beta) # Returns the keys alpha and beta.

def SignGen(message, p, q, g, alpha, beta): # Signature Generation
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % q
    k = randint(1, q-1)
    r = pow(g, k, p) % q
    s = (alpha * r + k * h) % q
    return (r, s) # Returns the signature as a tuple (r, s).

def SignVer(message, r, s, p, q, g, beta): # Signature Verification
    h = int(hashlib.sha3_256(message).hexdigest(), 16)
    h = h % q
    v = modinv(h, q)
    z_one = (s*v) % q
    z_two = ((q - r) * v) % q
    u = (pow(g, z_one, p) * pow(beta, z_two, p)) % p

    if r == (u % q): # If r == (u mod q), signature is verified.
        return 1
    else:
        return 0 # Otherwise, signature is not verified.

