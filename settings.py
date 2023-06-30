import random
# ======================================= EDIT THIS ======================================= #

# Name of the result folder
TEST_NAME = "test_serious_21_41_30_06"

PATH = "/datausers/ioit/thaontp/hynduf/test"

DATA_PATH = PATH + "/data/treebase"
LOG_PATH = PATH + "/log/" + TEST_NAME
RESULT_PATH = PATH + "/result/" + TEST_NAME
DETAILS_RESULT_PATH = RESULT_PATH + "/details"

DEBUG_PATH = PATH + "/debug"
SCRIPTS_PATH = DEBUG_PATH + "/scripts/" + TEST_NAME

SUFFIXES = [
    "SPR6",
    "TBR5",
    "ACO",
    "ACO-INC-UPD-ITERS"
]

COMMANDS = [
    PATH + "/cmd/mpboot-avx-new -s " + DATA_PATH + "/? " + " -pre " +
    LOG_PATH + "/?_" + SUFFIXES[0],

    PATH + "/cmd/mpboot-avx-new -s " + DATA_PATH + "/? " +
    " -tbr_pars -pre " + LOG_PATH + "/?_" + SUFFIXES[1],

    PATH + "/cmd/mpboot-avx-new -s " + DATA_PATH + "/? " +
    " -aco -pre " + LOG_PATH + "/?_" + SUFFIXES[2],

    PATH + "/cmd/mpboot-avx-new -s " + DATA_PATH + "/? " +
    " -aco -aco_update_iter 35 -pre " + LOG_PATH + "/?_" + SUFFIXES[3]
]

# Number of runs on each testcase for each command
NUM_RUNS = 10
SEEDS = [random.randint(0, 100000) for _ in range(NUM_RUNS)]

NUM_DATASET_FILES = 115
# ========================================================================================= #