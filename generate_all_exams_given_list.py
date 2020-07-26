#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:04:51 2020

@authors: Alice Raffaele, Alessandro Busatto, Marco Emporio, Marco Fattorelli, Romeo Rizzi, Aurora Rossi, Francesco Trotti

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
    parser.add_argument('students_list_csv', type=str, default=os.getcwd()+'/students_list_2020-06-30/lista_studenti_iscritti_con_chiavi.csv/', help='csv file with students'' data')
    args=parser.parse_args()

    assert len(sys.argv) == 3
    exam_date = str(sys.argv[1])
    FILE_STUDENTS_LIST = str(sys.argv[2])

    start_time = time.time()
    Path(REL_PATH_SHUTTLE).mkdir(parents=True, exist_ok=True) # it creates the shuttle folder if it does not exist
    if os.path.isfile(ALL_EXER_PER_STUD + exam_date + '.csv'): # it deletes the csv file with all exercises per student if already existing
        Path(ALL_EXER_PER_STUD + exam_date + '.csv').unlink()
    PATH_SHUTTLE = os.getcwd() + '/' + REL_PATH_SHUTTLE
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
            chosen_exer = g.gen_exam(exam_date, anchor, student_ID, matricola, name, surname)
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
