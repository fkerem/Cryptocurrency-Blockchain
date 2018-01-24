"""
PoW.py

"""

import DSA
import sys
import hashlib

if sys.version_info < (3, 6):
    import sha3

def rootMerkle(TxBlockFile, TxLen): #To Get the Root Hash of the Merkle Tree
    TxBlockFileBuffer = open(TxBlockFile, "r")
    lines = TxBlockFileBuffer.readlines()
    TxBlockFileBuffer.close()
    TxCount = len(lines)/TxLen #Num of Transactions in a Block
    
    hashTree = []
    for i in range(0,TxCount):
        transaction = "".join(lines[i*TxLen:(i+1)*TxLen])
        hashTree.append(hashlib.sha3_256(transaction).hexdigest())

    t = TxCount
    j = 0
    while(t>1):
        for i in range(j,j+t,2):
            hashTree.append(hashlib.sha3_256(hashTree[i]+hashTree[i+1]).hexdigest())
        j += t
        t = t>>1
    h = hashTree[2*TxCount-2]

    return h

def PoW(TxBlockFile, ChainFile, PoWLen, TxLen): #Updates LongestChain File for Each Block
    block = ""
    if TxBlockFile[-5] != "0":
        chainBuffer = open(ChainFile, "r")
        chain = chainBuffer.readlines()
        chainBuffer.close()
        block = chain[-1] #PoW for the Previous Transaction Block
    else: #for TransactionBlock0.txt
        block = "Day Zero Link in the Chain" + "\n"

    block += rootMerkle(TxBlockFile, TxLen) + "\n" #The Root Hash of the Merkle Tree

    while True:
        new_block = block + str(DSA.bitGenerator(2**128-1)) + "\n"
        new_PoW = hashlib.sha3_256(new_block).hexdigest()
        if new_PoW[:PoWLen] == "0"*PoWLen:
            new_PoW += "\n" #PoW
            block = new_block
            block += new_PoW
            break
    #Write/append to the ChainFile
    if TxBlockFile[-5] != "0":
        chainBuffer = open(ChainFile, "a")
        chainBuffer.write(block)
        chainBuffer.close()
    else: #for TransactionBlock0.txt
        chainBuffer = open(ChainFile, "w")
        chainBuffer.write(block)
        chainBuffer.close()

