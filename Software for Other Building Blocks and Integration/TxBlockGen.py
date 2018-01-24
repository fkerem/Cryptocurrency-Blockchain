"""
TxBlockGen.py

"""

import DSA
from random import *

def satoshi(): # To generate a satoshi amount arbitrarily.
    return str(randint(1, 999))

def BeforeSign(p, q, g, payer_b, payee_b): #The Lines of the Transaction to be Signed
    transaction = \
    "*** Bitcoin transaction ***" + "\n" + \
    "Serial number: " + str(DSA.bitGenerator(2**128-1)) + "\n" + \
    "p: " + str(p) + "\n" + \
    "q: " + str(q) + "\n" + \
    "g: " + str(g) + "\n" + \
    "Payer Public Key (beta): " + str(payer_b) + "\n" + \
    "Payee Public Key (beta): " + str(payee_b) + "\n" + \
    "Amount: " + satoshi() + " Satoshi" + "\n"
    return transaction

def TransactionGen(p, q, g): #Generating one transaction
    (payer_a, payer_b) = DSA.KeyGen(p, q, g) #Generating Keys for Payer
    (payee_a, payee_b) = DSA.KeyGen(p, q, g) #Generating Keys for Payee
    transaction = BeforeSign(p, q, g, payer_b, payee_b) #Generating first part of the Transaction
    (r, s) = DSA.SignGen(transaction, p, q, g, payer_a, payer_b) #Signing the Transaction
    transaction += \
    "Signature (r): " + str(r) + "\n" + \
    "Signature (s): " + str(s) + "\n"
    #Appending the signatures
    return transaction
    
def GenTxBlock(p, q, g, count): #Generating transactions based on count
    transactions = ""
    for i in range(0, count):
        transactions += TransactionGen(p, q, g)

    return transactions
