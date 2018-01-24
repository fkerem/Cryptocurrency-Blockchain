"""
GROUP MEMBERS:
- Faik Kerem ORS
- Mustafa AYDIN

Readme.txt:
Required modules: random, sys, hashlib, sha3

Please read the comments below for further explanation.
"""

from random import *
import sys
import hashlib

if sys.version_info < (3, 6):
    import sha3

def serialnoncegenerator(): # To generate uniformly randomly 128-bit integer
    serial = str(randint(0, 2**128 - 1))
    return serial

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

def PoWGenerator(transaction): # To generate a valid Proof of Work
    new_tr = ""
    PoW = ""
    while True:
        nonce = serialnoncegenerator()
        noncestr = "Nonce: " + nonce + "\n"
        new_tr = transaction + noncestr # Transaction is updated adding Nonce line.
        PoW = hashlib.sha3_256(new_tr).hexdigest()
        if PoW[:6] == "000000": # While the first 6 digits of the hash digest is not 0,
            break               # nonce value is changed and the transaction is hashed again.
    trPoW = "Proof of Work: " + PoW + "\n"
    new_tr = new_tr + trPoW # Transaction is updated adding PoW line.

    return (PoW,new_tr) # Returning PoW and valid transaction.


# To generate a transaction text excluding Nonce and PoW lines.
def trWoutLastTwoLines(prevHash):
    transaction = \
    "*** Bitcoin transaction ***" + "\n" + \
    "Serial number: " + serialnoncegenerator() + "\n" + \
    "Payer: User Name" + "\n" + \
    "Payee: " + payee() + "\n" + \
    "Amount: " + satoshi() + " Satoshi" + "\n" + \
    "Previous hash in the chain: " + prevHash + "\n"
    
    return transaction

result = []
prevHash = "" # The hash of the previous transaction.
for i in range(10): # To generate 10 transactions.
    if i == 0:
        prevHash = "First transaction"
    transaction = trWoutLastTwoLines(prevHash) # Generate a transaction without having last 2 lines.
    prevHash, transaction = PoWGenerator(transaction) # Generating PoW for the current transaction and updating the transaction.
    result.append(transaction)

# Generating the output file.
myFile = open("LongestChain.txt", "w")
for tra in result:
    myFile.write(tra)
myFile.close()
