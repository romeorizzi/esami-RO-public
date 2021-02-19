#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:45:29 2020

@authors: Alice Raffaele, Alessandro Busatto, Marco Emporio, Marco Fattorelli, Romeo Rizzi, Aurora Rossi, Francesco Trotti

"""

import argparse
import create_exercise_free as mode_free
import create_exercise_verifier as mode_ver
import map_generator
from distutils.dir_util import copy_tree
import csv
import errno
import glob
import hashlib
import os
import shutil
import sys
import tarfile
import zipfile

NB_EXERCISES = 10
RO_EXAM = 'esame_RO-'
REL_SHUTTLE_FOLDER = '/shuttle/'
REL_UTILS_FOLDER = '/utils/'
UPLOAD_INSTRUCTIONS = '/info_upload/ISTRUZIONI_RICONSEGNA.pdf'
START_INSTRUCTIONS = '/info_start/ISTRUZIONI_AVVIO.pdf'
TROUBLESHOOTING = 'troubleshooting/TROUBLESHOOTING.pdf'
COLLECTION_FOLDER = '/collections/'

def extract_ex(exam_date, stud):
    """It computes an hash starting from the string stud+exam_date, keeping only digits
    Parameters:
    exam_date (str): YYYY-MM-DD
    stud (str): student ID
    Returns:
    a list of integers"""
    h = hashlib.md5((stud+exam_date).encode('utf-8')).hexdigest()
    chosen_ex = [int(s) for s in h if s.isdigit() and int(s) != 0]
    assert len(chosen_ex) >= NB_EXERCISES # check there are enough digits in the returned list
    return chosen_ex

def add_main_folder(archives_name):
    """It adds the folder related to the current student
    Parameters:
    archives_name (str): the final student's folder
    Returns:
    int: 1 if the folder has been created from new and exercises need to be added; 0 if there is no need to proceed"""
    global absolute_path_student
    print("Creating the main folder " + absolute_path_student + "...")
    folder_student = os.getcwd() + REL_SHUTTLE_FOLDER + archives_name
    if os.path.exists(folder_student):
        answer = None # if the exam has been already created for given student and date, ask if re-write it or not
        while answer not in ("y", "n"):
            answer = input("Do you want to generate again the exam? Enter 'y' or 'n': ")
            if answer == "y": # it empties the folder absolute_path_student
                for root, dirs, files in os.walk(folder_student, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(folder_student)
                os.mkdir(absolute_path_student)
                return 1
            elif answer == "n":
                return 0
            else:
                print("Please enter 'yes' or 'no'")
    os.mkdir(absolute_path_student)
    return 1

def add_exercises(exam_date, path_exercises, ex_list):
    """It adds the exercises extracted to the student folder
    Parameters:
    exam_date (str): YYYY-MM-DD
    path_exercises (str): where to find the collection of exercises
    ex_list (list of integers): extracted exercises
    Returns:
    info_exer_map (list of str): for each exercise, its proper title to insert in the map"""
    global absolute_path_student
    info_exer_map = []
    type_list = [x for x in sorted(os.listdir(path_exercises)) if '.DS_Store' not in x]
    for i in range(len(type_list)):
        path_type = path_exercises + '/' + type_list[i]
        print(path_type)
        nb_ex_type = len(glob.glob(os.path.join(path_type, '*'))) # there must be at least one exercise for each type
        assert nb_ex_type > 0
        chosen = ex_list[i]
        if nb_ex_type == 1:
            chosen = 0
        else:
            chosen = ex_list[i] % nb_ex_type
        path_full_yaml = path_type + '/' + type_list[i] + str(chosen) + '.yaml'
        path_almost_yaml = path_type + '/' + type_list[i] + str(chosen) # (misses '.yaml')
        if i>=9:
            path_ex = absolute_path_student + '/esercizio_' + str(i+1)
        else:
            path_ex = absolute_path_student + '/esercizio_0' + str(i+1)
        os.mkdir(path_ex)
        if type_list[i] in ['dp_poldo', 'dp_lcs', 'dp_robot_no_gemme', 'dp_triangle', 'dp_knapsack']: # mode_ver
            info_exer_map += [mode_ver.create_exercise(exam_date, str(i+1), path_ex, type_list[i], path_full_yaml, path_almost_yaml)]
        else: # mode_free o mode_applet
            info_exer_map += [mode_free.create_exercise(exam_date, str(i+1), path_ex, path_full_yaml)] # it calls the script that actually creates the exercise folder and notebook

        print('Exercise ' + str(i+1) + ' added')
    return info_exer_map

def add_map(exam_date, matricola, info_map, name, surname):
    """It creates the index map
    Parameters:
    date (str): YYYY-MM-DD
    matricola (str): e.g., VR123456
    info_map (list of str): for each exercises, its proper title to insert in the map
    name (str): students''s name
    surname (str): students''s surname"""
    global absolute_path_student
    shutil.copy('./avvia_esame.py', absolute_path_student) #to do: activate conda env in avvia_esame.py
    to_render = map_generator.generate(exam_date, info_map)
    copy_tree('./map',absolute_path_student+'/map')
    f = open(absolute_path_student + '/map/' + 'index.html','w')
    f.write(to_render)
    f.close()

def add_graph_utils():
    """It adds graph utils
    Parameters:"""
    global absolute_path_student
    copy_tree('./utils/graph_utils/js',absolute_path_student+'/graph_utils/js')
    copy_tree('./utils/graph_utils/css',absolute_path_student+'/graph_utils/css')

def add_info():
    """It adds three useful files to the folder, copying them from utils folder"""
    global absolute_path_student
    PATH_UTILS = os.getcwd() + REL_UTILS_FOLDER
    info_upload_src = PATH_UTILS + UPLOAD_INSTRUCTIONS
    info_start_src = PATH_UTILS + START_INSTRUCTIONS
    info_troubleshooting_src = PATH_UTILS + TROUBLESHOOTING
    shutil.copy(info_start_src, absolute_path_student)
    shutil.copy(info_upload_src, absolute_path_student)
    shutil.copy(info_troubleshooting_src, absolute_path_student)

def create_archives(student_anchored_folder, student_local_folder, also_uncompressed):
    """It creates .tgz and .zip files of the students's folder
    Parameters:
    student_anchored_folder (str): the name to be give to the folder for the download from the student
    student_local_folder (str): the name of the student's local exam folder
    """
    global absolute_path_student
    current = os.getcwd()
    os.chdir(current + REL_SHUTTLE_FOLDER)
    os.mkdir(student_anchored_folder)
    command_zip = 'zip -r ' + student_local_folder + '.zip ' + student_local_folder
    command_tar = "tar -cvzf " + student_local_folder + ".tgz " + student_local_folder
    risp = os.system(command_zip)
    print("Zip created ({student_local_folder + '.zip'})")
    risp = os.system(command_tar)
    print("Tar created ({student_local_folder + '.tgz'})")
    shutil.move(student_local_folder + '.zip', student_anchored_folder + '/')
    shutil.move(student_local_folder + '.tgz', student_anchored_folder + '/')
    if also_uncompressed:
        shutil.move(student_local_folder, student_anchored_folder + '/')
    else:
        try:
            shutil.rmtree(student_local_folder)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (student_local_folder, e))
    os.chdir(current)

def gen_exam(exam_date, anchor, student_ID, matricola, name, surname, also_uncompressed = False):
    """Main procedure that generate the exam for the given student.
    It can also be called by generate_all_exams_given_list.py
    Parameters:
    exam_date (str): exam date according to the format YYYY-MM-DD
    anchor (str): random string to use in the student's folder name
    student_ID (str): unique ID associated to a student
    matricola (str): badge number associated to a student
    name (str): student's name
    surname (str): student's surname
    Returns:
    ex_list[:NB_EXERCISES] (list of integers): indexes of the instances assigned to the student, useful to compose a .csv that summarizes, for each student, its exercises
    """
    global absolute_path_student
    student_local_folder = RO_EXAM + exam_date + '_' + student_ID
    student_anchored_folder = RO_EXAM + exam_date + '_' + anchor + '_' + student_ID
    if os.path.exists(os.getcwd() + REL_SHUTTLE_FOLDER) == False:
        os.mkdir(os.getcwd() + REL_SHUTTLE_FOLDER)
    absolute_path_student = os.getcwd() + REL_SHUTTLE_FOLDER + student_local_folder # path folder to create
    ex_list = extract_ex(exam_date, matricola) # list of exercises to extract from collection
    keep_going = add_main_folder(student_anchored_folder) # if absolute_path_student already exists, ask if re-generating it or not
    if keep_going == 0:
        print("The exam (" + exam_date + ', ' + student_ID + ") has been already generated")
    else:
        print("\nNew generation of the exam (" + exam_date + ', ' + student_ID + ") started\nAdding exercises...")
        path_exercises = os.getcwd() + COLLECTION_FOLDER + "RO-" + exam_date
        info_exer_map = add_exercises(exam_date, path_exercises, ex_list)
        add_graph_utils()
        add_map(exam_date, matricola, info_exer_map, name, surname) # from the exercises created, it generates the map

        print("\nAdding the map...")
        #add_info()
        add_graph_utils()
        print("\n Adding graph utils")
        create_archives(student_anchored_folder, student_local_folder, also_uncompressed)
        print("\nGeneration of the exam (" + exam_date + ', ' + student_ID + ") completed")
    return ex_list[:NB_EXERCISES]

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Script to generate a new exam for the course of Ricerca Operativa (UniVR).
        It receives as input the exam date and the student data (ID, badge number, name and surname),
        which will be used to compute an hash in order to generate a pseudocasual exam
        (reconstrunctable in the future exactly as it is). ''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date according to the format YYYY-MM-DD')
    parser.add_argument('s', type=str, default='kdjbvbile', help='random string to use in the students''s folder name')
    parser.add_argument('student_ID', type=str, default='id123456', help='unique ID associated to a student')
    parser.add_argument('matricola', type=str, default='VR123456', help='badge number associated to a student')
    parser.add_argument('name', type=str, default='Pinco', help='student''s name')
    parser.add_argument('surname', type=str, default='Pallino', help='student''s surname')
    parser.add_argument("--with_uncompressed_folder", help="the generated anchored folder will contain also the uncompressed folder",
                    action="store_true")
    args = parser.parse_args()
    if args.with_uncompressed_folder:
        assert len(sys.argv) == 8
        print("The generated anchored folder will contain also the uncompressed folder.")
    else:
        assert len(sys.argv) == 7
    exam_date = str(sys.argv[1])
    anchor = str(sys.argv[2])
    student_ID = str(sys.argv[3])
    matricola = str(sys.argv[4])
    name = str(sys.argv[5])
    surname = str(sys.argv[6])
    gen_exam(exam_date, anchor, student_ID, matricola, name, surname, args.with_uncompressed_folder)
