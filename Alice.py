from main import generate_nonce, nonceSubtract, diffieHellman, encoder, decoder
import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES
import socket

def main():
    alice = "Alice"
    aliceKey = diffieHellman()
    aliceNonce = generate_nonce()
    
    #1. Alice sends a request to Bob
    msg = [alice]
    #send msg to bob
    
    #3. Alice sends a message to the server identifying herself and Bob, telling the server she wants to communicate with Bob.
    msgInner = encryptedMsg
    msg = [alice, bob, aliceNonce, msgInner]
    #send msg to server
    
    #5. Alice forwards the key to Bob who can decrypt it with the key he shares with the server, thus authenticating the data.
    decryptedServerMsg = DES.frombits(DES.decrypt(encryptedNewMsg,aliceKey))
    serverMsg = decoder.decode(decryptedServerMsg)
    aliceKab = serverMsg[2]
    toBob = serverMsg[3]
    #send toBob to Bob
    
    #7. Alice performs a simple operation on the nonce, re-encrypts it and sends it back verifying that she is still alive and that she holds the key.
    decryptedBobMsg = DES.frombits(DES.decrypt(encryptedNewMsg,aliceKab))
    decryptedBob = decoder.decode(decryptedBobMsg)
    newMsg = [nonceSubtract(decryptedBob[0])]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),aliceKab)
    #send encryptedNewMsg to Bob

if __name__ == "__main__":
    main()