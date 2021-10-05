#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import nbformat as nb
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import re
import shutil
import stat
import subprocess
import sys
import yaml

import create_exercise_free as mode_free

import importlib.util
spec = importlib.util.spec_from_file_location("prob_ver_gen", "problem_types/prob_ver_gen.py")
prob_ver_gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prob_ver_gen)


PATH_UTILS = os.getcwd() + '/utils/'
PATH_VERIFIERS = os.getcwd() + '/utils/verifiers/'

def insert_suppl_folders(path_mode):
    """It inserts all supplementary folders, such as 'allegati'
    Parameters:
    path_mode (str): the path to the current folder where to add the needed subfolders"""
    os.mkdir(path_mode + '/allegati')


def insert_rendition(notebook, notebook_name):
    """It inserts the button to save and export the notebook as an embed_HTML
    Parameters:
    notebook: a Jupyter nb.v4 notebook
    notebook_name (str): the notebook name"""
    button_rend = open(PATH_UTILS + 'preview_HTML.py').read()
    notebook['cells'] += [nb.v4.new_code_cell(button_rend.replace('?FILENAME?', notebook_name))]
    notebook.cells[-1].metadata = {"init_cell": True, "trusted": True, "hide_input": True, "editable": False, "deletable": False, "tags": ['run_start', 'noexport']}
    return

def create_exercise(exam_date, num_exercise, path_ex_folder, exer_type, fullpath_yaml):
    """It creates the new folder with 'mode_ver' (modalità con verificatori)
    Parameters:
    exam_date (str): YYYY-MM-DD
    num_exercise (str): the progressive number (starting from 1, encoded as a string) of the exercise in the exam folder under generation
    path_ex_folder (str): the path of the .ipynb file where to store the exercise to be created
    exer_type (str): the exercise type (e.g., 'dp_poldo')
    fullpath_yaml (str): the fullpath to the yaml instance file to be read and rendered"""
    global images_to_add
    global REL_PATH_IMAGES
    REL_PATH_IMAGES = 'img_' + exam_date
    images_to_add = []
    path_mode_ver = path_ex_folder + '/modo_verif/' # new folder for the considered submission mode
    os.mkdir(path_mode_ver)
    
    notebook_name = 'Esercizio_' + num_exercise + '.ipynb'
    prev_folder = 'esercizio_' + num_exercise

    notebook, yaml_generated = prob_ver_gen.generate_nb(exer_type, fullpath_yaml)
    
    insert_suppl_folders(path_mode_ver) # inserting the "allegati" subfolder
    insert_rendition(notebook, notebook_name) # inserting the button "Salva & Esporta" in the end of the notebook
    nb.write(notebook, notebook_name) # saving the notebook as a .ipynb file
    os.rename(os.getcwd()+ '/' + notebook_name, path_mode_ver + '/' + notebook_name) # assigning the proper name to the notebook
    if 0 != os.system("jupyter trust " + path_mode_ver + notebook_name): # signing the notebook in order to make it trusted
        print("\n\nGot an error when launching the jupyter command! Note: you should start these scripts from an environment where anaconda, or at least jupyther, is included.\n\n")    
    exer_yaml = yaml_generated # yaml instance for the mode free
    mode_free.create_exercise_given_yaml(exam_date, num_exercise, path_ex_folder, exer_yaml) # mode free
    
    # when selecting a mode in the map, the link has to change, in order to point to the correct notebook
    link_ver = 'http://127.0.0.1:8888/notebooks/'+prev_folder+'/modo_verif/' + notebook_name
    link_lib = 'http://127.0.0.1:8888/notebooks/'+prev_folder+'/modo_libero/' + notebook_name
    # adding tags
    if 'tags' in exer_yaml:
        e_dict = {'title':exer_yaml['title'],'tags':exer_yaml['tags'],'tot_points':0,'link':[link_ver,link_lib], 'tasks':exer_yaml['tasks'], 'mode':['Verificatore','Libera']}
    else:
        e_dict = {'title':exer_yaml['title'],'tags':[],'tot_points':0,'link':[link_ver,link_lib], 'tasks':exer_yaml['tasks'], 'mode':['Verificatore','Libera']}

    return e_dict





    
