#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 13:00:37 2020

@authors: Alice Raffaele, Alessandro Busatto, Marco Emporio, Marco Fattorelli, Romeo Rizzi, Aurora Rossi, Francesco Trotti

"""

import argparse
import json
import nbformat as nb
import os
from stat import S_IREAD, S_IRGRP, S_IROTH
import re
import shutil
import sys
import yaml

PATH_UTILS = os.getcwd() + '/utils/'
global REL_PATH_IMAGES # img_YYYY-MM-DD
global images_to_add # if there are images to add in the related folder, store here their filenames

def insert_import_mode_free(note):
    """It imports the proper modules and libraries needed for all notebooks
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_import = open(PATH_UTILS + 'import_mode_free.md', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_import)]
    note.cells[-1].metadata = {"jupyter": {"source_hidden": True}, "init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}

def insert_start_button(note):
    """It inserts the start button
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_start_button = open(PATH_UTILS + 'run_selected_cells.py', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_start_button)]
    note.cells[-1].metadata = {"init_cell": True}

def insert_needed_import(note, exer_name):
    """It inserts other necessaries modules and libraries needed for specific types of exercises
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_import = ''
    if exer_name in ('lp_duality', 'lp_interactive', 'lp_two_phases'):
        txt_interactive = open(PATH_UTILS + 'interactive_simplex_note.md', 'r', encoding='utf-8').read()
        note['cells'] += [nb.v4.new_markdown_cell(txt_interactive)]
        note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False}
        txt_import = open(PATH_UTILS + 'interactive_simplex.py', 'r', encoding='utf-8').read()
    else:
        txt_pulp = open(PATH_UTILS + 'pulp_note.md', 'r', encoding='utf-8').read()
        note['cells'] += [nb.v4.new_markdown_cell(txt_pulp)]
        note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
        txt_import = open(PATH_UTILS + 'import_pulp.md', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_import)]
    note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}

def insert_hide_code(note):
    """It inserts the HTML script to hide the input of code cells
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt = open(PATH_UTILS + 'hide_code.py', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt)]
    note.cells[-1].metadata = {"editable": False, "deletable": False, "tags": ['run_start']}
    return

def read_exercise_yaml(path_yaml):
    """It reads a yaml file and save its content in a dictionary
    Parameters:
    path_yaml (str): the path to the yaml instance"""
    exer_dict = {}
    with open(path_yaml, 'r') as stream:
        try:
            exer_dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return exer_dict

def insert_heading(note, exer_title):
    """It inserts the header and the exercise title
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt = open(PATH_UTILS + 'heading.md', 'r', encoding='utf-8').read()
    content_title = txt.replace('?title?', exer_title)
    note['cells'] += [nb.v4.new_markdown_cell(content_title)]
    note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
    return

def look_for_img(txt):
    """It looks for <img src='...'> in the field description1 and adds the name of the image found in the list images_to_add
    Parameters:
    txt (str): the field description1"""
    global images_to_add
    global REL_PATH_IMAGES
    to_look = "\<img src='" + REL_PATH_IMAGES + "\/(.)*\>"
    match = re.search(r""+to_look, txt)
    if match:
        to_sub = "<img src='" + REL_PATH_IMAGES
        #print(to_sub)
        img = re.sub(to_sub, "", re.search(r""+to_look, txt).group())
        img_name = img.split("'")
        images_to_add += [img_name[0].replace(to_sub, "")]
        #print(images_to_add)
        return 1
    else:
        return 0

def insert_description1(note, exer_descr1, exam_date, path_ex_folder):
    """It adds the description1 to the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    exer_descr1 (str): the content to add
    path_ex_folder (str): the path of the current exercise where the mode has to be added"""
    download_button_lib = open(PATH_UTILS + 'download_button.py', 'r', encoding='utf-8').read()
    img_check = False
    if look_for_img(exer_descr1) == 1:
        exer_descr1 = exer_descr1.replace("img_" + exam_date, "img")

        pattern = re.compile("^esame_RO-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_id")
        absolute_path_dirs_array = path_ex_folder.split('/')
        pos = None
        for i,dir in zip(range(len(absolute_path_dirs_array)), absolute_path_dirs_array):
            if pattern.match(absolute_path_dirs_array[i]):
                pos = i
        assert pos != None
        download_button_lib = download_button_lib.replace('@img_name@',images_to_add[-1]).replace('@path_ex_folder@',".../" + '/'.join(absolute_path_dirs_array[pos:]))

        img_check = True
    #print(exer_descr1)
    note['cells'] += [nb.v4.new_markdown_cell(exer_descr1)]
    note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False}
    if img_check: #adding download button
        note['cells'] += [nb.v4.new_code_cell(download_button_lib)]
        note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False}	
    return

def insert_description2(note, exer_descr2):
    """It adds the description2 to the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    exer_descr2 (str): the content to add"""
    note['cells'] += [nb.v4.new_markdown_cell(exer_descr2)]
    note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False}
    return

def insert_user_bar_lib(note, path_ex_folder):
    """It inserts the Python code to add the user bar needed to answer to each task
    Parameters:
    note (Jupyter nb.v4): the notebook
    path_ex_folder (str): the path of the current exercise where the mode has to be added"""
    user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()

    pattern = re.compile("^esame_RO-[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]_id")
    absolute_path_dirs_array = path_ex_folder.split('/')
    pos = None
    for i,dir in zip(range(len(absolute_path_dirs_array)), absolute_path_dirs_array):
        if pattern.match(absolute_path_dirs_array[i]):
            pos = i
    assert pos != None
    note['cells'] += [nb.v4.new_code_cell(user_bar_lib.replace('@path_ex_folder@',".../" + '/'.join(absolute_path_dirs_array[pos:])))]

    note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
    return

