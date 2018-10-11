import sympy
from numpy import array as nparray
from numpy import dtype
from numpy import poly1d
from numpy.polynomial.polynomial import polypow
from numpy import polydiv
import random

x = sympy.Symbol('x')

def GF(res):
    coeffs = res.all_coeffs()
    return sympy.Poly.from_list([abs(coeffs[i]%2) for i in range(len(coeffs))],gens=x)
    

def main():
    #hard-coded constants (you can change these if you want)
    primPoly = sympy.Poly.from_list([1,0,0,0,0,0,1,1],gens=x)

    G = 100
    
    #randomly choose A and B -> construct polynomials
    #Arand = random.randint(1,G); Brand = random.randint(1,G)
    Arand = 56
    Brand = 18
    A = sympy.Poly.from_list([1]+[0]*Arand,gens=x)
    B = sympy.Poly.from_list([1]+[0]*Brand,gens=x)
    
    #apply modulo -> map to Galois field GF(2)
    Ya = GF((sympy.div(A,primPoly,domain='QQ')[1]))
    Yb = GF((sympy.div(B,primPoly,domain='QQ')[1]))
    
    print(Ya,'\n',Yb)
    
    #exchange Ya and Yb : apply modulo -> map to Galois field GF(2)
    Yba = GF(sympy.div(GF(Yb**Arand),primPoly,domain='QQ')[1])
    Yab = GF(sympy.div(GF(Ya**Brand),primPoly,domain='QQ')[1])
    
    print(Yba,'\n',Yab)
    
if __name__ == "__main__":
    main()