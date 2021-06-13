#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 12:31:44 2020

@authors:
Verifiers: Alessandro Busatto, Paolo Graziani, Aurora Rossi, Davide Roznowicz;
Applet: Giacomo Di Maggio, Marco Emporio, Marco Fattorelli, Sebastiano Gaiardelli, Francesco Trotti;
Map: Rosario Di Matteo, Marco Emporio, Adriano Tumminelli;
OneDrive: Marco Fattorelli, Davide Roznowicz;
Integration: Alice Raffaele, Romeo Rizzi.

"""

import argparse
import create_exercise_free as mode_free
import create_exercise_verifier as mode_ver
from distutils.dir_util import copy_tree
import glob
import hashlib
import os
import sys

ALL_EXER_PREFIX = 'esame-RO_'
ALL_EXER_SUFFIX = '_tutti-gli-es'
COLLECTION_FOLDER = 'collections/'

def add_graph_utils(path_folder):
    """It adds graph utils
    Parameters:"""
    copy_tree('./utils/graph_utils/js',path_folder+'/graph_utils/js')
    copy_tree('./utils/graph_utils/css',path_folder+'/graph_utils/css')

def add_all_exercises(exam_date, path_all, path_collection):
    """ It creates a folder for each type of exercises and inside it adds a subfolder for each instance
    Parameters:
    exam_date (str): YYYY-MM-DD
    path_all (str): path where to save all the generated exercises
    path_collection (str): path where to find all .yaml instances"""
    if not os.path.isdir(path_collection):
        print(f"\nATTENTION: Collection folder non found! Could not find {path_collection}")
        exit(1)
    type_list = [x for x in sorted(os.listdir(path_collection)) if '.DS_Store' not in x and 'graphml-'+exam_date not in x]
    print(f"\nTaking from collection folder {path_collection}\n   List of the exercise types included: {type_list}")
    for i in range(len(type_list)):
        print('Type: ' + type_list[i])
        os.mkdir(path_all + '/' + type_list[i])
        path_type = path_collection + '/' + type_list[i]
        nb_ex_type = len(glob.glob(os.path.join(path_type, '*.yaml'))) # there must be at least one exercise for each type
        assert nb_ex_type > 0
        for j in range(nb_ex_type):
            path_full_yaml = path_type + '/' + type_list[i] + str(j) + '.yaml'
            path_almost_yaml = path_type + '/' + type_list[i] + str(j) # (misses '.yaml')
            if j+1>=9:
                path_ex = path_all + '/' + type_list[i] + '/istanza_' + str(j+1)
            else:
                path_ex = path_all + '/' + type_list[i] + '/istanza_0' + str(j+1)
            print(path_ex)
            os.mkdir(path_ex)
            if type_list[i] in ['dp_poldo', 'dp_lcs', 'dp_robot_no_gemme', 'dp_triangle', 'dp_knapsack']: # mode_ver
                mode_ver.create_exercise(exam_date, str(i+1), path_ex, type_list[i], path_full_yaml, path_almost_yaml)
            else: # mode_free o mode_applet
                mode_free.create_exercise(exam_date, str(j+1), path_ex, path_full_yaml)
            print('Exercise ' + str(j+1) + ' added')
        if type_list[i] in ['graphs_flows_and_cuts', 'graphs_planarity', 'graphs_shortest_paths', 'graphs_min_spanning_trees']:
            add_graph_utils(path_all + '/' + type_list[i])
    return

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''Script to generate all possible exercises for a given date, relying on a proper collection folder''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    args=parser.parse_args()
    
    eserciziario = False
    assert len(sys.argv) == 2
    exam_date = str(sys.argv[1])
   

    global PATH_ALL_EXER
    PATH_ALL_EXER = os.getcwd() + '/' + ALL_EXER_PREFIX + exam_date + ALL_EXER_SUFFIX
    PATH_COLLECTION = os.getcwd() + '/' + COLLECTION_FOLDER + "RO-" + exam_date
    
    if os.path.exists(PATH_ALL_EXER):
        answer = input(f"The target folder {PATH_ALL_EXER} already exists! Are you sure you want to erase it, and generate again the folder with all exercises? Enter 'y' or 'Y' if you want me to proceed: ")
        if answer not in ("y", "Y"):
            print("Operation aborted. This call has had no effect.")
            exit(0)
        for root, dirs, files in os.walk(PATH_ALL_EXER, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(PATH_ALL_EXER)
        print(f"I have removed the old folder ({PATH_ALL_EXER}). Now building up the new one ...\n")
    os.mkdir(PATH_ALL_EXER)
    add_all_exercises(exam_date, PATH_ALL_EXER, PATH_COLLECTION)
