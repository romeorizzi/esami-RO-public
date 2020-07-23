#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 10:24:17 2020

@author: Alice Raffaele
"""
import argparse
import os
import random
import sys
import yaml

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''Script to generate new Knapsack instances''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    args=parser.parse_args()
    
    assert len(sys.argv) == 2
    exam_date = str(sys.argv[1])

    n = 12
    B = 30
    description1 = "Si considerino uno zaino di capienza B = " + str(B) + " e i seguenti oggetti, con i loro rispettivi pesi e valori (p, v):<br>"
    offset = 5
    max_value = 20
    best_item_value = 0
    chosen = 0
    nb_exceeding = 0
    max_nb_exceeding = 3
    i = 0
    while i < n:
        if nb_exceeding < max_nb_exceeding:
            random_weight = random.randint(1,B+offset)
        else:
            random_weight = random.randint(1,B)
            if random_weight > B:
                nb_exceeding += 1
        if nb_exceeding >= max_nb_exceeding:
            continue;
        random_value = random.randint(1,max_value)
        description1 += str(i+1) + ": (" + str(random_weight) + ", " + str(random_value) + ")<br>"
        if random_weight <= B and random_value > best_item_value:
            best_item_value = random_value
            chosen = i+1
        i += 1
            
    # for i in range(n):
    #     random_weight = random.randint(1,B+offset)
    #     random_value = random.randint(1,max_value)
    #     description1 += str(i+1) + ": (" + str(random_weight) + ", " + str(random_value) + ")\n"
    #     if random_weight <= B and random_value > best_item_value:
    #         best_item_value = random_value
    #         chosen = i+1

    task1 = "Trovare un sottoinsieme di oggetti che abbia massimo valore possibile e il cui peso complessivo non ecceda B = " + str(B)
    task2 = "A un certo punto l'oggetto " + str(chosen) + " non e' piu' disponibile. Dire se e come varia la soluzione appena trovata"
    task3 = "L'oggetto " + str(chosen) + " torna disponibile ma ora e' variato B, diventato B' = " + str(B-offset) + ". Trovare un sottoinsieme di oggetti che abbia massimo valore possibile e il cui peso complessivo non ecceda B'"
    task4 = "Indicare e descrivere brevemente una possibile applicazione del problema dello zaino nella vita quotidiana"
    
    knapsack_file = {'name' : "dp_knapsack", 'title': "Problema dello zaino",
                  'description1': description1,
                  'tasks': [{'tot_points': 15, 'ver_points': 15, 'description1': task1},
                  {'tot_points': 10, 'ver_points': 10, 'description1': task2},
                  {'tot_points': 10, 'ver_points': 10, 'description1': task3},
                  {'tot_points': 5, 'ver_points': 5, 'description1': task4}]}
    
    PATH_KNAPSACK = os.getcwd() + '/../collection_' + exam_date + '/dp_knapsack/'
    count = len(os.listdir(PATH_KNAPSACK))
    instance_name = 'dp_knapsack' + str(count) + '.yaml'
                  
    with open(PATH_KNAPSACK + instance_name, 'w') as file:
        documents = yaml.dump(knapsack_file, file, sort_keys = False)
