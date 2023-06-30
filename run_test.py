import sys
import os
import shutil
import time
from settings import *
from helper_func import create_necessary_dirs

create_necessary_dirs()

def job_sub_commands_generator(filename):
    for i in range(NUM_RUNS):
        for id in range(len(COMMANDS)):
            s = COMMANDS[id].replace("?", filename) + '_' + str(SEEDS[i]) + ' -seed ' + str(SEEDS[i])
            with open("generated_run_test.sh", "w") as f:
                f.write("#!/bin/bash\n")
                f.write(s)
            c = 'qsub -q long_cpu -N ' + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ' -l select=1:ncpus=1 -j oe generated_run_test.sh'
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

# Subscribe jobs to the system
for file_name in list_of_files_desc_size:
  job_sub_commands_generator(file_name)
