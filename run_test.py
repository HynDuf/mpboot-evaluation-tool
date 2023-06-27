import sys
import os
import shutil
import random
import time

if len(sys.argv) != 2:
    print("Usage: python run_test.py <test_name>")
    print("test_name: The name of the running test (describing the purpose of the test)\n")
    print("Ex: python run_test.py SPR6_TBR5_ACO")
    sys.exit(1)

TEST_NAME = sys.argv[1]

# ======================================= EDIT THIS ======================================= #
PATH = "/home/diepht/hynduf/test"

DATA_PATH = PATH + "/data/example"

SUFFIXES = [
    "_SPR6",
    "_TBR5",
    "_ACO"
]

COMMANDS = [
    PATH + "/cmd/mpboot-avx -s " + DATA_PATH + "/? " + " -pre " +
    PATH + "/log/" + TEST_NAME + "/?" + SUFFIXES[0],

    PATH + "/cmd/mpboot-avx -s " + DATA_PATH + "/? " +
    " -tbr_pars -pre " + PATH + "/test/log/" + TEST_NAME + "/?" + SUFFIXES[1],

    PATH + "/cmd/mpboot-avx -s " + DATA_PATH + "/? " +
    " -aco -pre " + PATH + "/test/log/" + TEST_NAME + "/?" + SUFFIXES[2]
]

# Number of runs on each testcase for each command
NUM_RUNS = 10
SEEDS = [random.randint(0, 10000) for _ in range(NUM_RUNS)]
# ========================================================================================= #

# Remove files if exists in the result folder
shutil.rmtree(PATH + "/log/" + TEST_NAME, ignore_errors=True)
os.makedirs(PATH + "/log/" + TEST_NAME, exist_ok=True)

def job_sub_commands_generator(filename):
    for i in range(NUM_RUNS):
        for id in range(len(COMMANDS)):
            s = COMMANDS[id].replace("?", filename) + '_' + str(SEEDS[i]) + ' -seed ' + str(SEEDS[i]) + ' >/dev/null 2>&1'
            with open("generated_run_test.sh", "w") as f:
                f.write("#!/bin/bash\n")
                f.write(s)
            c = 'qsub -N ' + filename + SUFFIXES[id] + "_" + str(SEEDS[i]) + ' generated_run_test.sh'
            os.system(c)
        time.sleep(2)

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
