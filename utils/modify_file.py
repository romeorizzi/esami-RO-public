#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import argparse

pattern = re.compile("scope")

parser=argparse.ArgumentParser(
description='''Script to modify a file like a .yaml file in the collactions to update to changes in general architecture''',
epilog="""-------------------""")
parser.add_argument('file_fullname', type=str, default='2020-06-30', help='fullname for the file to be updated')
args=parser.parse_args()

assert len(sys.argv) == 2
file_fullname = sys.argv[1]

with open(file_fullname) as f:
    lines = f.readlines()

file_out = open(file_fullname, "w")
line = lines[0].rstrip()
line_next = lines[1].rstrip()
for next_line in lines[2:]:
    if len(line) == 0:
        #print("riga vuota")
        file_out.write("\n")
    elif line[-1] != ',' and pattern.match(line_next.lstrip()):
        #print("riga modificata")
        file_out.write(line + ",\n")
    else:
        file_out.write(line + "\n")
    line = line_next
    line_next = next_line.rstrip()
file_out.write(line + "\n")
file_out.write(line_next + "\n")
