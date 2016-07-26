import re
import os

SRCDIR = "../src/"

try:
    global_file = open(SRCDIR+"global.h",'r')
    GLOBAL =  global_file.readlines()
    global_file.close()
except:
    print "(global.py) Error: global.h cannot be opened"
    exit()
globalex = open('global_ex.h', 'w')
warning = """ /* This file was created automatically during compilation
from global.h. Do not edit. See python script
"global.py" for details. */ """
warning += "\n\n"
globalex.write(warning)


for line in GLOBAL:
    try:
        search = re.search("(\S+)\s+(\S+)",line)
        type = search.group(1)
        variable = search.group(2)
    except:
        continue
    if(line[0:2] == "//"): continue # Skip a comment
    if (re.search("(\S+)\[.*\]", search.group(2))): #dimensions (arrays)
        variable = re.search("(\S+)\[.*\]", search.group(2)).group(1)
    if (re.search("(\S+)=", search.group(2))): #equals (affectations)
        variable = re.search("(\S+)=", search.group(2)).group(1)
    if (re.search("(\S+)\s?;", search.group(2))): #";" (C separator)
        variable = re.search("(\S+)\s?;", search.group(2)).group(1)

    new_line = "extern " + type + " " + variable + ";\n"
    globalex.write(new_line)
globalex.close()
