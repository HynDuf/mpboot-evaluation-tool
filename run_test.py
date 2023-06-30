import sys
import os
import time
from settings import *
from helper_func import *

for SUF in SUFFIXES:
    if '_' in SUF:
        print("No underscore ('_') allowed in SUFFIXES. Please fix " + SUF)
        exit(0)
create_necessary_dirs()

def job_sub_commands_generator(filename):
    for i in range(NUM_RUNS):
        for id in range(len(COMMANDS)):
            s = COMMANDS[id].replace("?", filename) + '_' + str(SEEDS[i]) + ' -seed ' + str(SEEDS[i])
            script_path = SCRIPTS_PATH + "/" + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ".sh"
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(s)
            c = 'qsub -q para_cpu -N ' + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ' -l select=1:ncpus=1 -j oe ' + script_path
            os.system(c)

# Get list of all .phy files in the given directory
list_of_files_desc_size = filter(
    lambda x: os.path.isfile(os.path.join(DATA_PATH, x)) and x.endswith(".phy"
                                                                        ),
    os.listdir(DATA_PATH))
# Sort list of file names by size
list_of_files_desc_size = sorted(
    list_of_files_desc_size,
    key=lambda x: os.stat(os.path.join(DATA_PATH, x)).st_size)
list_of_files_desc_size.reverse()

print("There are " + str(len(list_of_files_desc_size)) + " files in DATA_PATH = " + DATA_PATH)
assert(NUM_DATASET_FILES == len(list_of_files_desc_size))

# Subscribe jobs to the system
for file_name in list_of_files_desc_size:
  job_sub_commands_generator(file_name)
