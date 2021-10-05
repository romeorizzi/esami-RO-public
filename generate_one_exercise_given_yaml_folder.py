#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import shutil
from distutils.dir_util import copy_tree

import create_exercise_free as mode_free
import create_exercise_verifier as mode_ver
from our_commons import check_active_conda_env

PATH_SINGLE_EXERCISES_FOLDER = os.path.join(os.getcwd(),"folder_guesting_single_compiled_exercises")

def add_graph_utils(path_folder):
    """It adds graph utils
    Parameters:"""
    copy_tree(os.path.join(os.getcwd(),'utils','graph_utils','js'),os.path.join(path_folder,'graph_utils','js'))
    copy_tree(os.path.join(os.getcwd(),'utils','graph_utils','css'),os.path.join(path_folder,'graph_utils','css'))


if __name__ == "__main__":
    check_active_conda_env("ROexam")
    parser=argparse.ArgumentParser(
    description='''Script to generate all possible exercises for a given date, relying on a proper collection folder''',
    epilog="""-------------------""")
    parser.add_argument('exercise_yaml_folder', type=str, default='2020-06-30', help='folder containing the .yaml file for the generation of the exercise')
    args=parser.parse_args()
    
    assert len(sys.argv) == 2
    exercise_yaml_folder = str(sys.argv[1])
    if not os.path.exists(exercise_yaml_folder) or not os.path.isdir(exercise_yaml_folder):
        print(f"Error! I could not find the folder containing the yaml file for the generation of the exercise. Folder not found:\n   {exercise_yaml_folder}")
        exit(1)
    if not os.path.exists(PATH_SINGLE_EXERCISES_FOLDER):
        os.mkdir(PATH_SINGLE_EXERCISES_FOLDER)

    tmp, version = os.path.split(exercise_yaml_folder)
    tmp, type_exe = os.path.split(tmp)
    tmp, collection = os.path.split(tmp)
    
    folder_path_of_the_generated_exercise=os.path.join(PATH_SINGLE_EXERCISES_FOLDER,f"{type_exe}_{collection}_{version}")

    
    if os.path.exists(folder_path_of_the_generated_exercise):
        answer = input(f"The target folder {folder_path_of_the_generated_exercise} already exists! Are you sure you want to erase it, and generate again the folder with all exercises? Enter 'y' or 'Y' if you want me to proceed: ")
        if answer not in ("y", "Y"):
            print("Operation aborted. This call has had no effect.")
            exit(0)
        shutil.rmtree(folder_path_of_the_generated_exercise)
        print(f"I have removed the old folder ({PATH_SINGLE_EXERCISES_FOLDER}). Now building up the new one ...\n")
    os.mkdir(folder_path_of_the_generated_exercise)

    if type_exe in ['graphs_flows_and_cuts', 'graphs_planarity', 'graphs_shortest_paths', 'graphs_min_spanning_trees']:
        add_graph_utils(folder_path_of_the_generated_exercise)
    folder_path_of_the_generated_exercise = os.path.join(folder_path_of_the_generated_exercise,f"istanza_{version}")
    os.mkdir(folder_path_of_the_generated_exercise)

    if type_exe in ['dp_poldo', 'dp_lcs', 'dp_robot_no_gemme', 'dp_triangle', 'dp_knapsack']: # mode_ver
        mode_ver.create_exercise('1999-12-31', '69', folder_path_of_the_generated_exercise, type_exe, os.path.join(exercise_yaml_folder,f"{type_exe}.yaml"))
    else: # mode_free o mode_applet
        mode_free.create_exercise('1999-12-31', '69', folder_path_of_the_generated_exercise, os.path.join(exercise_yaml_folder,f"{type_exe}.yaml"))
    print("\n ...Finished!")
    print(f"The problem has been placed in the folder {folder_path_of_the_generated_exercise}")
