#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 10:45:29 2020

@authors: Alice Raffaele, Alessandro Busatto, Marco Emporio, Marco Fattorelli, Romeo Rizzi, Aurora Rossi, Francesco Trotti

"""

import argparse
import create_exercise_free as mode1
import create_exercise_verifier as mode2
import create_exercise_applet as mode3
import map_generator
from distutils.dir_util import copy_tree
import csv
import errno
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
COLLECTION_FOLDER = '/collection_'

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
    type_list = [x for x in os.listdir(path_exercises) if '.DS_Store' not in x]
    for i in range(len(type_list)):
        path_type = path_exercises + '/' + type_list[i]
        nb_ex_type = len(os.listdir(path_type)) # there must be at least one exercise for each type
        ex_list[i] = ex_list[i] % nb_ex_type
        chosen_type_yaml = path_type + '/' + type_list[i] + str(ex_list[i] % nb_ex_type) + '.yaml'
        if i>=9:
            path_ex = absolute_path_student + '/esercizio_' + str(i+1)
        else:
            path_ex = absolute_path_student + '/esercizio_0' + str(i+1)
        os.mkdir(path_ex)
        info_exer_map += [mode1.create_exercise(exam_date, str(i+1), path_ex, chosen_type_yaml)] # it calls the script that actually creates the exercise folder and notebook
        #mode2.create_exercise(exam_date, str(i+1), path_ex, chosen_type_yaml)
        #mode3.create_exercise(exam_date, str(i+1), path_ex, chosen_type_yaml)
        print('Exercise ' + str(i+1) + ' added')
    return info_exer_map

def add_map(date, badge_nb, info_map, name, surname): ############to_do
    """It creates the index map
    Parameters:
    date (str): YYYY-MM-DD
    badge_nb (str): e.g., VR123456
    info_map (list of str): for each exercises, its proper title to insert in the map
    name (str): students''s name
    surname (str): students''s surname"""
    
    global absolute_path_student
    shutil.copy('./avvia_esame.py', absolute_path_student) #to do: activate conda env in avvia_esame.py 
    to_render = map_generator.generate(info_map)
    copy_tree('./map',absolute_path_student+'/map')
    f = open(absolute_path_student + '/map/' + 'index.html','w')
    f.write(to_render)
    f.close()

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

def create_archives(student_anchored_folder, student_local_folder):
    """It creates .tgz and .zip files of the students's folder
    Parameters:
    student_anchored_folder (str): the name to be give to the folder for the download from the student
    student_local_folder (str): the name of the student's local exam folder
    """
    global absolute_path_student
    print(f"absolute_path_student = {absolute_path_student}")
    print(f"student_local_folder = {student_local_folder}")
    print(f"student_anchored_folder = {student_anchored_folder}")
    current = os.getcwd()
    os.chdir(current + REL_SHUTTLE_FOLDER)
    os.mkdir(student_anchored_folder)
    command_zip = 'zip -r ' + student_local_folder + '.zip ' + student_local_folder
    command_tar = "tar -cvzf " + student_local_folder + ".tgz " + student_local_folder
    risp = os.system(command_zip)
    print("Zip created ({student_local_folder + '.zip'})")
    risp = os.system(command_tar)
    print("Tar created ({student_local_folder + '.tgz'})")
    shutil.move(student_local_folder, student_anchored_folder + '/')
    shutil.move(student_local_folder + '.zip', student_anchored_folder + '/')
    shutil.move(student_local_folder + '.tgz', student_anchored_folder + '/')
    os.chdir(current)

def gen_exam(exam_date, anchor, student_ID, badge_nb, name, surname):
    """Main procedure that generate the exam for the given student.
    It can also be called by generate_all_exams_given_list.py
    Parameters:
    exam_date (str): exam date according to the format YYYY-MM-DD
    anchor (str): random string to use in the student's folder name
    student_ID (str): unique ID associated to a student
    badge_nb (str): badge number associated to a student
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
    ex_list = extract_ex(exam_date, badge_nb) # list of exercises to extract from collection
    keep_going = add_main_folder(student_anchored_folder) # if absolute_path_student already exists, ask if re-generating it or not
    if keep_going == 0:
        print("The exam (" + exam_date + ', ' + student_ID + ") has been already generated")
    else:
        print("\nNew generation of the exam (" + exam_date + ', ' + student_ID + ") started\nAdding exercises...")
        path_exercises = os.getcwd() + COLLECTION_FOLDER + exam_date
        info_exer_map = add_exercises(exam_date, path_exercises, ex_list)
        add_map(exam_date, badge_nb, info_exer_map, name, surname) # from the exercises created, it generates the map
        print("\nAdding the map...")
        #add_info()
        create_archives(student_anchored_folder, student_local_folder)
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
    parser.add_argument('badge_nb', type=str, default='VR123456', help='badge number associated to a student')
    parser.add_argument('name', type=str, default='Pinco', help='student''s name')
    parser.add_argument('surname', type=str, default='Pallino', help='student''s surname')
    args=parser.parse_args()
    assert len(sys.argv) == 7
    exam_date = str(sys.argv[1])
    anchor = str(sys.argv[2])
    student_ID = str(sys.argv[3])
    badge_nb = str(sys.argv[4])
    name = str(sys.argv[5])
    surname = str(sys.argv[6])
    gen_exam(exam_date, anchor, student_ID, badge_nb, name, surname)
