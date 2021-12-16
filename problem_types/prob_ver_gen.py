#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import OrderedDict
import nbformat as nb
import re
import os
from sys import argv, exit, stderr
import yaml
import argparse

import sys
import os.path
if os.path.exists(f"./problem_types"):
    sys.path.extend([f'./problem_types/{name}' for name in os.listdir("./problem_types") if os.path.isdir(f"./problem_types/{name}") and os.path.exists(f"./problem_types/{name}/{name}_generator.py")])
else:
    sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name) and os.path.exists(f"{name}/{name}_generator.py")])

PATH_UTILS = os.getcwd() + '/utils/'
    
import dp_lcs_generator as dp_lcs
import dp_poldo_generator as dp_poldo
import dp_knapsack_generator as dp_knapsack
import dp_robot_no_gemme_generator as dp_robot_no_gemme
import dp_triangle_generator as dp_triangle


def insert_rendition(notebook, notebook_name):
    """It inserts the button to save and export the notebook as an embed_HTML
    Parameters:
    notebook: a Jupyter nb.v4 notebook
    notebook_name (str): the notebook name"""
    button_rend = open(PATH_UTILS + 'preview_HTML.py').read()
    notebook['cells'] += [nb.v4.new_code_cell(button_rend.replace('?FILENAME?', notebook_name))]
    notebook.cells[-1].metadata = {"init_cell": True, "trusted": True, "hide_input": True, "editable": False, "deletable": False, "tags": ['run_start', 'noexport']}
    return

def generate_nb(problem_type, fullpath_yaml):
    if problem_type == 'dp_poldo':
        return dp_poldo.generate_nb(fullpath_yaml)
    elif problem_type == 'dp_lcs':
        return dp_lcs.generate_nb(fullpath_yaml)
    elif problem_type == 'dp_robot_no_gemme':
        return dp_robot_no_gemme.generate_nb(fullpath_yaml)
    elif problem_type == 'dp_triangle': 
        return dp_triangle.generate_nb(fullpath_yaml)
    elif problem_type == 'dp_knapsack':
        return dp_knapsack.generate_nb(fullpath_yaml)
    else: #(TO DO: insert here other problem types with verifiers)
        print("Error! Unsupported problem type")
        exit(1)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''Generates an .ipynb file (notebook) for an exercise with verifiers of type <prob_ver_type> starting from the <yaml_file_fullname> that contains the instance specific data for customization of the exercise.''',
    epilog="""-------------------""")
    parser.add_argument('problem_type', type=str, default='dp_lcs', help='the string (the name of the problem type and of the immidiate subfolder of the folder guesting this script that implements that problem type')
    parser.add_argument('yaml_file_fullname', type=str, default='problem_instance.yaml', help='the fullname of the .yaml file containing the instance specific data for customization')
    parser.add_argument('notebook_fullname', type=str, default='problem_instance.ipynb', help='the fullname of the .ipynb file to be generated')
    args=parser.parse_args()

    problem_type = str(argv[1])
    yaml_file_fullname = str(argv[2])
    notebook_fullname = str(argv[3])
        
    notebook, yaml_gen = generate_nb(problem_type, yaml_file_fullname)
    
    insert_rendition(notebook, notebook_fullname) # inserting the button "Salva & Esporta" in the end of the notebook
    nb.write(notebook, notebook_fullname) # saving the notebook as a .ipynb file
    if 0 != os.system("jupyter trust " + notebook_fullname): # signing the notebook in order to make it trusted
        print("\n\nGot an error when launching the jupyter command! Note: you should start these scripts from an environment where anaconda, or at least jupyter, is included.\n\n")    
