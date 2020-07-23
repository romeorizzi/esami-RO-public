#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 16:25:55 2020

@author: Alice Raffaele
"""
import argparse
import os
import random
import sys
import yaml

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''Script to generate new Poldo instances''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    args=parser.parse_args()
    
    assert len(sys.argv) == 2
    exam_date = str(sys.argv[1])

    description1 = "Si consideri la seguente sequenza di numeri naturali:<br>\["
    n = 25
    chosen_index = random.randint(1,n-1)
    chosen = 0
    for i in range(n-1):
        rand = random.randint(10, 99)
        description1 += str(rand) + ", "
        if i == chosen_index:
            chosen = rand
    description1 += str(random.randint(10, 99)) + "\]"
    task1 = "Trovare una sottosequenza crescente che sia la piu' lunga possibile"
    task2 = "Trovare quante sono le sottosequenze crescenti di lunghezza massima"
    task3 = "Una sequenza e' detta una _Z-sequenza_ , o sequenza crescente con un possibile ripensamento, se esiste un indice _i_ tale che ciascuno degli elementi della sequenza esclusi al piu' il primo e l'_i_-esimo sono strettamente maggiori dell'elemento che immediatamente li precede nella sequenza. Trovare la piu' lunga Z-sequenza che sia una sottosequenza della sequenza data"
    task4 = "Trovare la piu' lunga sottosequenza crescente che includa l'elemento di valore " + str(chosen)
    
    poldo_file = {'name' : "dp_poldo", 'title': "Sottosequenze crescenti e decrescenti",
                  'description1': description1,
                  'tasks': [{'tot_points': 5, 'ver_points': 5, 'description1': task1},
                  {'tot_points': 10, 'ver_points': 10, 'description1': task2},
                  {'tot_points': 10, 'ver_points': 10, 'description1': task3},
                  {'tot_points': 5, 'ver_points': 5, 'description1': task4}]}
    
    PATH_POLDO = os.getcwd() + '/../collection_' + exam_date + '/dp_poldo/'
    count = len(os.listdir(PATH_POLDO))
    instance_name = 'dp_poldo' + str(count) + '.yaml'
                  
    with open(PATH_POLDO + instance_name, 'w') as file:
        documents = yaml.dump(poldo_file, file, sort_keys = False)
