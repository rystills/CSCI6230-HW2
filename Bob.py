from main import generate_nonce, nonceSubtract, diffieHellman, encoder, decoder
import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES

def main():
    bob = "Bob"
    bobKey = diffieHellman()
    bobNonce = generate_nonce()
    bobNoncePrime = generate_nonce()
    
    #2. Bob responds with a nonce encrypted under his key with the Server
    msg = [alice,bobNoncePrime]
    encryptedMsg = DES.encrypt(DES.tobits(encoder.encode(msg)),bobKey)
    #send encryptedMsg to alice
    
    #6. Bob sends Alice a nonce encrypted under K_AB to show that he has the key.
    decryptedAliceMsg = DES.frombits(DES.decrypt(toBob,bobKey))
    decryptedAlice = decoder.decode(decryptedAliceMsg)
    bobKab = decryptedAlice[2]
    newMsg = [bobNonce]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),bobKab)
    #send encryptedNewMsg to Alice
    
    #8. Bob see's that Alice's computation was correct. Hurray, we're ready to chat!
    decryptedAliceMsg = DES.frombits(DES.decrypt(encryptedNewMsg,bobKab))
    decryptedAlice = decoder.decode(decryptedAliceMsg)
    if (decryptedAlice[0] == nonceSubtract(bobNonce)):
        print("Success!")
    else:
        print("Error: Did not receive Bob Nonce - 1 from Alice")

if __name__ == "__main__":
    main()