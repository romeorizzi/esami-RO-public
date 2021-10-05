#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script can be used both as such and as a library (called by called by generate_all_exams_given_students_list.py).
It exports the functionality of:

  def gen_one_exam(exam_date, student_ID, matricola, name, surname, anchor="", passwd=None, as_zip = False, as_tgz = False, as_folder = False, as_encrypted_zip = True, as_encrypted_tgz = False)
    Main Purpose of procedure gen_one_exam:
       it generates the exam for that student.
    Parameters:
     exam_date: a string in the format YYYY-MM-DD
     anchor: a random string to use in the student's folder name
     student_ID: unique ID associated to a student (example: id996zei)
     matricola: badge number associated to a student (example: VR429697)
     name: the student's name is a string that might contain spaces
     surname: the student's surname is a string that might contain spaces
    Returns:
      ex_index_list (list of integers): for each exercise type in the collection it returns the index of the instance assigned to the student for that one exercise. This returned info is useful to compose a .csv that summarizes, for each student, its actual exercises.
"""

import sys
import os
import argparse
import csv
import errno
import glob
import hashlib
import shutil
from distutils.dir_util import copy_tree
import tarfile
import zipfile

import create_exercise_free as mode_free
import create_exercise_verifier as mode_ver
import map_generator
from our_commons import COLLECTION_FOLDER, check_active_conda_env

OUR_CONDA_ENV_FOR_GENERATION="ROexam"

start_up_folder = os.getcwd() # è il folder dove risiede e da cui deve essere lanciato questo script. Anche se in realtà uscirà quì espresso come un path assoluto (che parte dalla root), ma, per intenderci, dovrebbe essere qualcosa del tipo ~/corsi/RO/esami/esami-RO-private
STUDENTS_LISTS_BASEFOLDER = os.path.join(start_up_folder,'students_lists')
SHUTTLE_FOLDER = os.path.join(start_up_folder,'shuttle')
UTILS_FOLDER = os.path.join(start_up_folder,'utils')
RO_EXAM = 'esame-RO_'
UPLOAD_INSTRUCTIONS = os.path.join('info_upload','ISTRUZIONI_RICONSEGNA.pdf')
START_INSTRUCTIONS = os.path.join('info_start','ISTRUZIONI_AVVIO.pdf')
TROUBLESHOOTING = os.path.join('troubleshooting','TROUBLESHOOTING.pdf')

"""EVEN MORE IMPORTANT FOLDERS FOR VARIOUS PROCEDURES HERE BELOW:
      (all these variables are created and set up as global at the beginning of the main function gen_one_exam(student_ID, ...) and, after this unique set up moment, some of the other functions here below access them in only read mode to properly serve when called by gen_one_exam)

1. name_of_student_temporary_subfolder_in_shuttle_folder:
      set up as = RO_EXAM + exam_date + '_' + student_ID
      role1: the main role is that explained in item 2 of this list.
      role2: some of the external commands used when creating the archives get easier and more robust to use on different platforms when we move on the folder.
      used only by: create_archives
2. absolute_path_student_temporary_subfolder:
      set up as = SHUTTLE_FOLDER + name_of_student_temporary_subfolder_in_shuttle_folder
      role: this folder is meant to offer the place where to generate the materials for the student. This folder will then be the starting point for the generation of several kinds of archive files for the most convenient deployment. 
3. name_of_student_anchored_subfolder_in_shuttle_folder:
      set up as = RO_EXAM + exam_date + '_' + anchor + '__' + student_ID
      role: this folder offers the archives of the "student_temporary_subfolder" suitable for deployment from a web server where the access gets controlled by the knowledge of the anchor AND of the passwd. 
      used only by: create_archives
4. name_of_student_unanchored_subfolder_in_shuttle_folder:
      set up as = RO_EXAM + exam_date + '__' + student_ID
      role: this folder offers the archives of the "student_temporary_subfolder" suitable for deployment via Telegram or direct mail attachment (currenty only an encrypted zip to be decriptd using the anchor as key).      used only by: create_archives  

