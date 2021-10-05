#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

def usage():
    print(f"""This script ({sys.argv[0]}) asks for a "poldo" sequence seq of integers and a coloring col of seq meant to decompose seq into monotonic subsequences (Dilworth theorem). Right now this script only works out the decomposition and checks the monotonicity. 

Synopsis:
   ${sys.argv[0]} [SC|SD|NC|ND]

where:
  SC=strettamente crescente
  SD=strettamente decrescente
  NC= non crescente
  ND= non decrescente

Usage example:
   ${sys.argv[0]} 

to only get the subsequences.

""")

CEND      = '\33[0m'
CBOLD     = '\33[1m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'



def subseq_of_color(c, seq, coloring):
    return [val for val,i in zip(seq,coloring) if i==c]
    
if __name__ == "__main__":
    if len(sys.argv) != 1:
        print(f"Error: This script requires no argument, you called it with {len(sys.argv)-1} arguments!\n")
        usage()
        exit(1)

    print('Inserire la "poldo" sequenza di numeri interi:') 
    seq=list(map(int,input(" seq=").lstrip('[').rstrip(']').split(','))) 
    print('Ora la sequenza di coloring per la sequenza s:') 
    col=list(map(int,input(" col=").lstrip('[').rstrip(']').split(',')))

    print(f"seq={seq}")
    print(f"col={col}")
    C=max(col)
    for c in col:
        assert 1 <= c <= C
    for c in range(1,1+C):
        print(subseq_of_color(c, seq, col))

    exit(0)

