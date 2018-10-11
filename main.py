import sympy, random
x = sympy.Symbol('x')

"""
map the polynomial res to GF(2)
@param res: the polynomial to map to GF(2)
returns the polynomial res mapped to GF(2)
"""
def GF(res):
    coeffs = res.all_coeffs()
    return sympy.Poly.from_list([abs(coeffs[i]%2) for i in range(len(coeffs))],gens=x)
    
def main():
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
    print("Ya:  {0}\nYb:  {1}\nYba: {2}\nYab: {3}\nkey: {4}".format(Ya,Yb,Yba,Yab,key))
    
if __name__ == "__main__":
    main()