"""

def frozen_random_extraction(type_exercise, num_of_instances, exam_date, student_ID):
    """It computes an hash starting from the string student_ID+exam_date, keeping only digits
    Parameters:
    exam_date (str): YYYY-MM-DD
    student_ID (str): student_ID
    Returns:
    a list of integers"""
    h = hashlib.md5((student_ID+exam_date+type_exercise).encode('utf-8')).hexdigest()
    random_natural = sum(c for c in h.encode())
    return random_natural%num_of_instances


def add_exercises(exam_date, matricola, path_collection):
    """It adds the exercises extracted to the student_temporary_subfolder
    Parameters:
    exam_date (str): YYYY-MM-DD
    path_collection (str): where to find the collection of exercises
    ex_list (list of positive integers): extracted instance for each exercise type
    Returns:
       1. info_exer_map (list of str): for each exercise, its proper title to insert in the map
       2. ex_index_list (list of integers): for each exercise type in the collection it returns the index of the instance assigned to the student for that one exercise. Returning this is info is useful to compose a .csv file that summarizes, for each student, its actual exercises"""
    if not os.path.isdir(path_collection):
        print(f"\nATTENTION: Collection folder not found! Could not find {path_collection}")
        exit(1)
    info_exer_map = []
    type_list = [x for x in sorted(os.listdir(path_collection)) if '.DS_Store' not in x and 'graphml-'+exam_date not in x]
    print(f"\nTaking from collection folder {path_collection}\n   List of the exercise types included: {type_list}")
    ex_index_list = [None] * len(type_list)
    for i in range(len(type_list)):
        path_type = os.path.join(path_collection,type_list[i])
        print(path_type)
        num_of_instances = len(glob.glob(os.path.join(path_type, '??'))) # there must be at least one exercise for each type
        assert num_of_instances > 0
        chosen = 1+frozen_random_extraction(type_list[i], num_of_instances, exam_date, matricola)
        ex_index_list[i] = chosen
        path_full_yaml = os.path.join(path_type,str(chosen).zfill(2),f"{type_list[i]}.yaml")
        path_ex = os.path.join(absolute_path_student_temporary_subfolder, f"esercizio_{str(i+1)}")
        os.mkdir(path_ex)
        if type_list[i] in ['dp_poldo', 'dp_lcs', 'dp_robot_no_gemme', 'dp_triangle', 'dp_knapsack']: # mode_ver
            info_exer_map += [mode_ver.create_exercise(exam_date, str(i+1), path_ex, type_list[i], path_full_yaml)]
        else: # mode_free o mode_applet
            info_exer_map += [mode_free.create_exercise(exam_date, str(i+1), path_ex, path_full_yaml)] # it calls the script that actually creates the exercise folder and notebook

        print(f'Exercise {str(i+1)} ({type_list[i]}) added for student {absolute_path_student_temporary_subfolder[-8:]} (folder added: {absolute_path_student_temporary_subfolder}')
    print(f"\n\nECCO\n    ex_index_list = {ex_index_list} for matricola={matricola}\n\n")
    return info_exer_map, ex_index_list

def add_map(exam_date, matricola, info_exer_map, name, surname):
    """It creates the index map in the student_temporary_subfolder
    Parameters:
    date (str): YYYY-MM-DD
    matricola (str): e.g., VR123456
    info_exer_map (list of str): for each exercises, its proper title to insert in the map
    name (str): students''s name
    surname (str): students''s surname"""
    shutil.copy(os.path.join(os.getcwd(),'avvia_esame.py'), absolute_path_student_temporary_subfolder) #to do: activate conda env in avvia_esame.py
    to_render = map_generator.generate(exam_date, info_exer_map)
    copy_tree(os.path.join(os.getcwd(),'map'),os.path.join(absolute_path_student_temporary_subfolder,'map'))
    f = open(os.path.join(absolute_path_student_temporary_subfolder,'map','index.html'),'w')
    f.write(to_render)
    f.close()

def add_graph_utils():
    """It adds graph utils in the student_temporary_subfolder
    Parameters:"""
    copy_tree(os.path.join(os.getcwd(),'utils','graph_utils','js'),os.path.join(absolute_path_student_temporary_subfolder,'graph_utils','js'))
    copy_tree(os.path.join(os.getcwd(),'utils','graph_utils','css'),os.path.join(absolute_path_student_temporary_subfolder,'graph_utils','css'))


def add_info():
    """It adds three useful files to the student_temporary_subfolder, copying them from the utils folder"""
    info_upload_src = os.path.join(UTILS_FOLDER, UPLOAD_INSTRUCTIONS)
    info_start_src = os.path.join(UTILS_FOLDER, START_INSTRUCTIONS)
    info_troubleshooting_src = os.path.join(UTILS_FOLDER, TROUBLESHOOTING)
    shutil.copy(info_start_src, absolute_path_student_temporary_subfolder)
    shutil.copy(info_upload_src, absolute_path_student_temporary_subfolder)
    shutil.copy(info_troubleshooting_src, absolute_path_student_temporary_subfolder)

def create_archives(as_zip, as_tgz, as_folder, as_encrypted_zip, as_encrypted_tgz, encryption_key):
    """It creates .tgz and .zip archives of the 'name_of_student_temporary_subfolder_in_shuttle_folder' and moves them within either the 'name_of_student_anchored_subfolder_in_shuttle_folder' or in the 'name_of_student_unanchored_subfolder_in_shuttle_folder' depending on their inherent protections. If `as_folder` is set to `True` then also the unarchived folder is included. In any case the source folder 'name_of_student_temporary_subfolder_in_shuttle_folder' is removed. 
    Parameters:
    name_of_student_anchored_subfolder_in_shuttle_folder (str): the name to be give to the folder for the download from the student
    name_of_student_temporary_subfolder_in_shuttle_folder (str): the name of the student's local exam folder
    """
    os.chdir(SHUTTLE_FOLDER)
    folder_types_involved = []
    if as_zip or as_tgz:
        folder_types_involved.append(name_of_student_anchored_subfolder_in_shuttle_folder)
    if as_encrypted_zip or as_encrypted_tgz:
        folder_types_involved.append(name_of_student_unanchored_subfolder_in_shuttle_folder)
    for folder_type in folder_types_involved:
        if os.path.exists(folder_type):
            print(f"\nISSUE: There already exists a folder of this type (anchored versus unachored) for this student in the current shuttle. Namely, the file\n   {folder_type}\nwould go overwritten with the new generation.") 
            answer = input("Do you really want to delete and generate again that folder with the exam?\n > Enter 'y' or 'n': ")
            while answer not in ("y", "n", "Y", "N"):
                print("Please enter 'y' (for 'yes') or 'n' (for 'no')")
            if answer in ("n", "N"):
                continue
            shutil.rmtree(folder_type)
            print(f"I have removed the old student folder ({folder_type}). Now building up the new version of it  ...\n")
        os.mkdir(folder_type)
    if as_zip:
        if not os.path.exists(os.path.join(name_of_student_anchored_subfolder_in_shuttle_folder,name_of_student_temporary_subfolder_in_shuttle_folder + '.zip')):
            os.system(f"zip -r {name_of_student_temporary_subfolder_in_shuttle_folder}.zip {name_of_student_temporary_subfolder_in_shuttle_folder}")
            print("Zip created ({name_of_student_temporary_subfolder_in_shuttle_folder + '.zip'})")
            shutil.move(name_of_student_temporary_subfolder_in_shuttle_folder + '.zip', os.path.join(name_of_student_anchored_subfolder_in_shuttle_folder, ''))
    if as_tgz:
        if not os.path.exists(os.path.join(name_of_student_anchored_subfolder_in_shuttle_folder, name_of_student_temporary_subfolder_in_shuttle_folder + '.tgz')):
            os.system(f"tar -cvzf {name_of_student_temporary_subfolder_in_shuttle_folder}.tgz {name_of_student_temporary_subfolder_in_shuttle_folder}")
            print("Tar created ({name_of_student_temporary_subfolder_in_shuttle_folder + '.tgz'})")
            shutil.move(name_of_student_temporary_subfolder_in_shuttle_folder + '.tgz', os.path.join(name_of_student_anchored_subfolder_in_shuttle_folder,''))
    if as_encrypted_zip:
        if not os.path.exists(os.path.join(name_of_student_unanchored_subfolder_in_shuttle_folder, name_of_student_temporary_subfolder_in_shuttle_folder + '.zip')):
            os.system(f"zip -r --password {encryption_key} {name_of_student_temporary_subfolder_in_shuttle_folder}.zip {name_of_student_temporary_subfolder_in_shuttle_folder}")
            print("Encrypted Zip created ({name_of_student_temporary_subfolder_in_shuttle_folder + '.zip'})")
            shutil.move(name_of_student_temporary_subfolder_in_shuttle_folder + '.zip', os.path.join(name_of_student_unanchored_subfolder_in_shuttle_folder,''))
    if not as_folder:
        shutil.rmtree(name_of_student_temporary_subfolder_in_shuttle_folder)
    os.chdir(start_up_folder)

def gen_one_exam(exam_date, student_ID, matricola, name, surname, anchor="", passwd=None, as_zip = True, as_tgz = False, as_folder = False, as_encrypted_zip = True, as_encrypted_tgz = False):
    """Main procedure that generates the exam for the given student.
    It can also be called by generate_all_exams_given_students_list.py
    Parameters:
     exam_date: a string in the format YYYY-MM-DD
     anchor: a random string to use in the student's folder name
     student_ID: unique ID associated to a student (example: id996zei)
     matricola: badge number associated to a student (example: VR429697)
     name: the student's name is a string that might contain spaces
     surname: the student's surname is a string that might contain spaces
    Returns:
      ex_index_list (list of integers): for each exercise type in the collection it returns the instance number assigned to the student for that one exercise. This returned info is useful to compose a .csv that summarizes, for each student, its actual exercises.
    """
    global absolute_path_student_temporary_subfolder # path where the folder with the exam material for the student is first created
    global name_of_student_temporary_subfolder_in_shuttle_folder
    global name_of_student_anchored_subfolder_in_shuttle_folder
    global name_of_student_unanchored_subfolder_in_shuttle_folder
    name_of_student_temporary_subfolder_in_shuttle_folder = RO_EXAM + exam_date + '_' + student_ID
    absolute_path_student_temporary_subfolder = os.path.join(SHUTTLE_FOLDER, name_of_student_temporary_subfolder_in_shuttle_folder)
    name_of_student_anchored_subfolder_in_shuttle_folder = RO_EXAM + exam_date + '_' + anchor + '__' + student_ID
    name_of_student_unanchored_subfolder_in_shuttle_folder = RO_EXAM + exam_date + '__' + student_ID
    check_active_conda_env(OUR_CONDA_ENV_FOR_GENERATION)
    if os.path.exists(SHUTTLE_FOLDER) == False:   # students can be incrementally added!
        os.mkdir(SHUTTLE_FOLDER)
    if os.path.exists(absolute_path_student_temporary_subfolder):
        shutil.rmtree(absolute_path_student_temporary_subfolder)
    os.mkdir(absolute_path_student_temporary_subfolder)
    print("\nNew generation of the exam (" + exam_date + ', ' + student_ID + ") started\nAdding exercises...")
    path_collection = os.path.join(os.getcwd(), COLLECTION_FOLDER, exam_date)
    info_exer_map,ex_index_list = add_exercises(exam_date, matricola, path_collection)
    print("\nAdding the map...")
    add_map(exam_date, matricola, info_exer_map, name, surname) # from the exercises created, it generates the map
    print("\n Adding graph utils")
    add_graph_utils()
    create_archives(as_zip, as_tgz, as_folder, as_encrypted_zip, as_encrypted_tgz, encryption_key=anchor)
    print("\nGeneration of the exam (" + exam_date + ', ' + student_ID + ") completed")
    return ex_index_list

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
        description='''Script to generate a new exam for the course of Ricerca Operativa (UniVR).
        It receives as input the exam date and the student data (ID, badge number, name and surname),
        which will be used to compute an hash in order to generate a pseudocasual exam
        (reconstrunctable in the future exactly as it is). ''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date according to the format YYYY-MM-DD')
    parser.add_argument('student_ID', type=str, default='id123456', help='unique ID associated to a student')
    parser.add_argument("--with_uncompressed_folder", help="please, add also the uncompressed directly accessible folder",
                    action="store_true")
    parser.add_argument("--without_tgz", help="please, do NOT generate the .tgz archive (the one that ends up in the anchored folder)",
                    action="store_true")
    parser.add_argument("--without_zip", help="please, do NOT generate the unencrypted zip archive (the one without password protection that ends up in the anchored folder)",
                    action="store_true")
    parser.add_argument("--without_encrypted_zip", help="do NON generate the encrypted zip archive (the one with password protection that ends up in the unanchored folder with no anchor in the folder name)",
                    action="store_true")
    parser.add_argument("--with_encrypted_tgz", help="please, generate also the encrypted tgz archive (the one with password protection that ends up in the unanchored folder with no anchor in the folder name)",
                    action="store_true")
    args = parser.parse_args()
    assert len(sys.argv) >= 3
    exam_date = str(sys.argv[1])
    student_ID = str(sys.argv[2])
    
    FILE_STUDENTS_LIST = os.path.join(STUDENTS_LISTS_BASEFOLDER,exam_date,"lista_studenti_iscritti_con_chiavi.csv")
    if not os.path.exists(FILE_STUDENTS_LIST):
        print(f"Error: I could not find the .csv file:\n    {FILE_STUDENTS_LIST}\nThis file is needed (see the name of this script!). If you are just playing around consider copying the file from another exam date and either use it as it is or drop all rows except the one for the TEST fake student. Also, it is easy to edit/create other lines: anchors (the third field) are just any random string of that same lenght as the others, and the password (the fourth field) is just 6 digits.")
        exit(1)
    ID_FIELD=4
    student_found=False
    with open(FILE_STUDENTS_LIST) as csv_file: # we seek the file to find the data of the given student
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[ID_FIELD] == student_ID:
                student_found=True
                matricola = row[0]
                anchor = row[2]
                passwd = row[3]
                name = row[5]
                surname = row[6]
    if not student_found:
        print(f"Error: I could not find your student ({student_ID}) within the .csv file:\n    {FILE_STUDENTS_LIST}\nIf you really want to generate an exam for this student, please, add first a line to the above .csv file and then run this script! Do not be scared in just adding lines to this file, as long as you do not spoil the other lines there is no danger in just adding conformant lines: anchors (the third field) are just any random string of that same lenght as the others, and the password (the fourth field) is just 6 digits.")
        exit(0)


    print(f"For this student ({student_ID}) the shuttle will contain:")
    if args.with_uncompressed_folder:
        print("  + The uncompressed and directly accessible folder.")
    if not args.without_zip:
        print("  + The unprotected .zip archive hidden within the anchored folder.")
    if not args.without_tgz:
        print("  + The unprotected .tgz archive hidden within the anchored folder.")
    if not args.without_encrypted_zip:
        print("  + The encryption protected .zip archive within the unanchored folder.")
    if args.with_encrypted_tgz:
        print("  + The password protected .tgz archive within the unanchored folder.")
                
    e_list = "" 
    chosen_exer = gen_one_exam(exam_date, student_ID, matricola, name, surname, anchor, passwd, as_zip=not args.without_zip, as_tgz=not args.without_tgz, as_folder=args.with_uncompressed_folder, as_encrypted_zip=not args.without_encrypted_zip, as_encrypted_tgz=args.with_encrypted_tgz)
    for e in chosen_exer:
        e_list += str(e) + ','
    e_list += name + ',' + surname + '\n'
    print(f'\nThe exam generated for {student_ID} ({name} {surname}, {matricola}) has the following profile for the exercises:\n {chosen_exer}')

    
