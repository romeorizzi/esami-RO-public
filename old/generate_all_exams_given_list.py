#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:04:51 2020

@authors:
Verifiers: Alessandro Busatto, Paolo Graziani, Aurora Rossi, Davide Roznowicz;
Applet: Giacomo Di Maggio, Marco Emporio, Marco Fattorelli, Sebastiano Gaiardelli, Francesco Trotti;
Map: Rosario Di Matteo, Marco Emporio, Adriano Tumminelli;
OneDrive: Marco Fattorelli, Davide Roznowicz;
Integration: Alice Raffaele, Romeo Rizzi.

"""

import argparse
import csv
import generate_exam as g
import os
from pathlib import Path
import sys
import time

REL_PATH_SHUTTLE = 'shuttle' # main folder where to put all exams generated
ALL_EXER_PER_STUD = 'all_exercises_list_' # csv file where to save all exercises assigned to students (to facilitate correction)

if __name__ == "__main__":
    parser=argparse.ArgumentParser(
    description='''Script to generate all exams for a given date and a given list of students''',
    epilog="""-------------------""")
    parser.add_argument('exam_date', type=str, default='2020-06-30', help='exam date in the format YYYY-MM-DD')
#    parser.add_argument('students_list_csv', type=str, default=os.getcwd()+'/students_lists/2020-06-30/lista_studenti_iscritti_con_chiavi.csv/', help='csv file with students'' data')
    parser.add_argument("--with_uncompressed_folder", help="the generated anchored folder will contain also the uncompressed folder",
                    action="store_true")
    args = parser.parse_args()
    if args.with_uncompressed_folder:
        assert len(sys.argv) == 3
        print("The generated anchored folders will contain also the respective uncompressed folder.")
    else:
        assert len(sys.argv) == 2
    exam_date = str(sys.argv[1])
    FILE_STUDENTS_LIST = "students_lists/"+exam_date+"/lista_studenti_iscritti_con_chiavi.csv"

    # Creation of shuttle
    start_time = time.time()
    PATH_SHUTTLE = os.getcwd() + '/' + REL_PATH_SHUTTLE
    if os.path.exists(PATH_SHUTTLE):
        answer = None # if the exam has been already created for given student and date, ask if re-write it or not
        while answer not in ("y", "n"):
            answer = input("Do you want to generate again the shuttle folder? Enter 'y' or 'n': ")
            if answer == "y": # it empties the folder PATH_SHUTTLE
                for root, dirs, files in os.walk(PATH_SHUTTLE, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(PATH_SHUTTLE)
                os.mkdir(PATH_SHUTTLE)
                keep_going = 1
            elif answer == "n":
                keep_going = 0
            else:
                print("Please enter 'yes' or 'no'")
    else:
        os.mkdir(PATH_SHUTTLE)
        keep_going = 1
    
    # Generation of the exams    
    if keep_going:
        if os.path.isfile(ALL_EXER_PER_STUD + exam_date + '.csv'): # it deletes the csv file with all exercises per student if already existing
            Path(ALL_EXER_PER_STUD + exam_date + '.csv').unlink()
        all_exer_list = [] # to save all exercises assigned to each student
        with open(FILE_STUDENTS_LIST) as csv_file: # it reads the students list csv and generates an exam for each one of them
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                matricola = row[0]
                anchor = row[2]
                student_ID = row[4]
                name = row[5]
                surname = row[6]
                print('\nGenerating the exam for ' + name + ' ' + surname + ' (' + matricola + ')...')
                e_list = matricola + ',' + name + ',' + surname + ','
                chosen_exer = g.gen_exam(exam_date, anchor, student_ID, matricola, name, surname, args.with_uncompressed_folder)
                for e in chosen_exer:
                    e_list += str(e) + ','
                e_list += '\n'
                line_count += 1
                all_exer_list += [e_list]
            print(f'\nGenerated {line_count} exams.')
        exer_file = open(ALL_EXER_PER_STUD + exam_date + '.csv','w+') # writing the csv file with all exercises per student
        for line in all_exer_list:
            exer_file.write(str(line))
        exer_file.close()
    print("--- %s seconds ---" % (time.time() - start_time))
