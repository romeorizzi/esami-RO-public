#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
import re
from pathlib import PurePath, Path
from pprint import pprint
import argparse

#import yield_long_dp_poldo, yield_long_dp_robot_no_gemme, yield_long_dp_triangle, yield_long_dp_lcs, yield_long_dp_knapsack
#from dp_lcs import yield_long_dp_lcs

CATEGORY="'NOT_DETECTED'"
def usage():
    risp = ""
    if CATEGORY=="'NOT_DETECTED'":
        risp += f"I guess you launched this script ({sys.argv[0]}) the wrong way since I could not detect the category of the problem (something like 'dp_poldo' or 'graphs_planarity' or 'lp_dualize'."
    risp += f"""This script ({sys.argv[0]}) serves in the generation process of problems in the category '{CATEGORY}'. It mainly generates a full source yaml file problem starting from a tiny yaml file with extension '.instance' and containing only the instance data (as specifically encoded for problems of the '{CATEGORY}' category). The generated file with the same basename but extension '.yaml' can be used as the source for the later generation of the Jupyter notebooks for the exam. The generated file with extension '.long_yaml' expands that file by including further matrials for later use and with various purposes: some of these are meant to support the evaluation and grading work by side of the instructor, others to provide explanations or just a correct solution for needed reference to the student. The list of these materials is expanding and in the future these could reach for futher collocations of purpose and use like including features for contextual assistance utils (during the the exam or when training) or other related services.

Right now, this script requires precisely one argument. The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. This fullname is expected to have .instance as extension!

Right now the script writes down on stdout the extended yaml file including the additional authomatically generated fields offering the support information for the specific fields and for the field categories that have been required (support in the evaluation process, explanations or feedback to the students, instance design).

Usage syntax:
   {sys.argv[0]} [-h] [--write_on_file] instance_fullfilename

Usage example:
   {sys.argv[0]} {os.path.join("..","collections","2021-07-16",CATEGORY,"01",CATEGORY)+".instance"}

The file {os.path.join("..","collections","2021-07-16",CATEGORY,"01",CATEGORY)+".instance"} is only required to contain the `instance` field with the instance defining data for problem category {CATEGORY} but if it contains further data (like for example if it is actually a file used for the generation of the exam) that should not be a problem. In particular, if it is actually a (renamed) .long_yaml file then the expected outcome is to get a faithful copy of that file. 

Work in progress ... (see also other scripts to get the wider picture of what still needs to be implemented).

"""
    return risp


def main():
    global CATEGORY
    CATEGORY="'NOT_DETECTED'"
    if len(sys.argv) < 2:
        print(f"Error: This script requires at least one argument, you called it with {len(sys.argv)-1} arguments!\n")
        print(usage())
        exit(1)

    parser=argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=usage,
    epilog="""-------------------""")
    parser.add_argument('instance_fullfilename', type=str, help=f'this mandatory argument should specify the fullname of the .instance file containing an instance for problem {CATEGORY}. This fullname is expected to have .instance as extension!')
    parser.add_argument('--write_on_file', help=f'when you use this optional argument then the output is redirected on a file with the same fullname as the instance file but with extension .yaml rather than .instance', action="store_true")
    args = parser.parse_args()
        
    filename_in = args.instance_fullfilename
    if not os.path.exists(filename_in):
        print(f"\nError: I could not find the instance file:\n    {filename_in}\nScript aborting.")
        exit(1)
    if filename_in[-9:] != ".instance":
        print(f"Error: The unique argument to this script should be the fullname of the .instance file containing an instance for problem {CATEGORY}. This fullname is expected to have .instance as extension!\n")
        print(usage())
        exit(1)
    CATEGORY=PurePath(filename_in[:-9]).parts[-1]
    exec(f"from {CATEGORY} import yield_long_{CATEGORY}")
    
    with open(filename_in) as file:
        instance_txt = file.readlines()
    with open(filename_in) as file:
        try:
            instance_dict = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)
            print(f"Attenzione! Il file yaml ({filename_in}) appare CORROTTO")
            exit(1)
    assert instance_txt[0][:3]=="---"
    assert instance_txt[1][:5]=="name:"
    assert instance_txt[-1][:3]=="..."
    fout = sys.stdout
    if args.write_on_file:
        fout_name = filename_in[:-9]+".yaml"
        fout = open(fout_name, "w")
    turned_off_info=set({})
    exec(f"yield_long_{CATEGORY}.explain_info_addenda_profile(turned_off_info)")
    active_task = None
    active_task_num = 0
    for line in instance_txt:
        #print(f"line> {line}")
        if line[:len("    task_codename:")] == "    task_codename:":
            active_task = line[len("    task_codename:"):].strip().strip("'").strip('"')
            active_task_num += 1
        if active_task != None and (line.strip()=="" or line[:2]=="- " or line[:3]=="..."):
            exec(f"yield_long_{CATEGORY}.yield_info_addenda(instance_dict, active_task, active_task_num, turned_off_info=turned_off_info, fout=fout)")
            active_task = None
        if "PLACEHOLDER_" not in line:
            print(line,end='',file=fout)
        else:
            tag,std_name=line.split(":")
            tag=tag.strip()
            std_name=std_name.strip()
            assert std_name[:len("PLACEHOLDER_")] == "PLACEHOLDER_"
            std_name=std_name[len("PLACEHOLDER_"):]
            exec(f"yield_long_{CATEGORY}.put_standardized_items(tag, std_name, instance_dict, active_task, active_task_num, fout=fout)")

    exit(0)

if __name__ == "__main__":
    main()
