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
from graph_utils import parser
import yaml

PATH_UTILS = os.getcwd() + '/utils/'
PATH_GRAPH_UTILS = os.getcwd() + '/utils/graph_utils/'
global REL_PATH_IMAGES # img-YYYY-MM-DD
global images_to_add # if there are images to add in the related folder, store here their filenames

def insert_import_mode_free(note):
    """It imports the proper modules and libraries needed for all notebooks
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_import = open(PATH_UTILS + 'import_mode_free.md', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_import)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags":["noexport"]}

def insert_task_buttons(note,i):
    """It inserts 'Avvia task', 'Carica ultima configurazione' e 'Reset task'
    Parameters:
    note (Jupyter nb.v4): the notebook
    i: index of task"""
    txt_start_button = open(PATH_GRAPH_UTILS + 'init_buttons.py', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_start_button.replace('$i$',i))]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "tags":["noexport"]}

def insert_needed_import(note, exer_name):
    """It inserts other necessaries modules and libraries needed for specific types of exercises
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_import = ''
    if exer_name in ('lp_duality', 'lp_interactive', 'lp_two_phases'):
        txt_interactive = open(PATH_UTILS + 'interactive_simplex_note.md', 'r', encoding='utf-8').read()
        note['cells'] += [nb.v4.new_markdown_cell(txt_interactive)]
        note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags":["noexport"]}
        txt_import = open(PATH_UTILS + 'interactive_simplex.py', 'r', encoding='utf-8').read()
    else:
        txt_pulp = open(PATH_UTILS + 'pulp_note.md', 'r', encoding='utf-8').read()
        note['cells'] += [nb.v4.new_markdown_cell(txt_pulp)]
        note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags":["noexport"]}
        txt_import = open(PATH_UTILS + 'import_pulp.md', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_import)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags":["noexport"]}

