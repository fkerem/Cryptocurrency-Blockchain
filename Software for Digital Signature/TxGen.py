"""
TxGen.py

GROUP MEMBERS:
Faik Kerem Ors
Mustafa Aydin

"""

import sys
import DSA
from random import *
import hashlib

if sys.version_info < (3, 6):
    import sha3

def payee(): # To generate a payee name arbitrarily.
    payee = ""
    for i in range(10):
        num = randint(48, 90)
        while(num > 57 and num < 65):
            num = randint(48, 90)
        payee += chr(num)
        
    return payee

def satoshi(): # To generate a satoshi amount arbitrarily.
    return str(randint(1, 999))

def nineLine(p, q, g, beta): # First nine lines of single transaction.
    transaction = \
    "*** Bitcoin transaction ***" + "\n" + \
    "Serial number: " + str(DSA.bitGenerator(2**128-1)) + "\n" + \
    "Payer: " + payee() + "\n" + \
    "Payee: " + payee() + "\n" + \
    "Amount: " + satoshi() + " Satoshi" + "\n" + \
    "p: " + str(p) + "\n" + \
    "q: " + str(q) + "\n" + \
    "g: " + str(g) + "\n" + \
    "Public Key (beta): " + str(beta) + "\n"

    return transaction

def GenSingleTx(p, q, g, alpha, beta): # Generating single transaction text file.
    transaction = nineLine(p, q, g, beta) # First nine lines will be hashed and signed.
    (r, s) = DSA.SignGen(transaction, p, q, g, alpha, beta)
    transaction += \
    "Signature (r): " + str(r) + "\n" + \
    "Signature (s): " + str(s) + "\n"
    
    return transaction # Returns the transaction string.
