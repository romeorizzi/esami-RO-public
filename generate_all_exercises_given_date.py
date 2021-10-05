#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import glob
import hashlib
import shutil
from distutils.dir_util import copy_tree
import time

import create_exercise_free as mode_free
import create_exercise_verifier as mode_ver
from our_commons import COLLECTION_FOLDER, check_active_conda_env

ALL_EXER_PREFIX = 'esame-RO_'
ALL_EXER_SUFFIX = '_whole-compiled-collection'

def add_graph_utils(path_folder):
    """It adds graph utils
    Parameters:"""
    copy_tree(os.path.join(os.getcwd(),'utils','graph_utils','js'),os.path.join(path_folder,'graph_utils','js'))
    copy_tree(os.path.join(os.getcwd(),'utils','graph_utils','css'),os.path.join(path_folder,'graph_utils','css'))

def add_all_exercises(exam_date, path_all, path_collection):
    """ It creates a folder for each of the exercise types for that exam, this folder contains a subfolder for each instance of that exercise type 
    Parameters:
    exam_date (str): YYYY-MM-DD
    path_all (str): path where to save all the generated exercises
    path_collection (str): path where to find all .yaml instances"""
    if not os.path.isdir(path_collection):
        print(f"\nATTENTION: Collection folder not found! Could not find {path_collection}")
        exit(1)
    type_list = [x for x in sorted(os.listdir(path_collection)) if '.DS_Store' not in x and 'graphml-'+exam_date not in x]
    print(f"\nTaking from collection folder {path_collection}\n   List of the exercise types included: {type_list}")
    for i in range(len(type_list)):
        print(f'\nNow adding Exercise {str(i+1)} (of Type: {type_list[i]})')
        os.mkdir(os.path.join(path_all,type_list[i]))
        path_type = os.path.join(path_collection,type_list[i])
        num_instances = len(glob.glob(os.path.join(path_type, '??'))) # there must be at least one exercise for each type
        assert num_instances > 0
        for j in range(1, 1+num_instances):
            path_full_yaml = os.path.join(path_type,str(j).zfill(2),f"{type_list[i]}.yaml")
            path_ex = os.path.join(path_all,type_list[i],f"istanza_{str(j).zfill(2)}")
            print(path_ex)
            os.mkdir(path_ex)
            if type_list[i] in ['dp_poldo', 'dp_lcs', 'dp_robot_no_gemme', 'dp_triangle', 'dp_knapsack']: # mode_ver
                mode_ver.create_exercise(exam_date, str(i+1), path_ex, type_list[i], path_full_yaml)
            else: # mode_free o mode_applet
                mode_free.create_exercise(exam_date, str(i+1).zfill(2), path_ex, path_full_yaml)
            print(f'Instance {str(j).zfill(2)} added (for Exercise {str(i)})')
        print(f'Exercise {str(i+1)} added! (Its type was {type_list[i]})')
        if type_list[i] in ['graphs_flows_and_cuts', 'graphs_planarity', 'graphs_shortest_paths', 'graphs_min_spanning_trees']:
            add_graph_utils(os.path.join(path_all,type_list[i]))
            

if __name__ == "__main__":
    check_active_conda_env("ROexam")
    parser=argparse.ArgumentParser(
    description='''Script to generate all possible exercises for a given date, relying on a proper collection folder''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    args=parser.parse_args()
    
    assert len(sys.argv) == 2
    exam_date = str(sys.argv[1])
   

    global PATH_ALL_EXER
    PATH_ALL_EXER = os.path.join(os.getcwd(),ALL_EXER_PREFIX + exam_date + ALL_EXER_SUFFIX)
    PATH_COLLECTION = os.path.join(os.getcwd(),COLLECTION_FOLDER,exam_date)
    
    if os.path.exists(PATH_ALL_EXER):
        answer = input(f"The target folder {PATH_ALL_EXER} already exists! Are you sure you want to erase it, and generate again the folder with all exercises? Enter 'y' or 'Y' if you want me to proceed: ")
        if answer not in ("y", "Y"):
            print("Operation aborted. This call has had no effect.")
            exit(0)
        shutil.rmtree(PATH_ALL_EXER)
        print(f"I have removed the old folder ({PATH_ALL_EXER}). Now building up the new one ...\n")
    start_time = time.time()
    os.mkdir(PATH_ALL_EXER)
    add_all_exercises(exam_date, PATH_ALL_EXER, PATH_COLLECTION)
    print("\nFinished!\nThe whole generation process took  %s seconds." % (time.time() - start_time))