def insert_graph_import(note):
    """It inserts all necessaries modules and libraries needed for graph exercises
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    txt_import = open(PATH_GRAPH_UTILS + 'graph_applet_import.py', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(txt_import)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}

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
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False}
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
        exer_descr1 = exer_descr1.replace("img-" + exam_date, "img")

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
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False}
    if img_check: #adding download button
        note['cells'] += [nb.v4.new_code_cell(download_button_lib)]
        note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False}
    return

def insert_description2(note, exer_descr2):
    """It adds the description2 to the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    exer_descr2 (str): the content to add"""
    note['cells'] += [nb.v4.new_markdown_cell(exer_descr2)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False}
    return

def insert_user_bar_lib(note):#, path_ex_folder):
    """It inserts the Python code to add the user bar needed to answer to each task
    Parameters:
    note (Jupyter nb.v4): the notebook
    path_ex_folder (str): the path of the current exercise where the mode has to be added"""
    user_bar_lib = open(PATH_UTILS + 'user_bar.py', 'r', encoding='utf-8').read()
    note['cells'] += [nb.v4.new_code_cell(user_bar_lib)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    return

def insert_user_bar_cell(note):
    """It inserts the user bar as a code cell
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    user_bar_call = open(PATH_UTILS + 'user_bar_call.md').read()
    note['cells'] += [nb.v4.new_code_cell(user_bar_call)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    return

def insert_single_task(note,task,i):
    """It inserts single task in the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    task (dict): the dictionary of task
	i (int): index of task"""
    task_txt = '__Richiesta ' + str(i+1) + ' \[' + str(task['tot_points']) + ' punti\]__: '
    task_txt += task['description1']
    note['cells'] += [nb.v4.new_markdown_cell(task_txt)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False}
    insert_user_bar_cell(note)
    return

def insert_single_graph_task(note,task,i):
    """It inserts single graph task in the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    task (dict): the dictionary of task
	i (int): index of task"""
    task_txt = '__Richiesta ' + str(i+1) + ' \[' + str(task['tot_points']) + ' punti\]__: '
    task_txt += task['description1']
    note['cells'] += [nb.v4.new_markdown_cell(task_txt)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False}
    insert_task_buttons(note,str(i+1))
    task_graph = get_graph_data(task['graphml'],str(i+1))
    note['cells'] += [nb.v4.new_code_cell(task_graph)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    config_check = open(PATH_GRAPH_UTILS + 'config_check.py').read()
    note['cells'] += [nb.v4.new_code_cell(config_check.replace('$i$',str(i+1)))]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    display_graph = open(PATH_GRAPH_UTILS + 'display.py').read().replace('$i$',str(i+1))
    note['cells'] += [nb.v4.new_code_cell(display_graph)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    insert_user_bar_cell(note)
    return

def insert_tasks(note, exer_tasks):
    """It inserts all tasks in the notebook
    Parameters:
    note (Jupyter nb.v4): the notebook
    exer_tasks (dict): the dictionary of tasks"""
    for i in range(len(exer_tasks)):
        if 'graphml' in exer_tasks[i]:
            insert_single_graph_task(note,exer_tasks[i],i)
        else:
            insert_single_task(note,exer_tasks[i],i)
    return

def get_graph_data(graphml,i):
    """It inserts graph dictionary (after calling the graphml parser) in the notebook
    Parameters:
    graphml: path of graphml
    i: index of task"""
    html_button = open(PATH_GRAPH_UTILS + 'buttons.html').read()
    g = parser(graphml)
    return f"""
    graph_data{i} = {g[0]}
    friends_e{i} = {g[1]}
    friends_n{i} = {g[2]}
    center{i} = {g[3]}
    html_text{i} = '''{html_button.replace('$n$', i)}'''
    """

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

def insert_graph_folder(path_mode):
    """It inserts check-points folder for graph exercise
    Parameters:
    path_mode (str): the path to the current folder where to add the needed subfolders"""
    os.mkdir(path_mode + 'allegati/ck_points')

def insert_rendition(note, note_name):
    """It inserts the button to save and export the notebook as an embed_HTML
    Parameters:
    note (Jupyter nb.v4): the notebook
    note_name (str): the notebook name"""
    button_rend = open(PATH_UTILS + 'preview_HTML.py').read()
    note['cells'] += [nb.v4.new_code_cell(button_rend.replace('?FILENAME?', note_name))]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}
    return

def insert_no_scroll(note):
    """It inserts javascript code to avoid scroll down of output div (for graph)
    Parameters:
    note (Jupyter nb.v4): the notebook"""
    no_scroll = open(PATH_GRAPH_UTILS + 'no_scroll.py').read()
    note['cells'] += [nb.v4.new_code_cell(no_scroll)]
    note.cells[-1].metadata = {"init_cell": True, "hide_input": True, "trusted": True, "editable": False, "deletable": False, "tags": ["noexport"]}

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
    exer = read_exercise_yaml(path_yaml) # reading the given yaml
    if exer['name'] in ('graphs_flows_and_cuts', 'graphs_min_spanning_trees', 'graphs_shortest_paths', 'graphs_planarity'):
        mode_subpath = '/modo_applet/'
        mode = 'Applet'
    else:
        mode_subpath = '/modo_libero/'
        mode = 'Libera'
    PATH_MODE_FULL = path_ex_folder + mode_subpath # new folder for the considered submission mode
    os.mkdir(PATH_MODE_FULL)
    notebook = nb.v4.new_notebook() # creating the new notebook
    #print(exer['name'])
    if mode == 'Applet':
        insert_graph_import(notebook) #required graph import
        insert_no_scroll(notebook) #no scroll of output div
    else:
        insert_import_mode_free(notebook) # required import

    insert_user_bar_lib(notebook)#path_ex_folder) # insert user_bar.py in a code cell
    insert_heading(notebook, exer['title']) # heading with title
    if 'description1' in exer:
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
    os.rename(os.getcwd()+ '/' + note_name, PATH_MODE_FULL + '/' + note_name)
    os.system("jupyter trust " + PATH_MODE_FULL + note_name) # signing the notebook in order to make it trusted
    insert_suppl_folders(PATH_MODE_FULL) # inserting the supplementary folders (i.e., 'allegati', 'img')
    if mode == 'Applet':
        insert_graph_folder(PATH_MODE_FULL)
    if 'tags' in exer:
        e_dict = {'title':exer['title'],'tags':exer['tags'],'tot_points':0,'link':['http://127.0.0.1:8888/notebooks/'+prev_folder + mode_subpath + note_name], 'tasks':exer['tasks'], 'mode':[mode]}
    else:
        e_dict = {'title':exer['title'],'tags':[],'tot_points':0,'link':['http://127.0.0.1:8888/notebooks/'+prev_folder + mode_subpath + note_name], 'tasks':exer['tasks'], 'mode':[mode]}
    return e_dict

def create_exercise_given_yaml(exam_date, num, path_ex_folder, exer):
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
    if exer['name'] in ('graphs_flows_and_cuts', 'graphs_min_spanning_trees', 'graphs_shortest_paths', 'graphs_planarity'):
        mode_subpath = '/modo_applet/'
        mode = 'Applet'
    else:
        mode_subpath = '/modo_libero/'
        mode = 'Libera'
    PATH_MODE_FULL = path_ex_folder + mode_subpath # new folder for the considered submission mode
    os.mkdir(PATH_MODE_FULL)
    notebook = nb.v4.new_notebook() # creating the new notebook
    #print(exer['name'])
    if mode == 'Applet':
        insert_graph_import(notebook) #required graph import
        insert_no_scroll(notebook) #no scroll of output div
    else:
        insert_import_mode_free(notebook) # required import

    insert_user_bar_lib(notebook)#path_ex_folder) # insert user_bar.py in a code cell
    insert_heading(notebook, exer['title']) # heading with title
    if 'description1' in exer:
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
    os.rename(os.getcwd()+ '/' + note_name, PATH_MODE_FULL + '/' + note_name)
    os.system("jupyter trust " + PATH_MODE_FULL + note_name) # signing the notebook in order to make it trusted
    insert_suppl_folders(PATH_MODE_FULL) # inserting the supplementary folders (i.e., 'allegati', 'img')
    if mode == 'Applet':
        insert_graph_folder(PATH_MODE_FULL)
    # if 'tags' in exer:
    #     e_dict = {'title':exer['title'],'tags':exer['tags'],'tot_points':0,'link':['http://127.0.0.1:8888/notebooks/'+prev_folder + mode_subpath + note_name], 'tasks':exer['tasks'], 'mode':[mode]}
    # else:
    #     e_dict = {'title':exer['title'],'tags':[],'tot_points':0,'link':['http://127.0.0.1:8888/notebooks/'+prev_folder + mode_subpath + note_name], 'tasks':exer['tasks'], 'mode':[mode]}
    # return e_dict

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Script to generate a new exercise solvable with the so called 'free and structured' mode ('modo_libero').
        It receives as inputs the number of the exercise, the path of the exercise folder where to add the free mode subfolder and the
        path of the .yaml instance containing the exercise itself.''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
    parser.add_argument('num', type=str, default=1, help='progressive number of the exercise in the exam')
    parser.add_argument('path', type=str, default=os.getcwd()+'/shuttle/esame_RO-2020-06-30_VR123456/esercizio_1/', help='path to the exercise folder where to add the subfolder ''modo_libero'' ')
    parser.add_argument('yaml_instance', type=str, default=os.getcwd()+'/collections/RO-2020-06-30/graphs_trees/graphs_trees0.yaml', help='path to the yaml instance to code as exercise')
    args=parser.parse_args()

    assert len(sys.argv) == 5
    exam_date = str(sys.argv[1])
    num = str(sys.argv[2])
    path = str(sys.argv[3])
    yaml_file = str(sys.argv[4])
    create_exercise(exam_date, num, path, yaml_file)
