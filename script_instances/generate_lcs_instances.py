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

    description1 = "Trovare la piu' lunga sottosequenza comune tra le stringhe _s_ = ?s? e _t_ = ?t?"
    
    n = 17
    chosen_index_suff = random.randint(int(n/4), int(n*3/4))
    chosen_index_pref = random.randint(int(n/4), int(n*3/4))
    alphabet = ['A', 'C', 'G', 'T']
    s = ''
    t = ''
    for i in range(n):
        s += alphabet[random.randint(0, len(alphabet)-1)]
        t += alphabet[random.randint(0, len(alphabet)-1)]
    description1 = description1.replace('?s?', s).replace('?t?', t)
    description2 = "Fare lo stesso con alcuni suffissi di _s_ e _t_."
    
    t_suffix = t[-(chosen_index_suff+1):]
    s_pref = s[:chosen_index_pref+1]
    
    task1 = "Dire qual e' la piu' lunga sottosequenza comune tra _s_ e _t_"
    #task2 = "Dire qual e' la piu' lunga sottosequenza comune tra _s_ e _t_ che incomincia con 'C'"
    task3 = "Dire qual e' la piu' lunga sottosequenza comune tra _s_ e il suffisso _t" + str(chosen_index_suff +1) + "_ = " + t_suffix + " di _t_"
    task4 = "Dire qual e' la piu' lunga sottosequenza comune tra _t_ e il prefisso _s" + str(chosen_index_pref +1) + "_ = " + s_pref + " di _s_"
    
    lcs_file = {'name' : "dp_string", 'title': "Sottosequenza comune",
                  'description1': description1, 'description2': description2,
                  'tasks': [{'tot_points': 10, 'ver_points': 10, 'description1': task1},
                  #{'tot_points': 5, 'ver_points': 5, 'description1': task2},
                  {'tot_points': 10, 'ver_points': 10, 'description1': task3},
                  {'tot_points': 10, 'ver_points': 10, 'description1': task4}]}
    
    PATH_LCS = os.getcwd() + '/../collection_' + exam_date + '/dp_string/'
    count = len(os.listdir(PATH_LCS))
    instance_name = 'dp_string' + str(count) + '.yaml'
                  
    with open(PATH_LCS + instance_name, 'w') as file:
        documents = yaml.dump(lcs_file, file, sort_keys = False)
