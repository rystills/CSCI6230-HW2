import sympy, random, sys
try: import simplejson as json
except ImportError: import json
sys.path.insert(0, 'DES/'); import DES

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
    #hard-coded constants (you can change these if you want, but primpoly should stay degree 10)
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
    pass

    
if __name__ == "__main__":
    main()