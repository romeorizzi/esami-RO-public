#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:00:55 2020

@authors:
Verifiers: Alessandro Busatto, Paolo Graziani, Aurora Rossi, Davide Roznowicz;
Applet: Giacomo Di Maggio, Marco Emporio, Marco Fattorelli, Sebastiano Gaiardelli, Francesco Trotti;
Map: Rosario Di Matteo, Marco Emporio, Adriano Tumminelli;
OneDrive: Marco Fattorelli, Davide Roznowicz;
Integration: Alice Raffaele, Romeo Rizzi.

"""

import argparse
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
import dp_poldo_generator as dp_poldo
import dp_lcs_generator as dp_lcs
import dp_robot_no_gemme_generator as dp_robot_no_gemme
import dp_triangle_generator as dp_triangle
import dp_knapsack_generator as dp_knapsack
import create_exercise_free as mode_free

PATH_UTILS = os.getcwd() + '/utils/'
PATH_VERIFIERS = os.getcwd() + '/utils/verifiers/'

def insert_suppl_folders(path_mode):
    """It inserts all supplementary folders, such as 'allegati'
    Parameters:
    path_mode (str): the path to the current folder where to add the needed subfolders"""
    os.mkdir(path_mode + '/allegati')


def insert_rendition(note, note_name):
    """It inserts the button to save and export the notebook as an embed_HTML
    Parameters:
    note (Jupyter nb.v4): the notebook
    note_name (str): the notebook name"""
    button_rend = open(PATH_UTILS + 'preview_HTML.py').read()
    note['cells'] += [nb.v4.new_code_cell(button_rend.replace('?FILENAME?', note_name))]
    note.cells[-1].metadata = {"init_cell": True, "trusted": True, "hide_input": True, "editable": False, "deletable": False, "tags": ['run_start', 'noexport']}
    return

def create_exercise(exam_date, num, path_ex_folder, ex_type, path_yaml, path_almost_yaml):
    """It creates the new folder with 'mode_ver' (modalità con verificatori)
    Parameters:
    exam_date (str): YYYY-MM-DD
    num (str): the progressive number of the exercise in the exam folder
    path_ex_folder (str): the path of the current exercise where the mode has to be added
    ex_type (str): the exercise type (e.g., 'dp_poldo')
    path_yaml (str): the path to the yaml instance to read"""
    global images_to_add
    global REL_PATH_IMAGES
    REL_PATH_IMAGES = 'img_' + exam_date
    images_to_add = []
    path_mode_ver = path_ex_folder + '/modo_verif/' # new folder for the considered submission mode
    os.mkdir(path_mode_ver)
    instance_free = path_almost_yaml + '_free.yaml'
    
    if int(num) >= 10: # writing the notebook and saving it in the correct folder
        note_name = 'Esercizio_' + num + '.ipynb'
        prev_folder = 'esercizio_' + num
    else:
        note_name = 'Esercizio_0' + num + '.ipynb'
        prev_folder = 'esercizio_0' + num
        
    if ex_type == 'dp_poldo':
        note, yaml_gen = dp_poldo.generate_nb(path_yaml)
    elif ex_type == 'dp_lcs':
        note, yaml_gen = dp_lcs.generate_nb(path_yaml)
    elif ex_type == 'dp_robot_no_gemme':
        note, yaml_gen = dp_robot_no_gemme.generate_nb(path_yaml)
    elif ex_type == 'dp_triangle': 
        note, yaml_gen = dp_triangle.generate_nb(path_yaml)
    else: # ex_type == 'dp_knapsack': (TO DO: add other dynamic programming exercises here)
        note, yaml_gen = dp_knapsack.generate_nb(path_yaml)
    
    insert_suppl_folders(path_mode_ver) # inserting the "allegati" subfolder
    insert_rendition(note, note_name) # inserting the button "Salva & Esporta" in the end of the notebook
    nb.write(note, note_name) # saving the notebook as a .ipynb file
    os.rename(os.getcwd()+ '/' + note_name, path_mode_ver + '/' + note_name) # assigning the proper name to the notebook
    os.system("jupyter trust " + path_mode_ver + note_name) # signing the notebook in order to make it trusted
    
    exer = yaml_gen # yaml instance for the mode free
    mode_free.create_exercise_given_yaml(exam_date, num, path_ex_folder, exer) # mode free
    
    # when selecting a mode in the map, the link has to change, in order to point to the correct notebook
    link_ver = 'http://127.0.0.1:8888/notebooks/'+prev_folder+'/modo_verif/' + note_name
    link_lib = 'http://127.0.0.1:8888/notebooks/'+prev_folder+'/modo_libero/' + note_name
    # adding tags
    if 'tags' in exer:
        e_dict = {'title':exer['title'],'tags':exer['tags'],'tot_points':0,'link':[link_ver,link_lib], 'tasks':exer['tasks'], 'mode':['Verificatore','Libera']}
    else:
	    e_dict = {'title':exer['title'],'tags':[],'tot_points':0,'link':[link_ver,link_lib], 'tasks':exer['tasks'], 'mode':['Verificatore','Libera']}

    return e_dict





    