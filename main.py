import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/')
import DES

x = sympy.Symbol('x')
encoder = json.JSONEncoder()
decoder = json.JSONDecoder()

"""
map the polynomial res to GF(2)
@param res: the polynomial to map to GF(2)
returns the polynomial res mapped to GF(2)
"""
def GF(res):
    coeffs = res.all_coeffs()
    return sympy.Poly.from_list([abs(coeffs[i]%2) for i in range(len(coeffs))],gens=x)

"""
Generate pseudorandom number.
"""
def generate_nonce(length=8):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

"""
subtract one from the specified nonce
@param nonce: the nonce to subtract from
"""
def nonceSubtract(nonce):
    smallestOne = nonce.rfind('1')
    if (smallestOne == -1):
        return "1" * len(nonce)
    return nonce[:smallestOne] + '0' + nonce[smallestOne+1:]

"""
diffie-hellman implementation
"""
def diffieHellman():
    #hard-coded constants (you can change these if you want)
    primPoly = sympy.Poly.from_list([1,0,0,0,0,0,0,0,0,1,1],gens=x)
    G = 100
    
    #randomly choose A and B -> construct polynomials
    Arand = random.randint(1,G)
    Brand = random.randint(1,G)
    
    A = sympy.Poly.from_list([1]+[0]*Arand,gens=x)
    B = sympy.Poly.from_list([1]+[0]*Brand,gens=x)
    
    #apply modulo -> map to Galois field GF(2)
    Ya = GF((sympy.div(A,primPoly,domain='QQ')[1]))
    Yb = GF((sympy.div(B,primPoly,domain='QQ')[1]))
    
    #exchange Ya and Yb : apply modulo -> map to Galois field GF(2)
    Yba = GF(sympy.div(GF(Yb**Arand),primPoly,domain='QQ')[1])
    Yab = GF(sympy.div(GF(Ya**Brand),primPoly,domain='QQ')[1])
    
    #convert poly to key 
    key = Yab.all_coeffs()
    key = [0] * (10-len(key)) + key
    
    #final verification
    #print("Ya:  {0}\nYb:  {1}\nYba: {2}\nYab: {3}\nkey: {4}".format(Ya,Yb,Yba,Yab,key))
    
    return key
    
def main():
    #generate random session key on the server for alice and bob to communicate
    Kab = [random.randint(0, 9) for _ in range(10)]
    
    alice = "Alice"
    bob = "Bob"
    aliceKey = diffieHellman()
    bobKey = diffieHellman()
    aliceNonce = generate_nonce()
    bobNonce = generate_nonce()
    bobNewNonce = generate_nonce()
    
    #1. Alice sends a request to Bob
    msg = [alice]
    #send msg to bob
    
    #2. Bob responds with a nonce encrypted under his key with the Server
    msg = [alice,bobNewNonce]
    encryptedMsg = DES.encrypt(DES.tobits(encoder.encode(msg)),bobKey)
    #send encryptedMsg to alice
    
    #3. Alice sends a message to the server identifying herself and Bob, telling the server she wants to communicate with Bob.
    msgInner = encryptedMsg
    msg = [alice, bob, aliceNonce, msgInner]
    #send msg to server
    
    #4. The server generates K_AB and sends back to Alice a copy encrypted under K_BS for Alice to forward to Bob and also a copy for Alice. 
    #Since Alice may be requesting keys for several different people, the nonce assures Alice that the message is fresh and that 
    #the server is replying to that particular message and the inclusion of Bob's name tells Alice who she is to share this key with.
    #Note the inclusion of the nonce.
    decryptedBobMsg = DES.frombits(DES.decrypt(msg[3],bobKey))
    decryptedBob = decoder.decode(decryptedBobMsg)
    decryptedBob.append(Kab)
    
    reEncryptedBob = DES.encrypt(DES.tobits(encoder.encode(decryptedBob)),bobKey)
    newMsg = [msg[1],msg[2],Kab,reEncryptedBob]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),aliceKey)
    #send encryptedNewMsg to alice
    
    #5. Alice forwards the key to Bob who can decrypt it with the key he shares with the server, thus authenticating the data.
    decryptedServerMsg = DES.frombits(DES.decrypt(encryptedNewMsg,aliceKey))
    serverMsg = decoder.decode(decryptedServerMsg)
    aliceKab = serverMsg[2]
    toBob = serverMsg[3]
    #send toBob to Bob
    
    #6. Bob sends Alice a nonce encrypted under K_AB to show that he has the key.
    decryptedAliceMsg = DES.frombits(DES.decrypt(toBob,bobKey))
    decryptedAlice = decoder.decode(decryptedAliceMsg)
    bobKab = decryptedAlice[2]
    newMsg = [bobNonce]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),bobKab)
    #send encryptedNewMsg to Alice
    
    #7. Alice performs a simple operation on the nonce, re-encrypts it and sends it back verifying that she is still alive and that she holds the key.
    decryptedBobMsg = DES.frombits(DES.decrypt(encryptedNewMsg,aliceKab))
    decryptedBob = decoder.decode(decryptedBobMsg)
    newMsg = [nonceSubtract(decryptedBob[0])]
    encryptedNewMsg = DES.encrypt(DES.tobits(encoder.encode(newMsg)),aliceKab)
    #send encryptedNewMsg to Bob

    #8. Bob see's that Alice's computation was correct. Hurray, we're ready to chat!
    decryptedAliceMsg = DES.frombits(DES.decrypt(encryptedNewMsg,bobKab))
    decryptedAlice = decoder.decode(decryptedAliceMsg)
    if (decryptedAlice[0] == nonceSubtract(bobNonce)):
        print("Success!")
    else:
        print("Error: Did not receive Bob Nonce - 1 from Alice")
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #1. Alice sends to server (Alice ID, Bob ID, Alice Nonce)
    #2. server sends to Alice (all encrypted with Alice key):
        #Alice Nonce, Bob ID, symmetric key,
            #symmetric key, Alice ID (these encrypted with Bob's key as well)
    #3. Alice sends Bob encrypted portion to Bob
    #4. Bob sends Bob Nonce to Alice 
    #5. Alice sends to Bob Bob Nonce - 1
    #6. Nonce verifies that it is indeed Nonce - 1

    
if __name__ == "__main__":
    main()