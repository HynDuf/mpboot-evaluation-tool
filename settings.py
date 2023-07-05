import random
# ======================================= EDIT THIS ======================================= #

# Name of the result folder
TEST_NAME = "test_serious_07_02_04_07"

PATH = "/datausers/ioit/thaontp/hynduf/test"

DATA_PATH = PATH + "/data/treebase"
LOG_PATH = PATH + "/log/" + TEST_NAME
RESULT_PATH = PATH + "/result/" + TEST_NAME
DETAILS_RESULT_PATH = RESULT_PATH + "/details"

DEBUG_PATH = PATH + "/debug"
SCRIPTS_PATH = DEBUG_PATH + "/scripts/" + TEST_NAME

SUFFIXES = [
    "ACO-OPT",
    "ACO-OPT-C"
]

COMMANDS = [
    # PATH + "/cmd/mpboot-avx-new -s " + DATA_PATH + "/? " + " -pre " +
    # LOG_PATH + "/?_" + SUFFIXES[0],

    # PATH + "/cmd/mpboot-avx-new -s " + DATA_PATH + "/? " +
    # " -tbr_pars -pre " + LOG_PATH + "/?_" + SUFFIXES[1],

    PATH + "/cmd/mpboot-avx-opt -s " + DATA_PATH + "/? " +
    " -aco -pre " + LOG_PATH + "/?_" + SUFFIXES[0],

    PATH + "/cmd/mpboot-avx-opt-c -s " + DATA_PATH + "/? " +
    " -aco -pre " + LOG_PATH + "/?_" + SUFFIXES[1]
]

# Number of runs on each testcase for each command
NUM_RUNS = 10
# SEEDS = [random.randint(0, 100000) for _ in range(NUM_RUNS)]
SEEDS = [16321, 57307, 51137, 34235, 86622, 25298, 57844, 66232, 81441, 84374]

NUM_DATASET_FILES = 115
# ========================================================================================= #