def insert_user_bar_cell(note):
    """It inserts the user bar as a code cell
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
    note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
    note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
    return

def insert_tasks(note, exer_tasks):
    """It inserts all tasks in the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    exer_tasks (dict): the dictionary of tasks"""
    for i in range(len(exer_tasks)):
        task_txt = '__Richiesta ' + str(i+1) + ' \[' + str(exer_tasks[i]['tot_points']) + ' punti\]__: '
        task_txt += exer_tasks[i]['description1']
        note['cells'] += [nb.v4.new_markdown_cell(task_txt)]
        note.cells[-1].metadata = {"init_cell": True, "editable": False, "deletable": False, "tags": ['run_start']}
        insert_user_bar_cell(note)
    return

def insert_suppl_folders(path_mode):
    """It inserts all supplementary folders, such as 'allegati' and 'img' if needed
    Parameters:
    path_mode (str): the path to the current folder where to add the needed subfolders"""
    global REL_PATH_IMAGES
    os.mkdir(path_mode + '/allegati')
    if len(images_to_add) > 0:
        path_ex_images = path_mode + 'img'
        os.mkdir(path_ex_images)
        for img in images_to_add:
            path_img_src = os.getcwd() + '/' + REL_PATH_IMAGES + img
            shutil.copy2(path_img_src, path_ex_images)
            os.chmod(path_ex_images+"/"+img, S_IREAD)

def insert_rendition(note, note_name):
    """It inserts the button to save and export the notebook as an embed_HTML
    Parameters:
    note (Jupyter nb.v4): the notebook
    note_name (str): the notebook name"""
    button_rend = open(PATH_UTILS + 'preview_HTML.py').read()
    note['cells'] += [nb.v4.new_code_cell(button_rend.replace('?FILENAME?', note_name))]
    note.cells[-1].metadata = {"init_cell": True, "tags": ['run_start'], "editable": False, "deletable": False, "tags": ['run_start']}
    return
	
def create_exercise(exam_date, num, path_ex_folder, path_yaml):
    """It creates the new folder with 'free mode' ('modo_libero')
    Parameters:
    exam_date (str): YYYY-MM-DD
    num (str): the progressive number of the exercise in the exam folder
    path_ex_folder (str): the path of the current exercise where the mode has to be added
    path_yaml (str): the path to the yaml instance to read"""
    global images_to_add
    global REL_PATH_IMAGES
    REL_PATH_IMAGES = 'img_' + exam_date
    images_to_add = []
    path_mode_free = path_ex_folder + '/modo_libero/' # new folder for the considered submission mode
    os.mkdir(path_mode_free)
    exer = read_exercise_yaml(path_yaml) # reading the given yaml
    notebook = nb.v4.new_notebook() # creating the new notebook
    insert_import_mode_free(notebook) # required import
    insert_start_button(notebook) # start button to run cells with tag 'run_start'
    insert_hide_code(notebook) # hide all code cells
    insert_user_bar_lib(notebook,path_ex_folder) # insert user_bar.py in a code cell
    insert_heading(notebook, exer['title']) # heading with title
    insert_description1(notebook, exer['description1'], exam_date, path_ex_folder) # description 1
    if 'description2' in exer:
        insert_description2(notebook, exer['description2']) # description 2
    insert_tasks(notebook, exer['tasks']) # inserting the several tasks
    if exer['name'] in ('lp_duality', 'lp_interactive', 'lp_modelling', 'lp_two_phases'): # other libraries needed for some types of exercises
        insert_needed_import(notebook, exer['name'])

    if int(num) >= 10: # writing the notebook and saving it in the correct folder
        note_name = 'Esercizio_' + num + '.ipynb'
        prev_folder = 'esercizio_' + num
    else:
        note_name = 'Esercizio_0' + num + '.ipynb'
        prev_folder = 'esercizio_0' + num
    insert_rendition(notebook, note_name)
    nb.write(notebook, note_name)
    os.rename(os.getcwd()+ '/' + note_name, path_mode_free + '/' + note_name)
    os.system("jupyter trust " + path_mode_free + note_name) # signing the notebook in order to make it trusted
    insert_suppl_folders(path_mode_free) # inserting the supplementary folders (i.e., 'allegati', 'img')
    if 'tags' in exer:
        e_dict = {'title':exer['title'],'tags':exer['tags'],'tot_points':0,'link':'http://127.0.0.1:8888/notebooks/'+prev_folder+'/modo_libero/' + note_name, 'tasks':exer['tasks']}
    else:
	    e_dict = {'title':exer['title'],'tags':[],'tot_points':0,'link':'http://127.0.0.1:8888/notebooks/'+prev_folder+'/modo_libero/' + note_name, 'tasks':exer['tasks']}
    return e_dict

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Script to generate a new exercise solvable with the so called 'free and structured' mode ('modo_libero').
        It receives as inputs the number of the exercise, the path of the exercise folder where to add the free mode subfolder and the
        path of the .yaml instance containing the exercise itself.''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    parser.add_argument('num', type=str, default=1, help='progressive number of the exercise in the exam')
    parser.add_argument('path', type=str, default=os.getcwd()+'/shuttle/esame_RO-2020-06-30_VR123456/esercizio_1/', help='path to the exercise folder where to add the subfolder ''modo_libero'' ')
    parser.add_argument('yaml_instance', type=str, default=os.getcwd()+'/collection_2020-06-30/graphs_trees/graphs_trees0.yaml', help='path to the yaml instance to code as exercise')
    args=parser.parse_args()

    assert len(sys.argv) == 5
    exam_date = str(sys.argv[1])
    num = str(sys.argv[2])
    path = str(sys.argv[3])
    yaml_file = str(sys.argv[4])
    create_exercise(exam_date, num, path, yaml_file)
