#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from sys import argv, exit, stderr
import yaml
import re
from collections import OrderedDict

import nbformat as nb
from tabulate import tabulate

PATH_UTILS = os.getcwd() + '/utils/'


def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()

def add_cell(notebookbook, cell_type,data,metadata):
    """ It adds a new cell (with the given type, text and metadata) to the notebookbook notebookbook 
    """
    if cell_type=="Code":
        notebookbook['cells'].append(nb.v4.new_code_cell(data,metadata=metadata));
    elif cell_type=="Markdown":
        notebookbook['cells'].append(nb.v4.new_markdown_cell(data,metadata=metadata));
    elif cell_type=="Raw":
        notebookbook['cells'].append(nb.v4.new_raw_cell(data,metadata=metadata));
    else:
        assert False

def read_exercise_yaml(fullpath_yaml):
    """It reads a yaml file and save its content in a dictionary
    Parameters:
    fullpath_yaml (str): the path to the yaml instance"""
    exer_dict = {}
    with open(fullpath_yaml, 'r') as stream:
        try:
            exer_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)
    return exer_dict

def insert_import_mode_free(notebookbook, run_cells=True):
    """It imports the proper modules and libraries needed for all notebookbooks
    Parameters:
    notebookbook: a Jupyter nb.v4 notebookbook"""
    txt_import = open(PATH_UTILS + 'import_mode_free.md', 'r', encoding='utf-8').read()
    notebookbook['cells'] += [nb.v4.new_code_cell(txt_import)]
    notebookbook.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags":['run_start','noexport'] if run_cells else ['noexport']}

def insert_heading(notebookbook, exer_title, run_cells=True):
    """It inserts the header and the exercise title
    Parameters:
    notebookbook: a Jupyter nb.v4 notebookbook"""
    txt = open(PATH_UTILS + 'heading.md', 'r', encoding='utf-8').read()
    content_title = txt.replace('?title?', exer_title)
    notebookbook['cells'] += [nb.v4.new_markdown_cell(content_title)]
    notebookbook.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start'] if run_cells else []}
    
    #notebookbook['cells'] += [nb.v4.new_markdown_cell('<b>NOTA</b>: qui sotto sono riportate alcune celle di codice con import necessari al funzionamento dei verificatori; ignorali pure. Clicca su "Avvio esercizio" e poi vai pure oltre la barra nera, per svolgere le richieste.')]
    #notebookbook.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
    
def insert_n_tasks(notebookbook, n_tasks, run_cells=True):    
    text_import = """\
    from tabulate import tabulate
    import copy
    n_tasks = """ + str(n_tasks) + """;
    arr_point = [-1] * n_tasks;"""
    notebookbook['cells'] += [nb.v4.new_code_cell(text_import)]
    notebookbook.cells[-1].metadata = {"hide_input": True, "trusted":True, "init_cell": True, "editable": False, "deletable": False, "tags":['run_start','noexport'] if run_cells else ['noexport']}
# Nota: nel caso di knapsack il campo "editable" non era specificato, ho assunto fosse una dimenticanza        
# Nota: nel caso di poldo il campo "editable" e "deletable" non erano specificati, ho assunto fosse una dimenticanza        
# Nota: nel caso di triangle il campo "editable" e "deletable" non erano specificati, ho assunto fosse una dimenticanza        

def insert_user_bar_lib(notebookbook, run_cells=True):#, path_ex_folder):
    """It inserts the Python code to add the user bar needed to answer to each task
    Parameters:
    notebookbook: a Jupyter nb.v4 notebookbook
    path_ex_folder (str): the path of the current exercise where the mode has to be added"""
    user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
    notebookbook['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
    notebookbook.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport'] if run_cells else ['noexport']}

# def insert_user_bar_cell(notebookbook, run_cells=True):
#     """It inserts the user bar as a code cell
#     Parameters:
#     notebookbook: a Jupyter nb.v4 notebookbook"""
#     user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
#     notebookbook['cells'] += [nb.v4.new_code_cell(user_bar_call)]
#     if run_cells:
#         notebookbook.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start','noexport']}
#     else:
#         notebookbook.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport']}
#     return


# def insert_separator_bar(notebookbook):
#     content = '<h1>_______________________________________________________________________________________ </h1>'
#     notebookbook['cells'] += [nb.v4.new_markdown_cell(content)]
#     notebookbook.cells[-1].metadata = {"hide_input": True, "trusted": True, "init_cell": True, "editable": False, "deletable": False, "tags": ['noexport']}
#     return
