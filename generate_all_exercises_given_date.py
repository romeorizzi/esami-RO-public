#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:31:44 2020

@authors: Alice Raffaele, Alessandro Busatto, Marco Emporio, Marco Fattorelli, Romeo Rizzi, Aurora Rossi, Francesco Trotti

"""
import argparse
import create_exercise_free as mode1
#import create_exercise_verifier as mode2
#import create_exercise_applet as mode3
import hashlib
import os
import sys

ALL_EXER_PREFIX = 'esame_RO_' 
ALL_EXER_SUFFIX = '_tutti_gli_es'
COLLECTION_FOLDER = 'collections/'

def add_all_exercises(exam_date, path_all, path_collection):
    """ It creates a folder for each type of exercises and inside it adds a subfolder for each instance
    Parameters:
    exam_date (str): YYYY-MM-DD
    path_all (str): path where to save all the generated exercises
    path_collection (str): path where to find all .yaml instances"""
    type_list = [x for x in os.listdir(path_collection) if '.DS_Store' not in x]
    print(type_list)
    for i in range(len(type_list)):
        print('Type: ' + type_list[i])
        os.mkdir(path_all + '/' + type_list[i])
        path_type = path_collection + '/' + type_list[i]
        nb_ex_type = len(os.listdir(path_type)) # indexing file da 0
        for j in range(nb_ex_type):
            chosen_type_yaml = path_type + '/' + type_list[i] + str(j) + '.yaml'
            if j+1>=9:
                path_ex = path_all + '/' + type_list[i] + '/istanza_' + str(j+1)
            else:
                path_ex = path_all + '/' + type_list[i] + '/istanza_0' + str(j+1)
            print(path_ex)
            os.mkdir(path_ex)
            mode1.create_exercise(exam_date, str(j+1), path_ex, chosen_type_yaml)
            #mode2.create_exercise(str(i+1), path_ex, chosen_type_yaml)
            #mode3.create_exercise(str(i+1), path_ex, chosen_type_yaml)
            print('Exercise ' + str(j+1) + ' added')
    return

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''Script to generate all possible exercises for a given date, relying on a proper collection folder''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    args=parser.parse_args()
    
    assert len(sys.argv) == 2
    exam_date = str(sys.argv[1])
    
    os.mkdir(os.getcwd() + '/' + ALL_EXER_PREFIX + exam_date + ALL_EXER_SUFFIX)
    path_all = os.getcwd() + '/' + ALL_EXER_PREFIX + exam_date + ALL_EXER_SUFFIX
    path_collection = os.getcwd() + '/' + COLLECTION_FOLDER + "RO-" + exam_date
    add_all_exercises(exam_date, path_all, path_collection)
