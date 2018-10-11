'''
Created on Oct 10, 2018

@author: Ryan
'''
import sympy
from numpy import array as nparray
from numpy import dtype
from numpy import poly1d
from numpy.polynomial.polynomial import polypow
from numpy import polydiv
import random

def GF(res):
    return poly1d(nparray([abs(res[i]%2) for i in range(res.order,-1,-1)],dtype=object))

def main():
    #hard-coded constants (you can change these if you want)
    primPoly = poly1d(nparray([1,0,0,0,0,0,1,1],dtype=object))
    G = 100
    
    #randomly choose A and B -> construct polynomials
    #Arand = random.randint(1,G); Brand = random.randint(1,G)
    Arand = 53
    Brand = 34
    A = poly1d(nparray([1]+[0]*Arand,dtype=object))
    B = poly1d(nparray([1]+[0]*Brand,dtype=object))
    
    #apply modulo -> map to Galois field GF(2)
    Ya = GF((A/primPoly)[1])
    Yb = GF((B/primPoly)[1])
    
    print(Ya,'\n',Yb)
    
    #exchange Ya and Yb : apply modulo -> map to Galois field GF(2)
    Yba = GF((GF(Yb**Arand)/primPoly)[1])
    Yab = GF((GF(Ya**Brand)/primPoly)[1])
    
    print(Yba,'\n',Yab)
    
if __name__ == "__main__":
    main()