import random
# ======================================= EDIT THIS ======================================= #

# Name of the result folder
TEST_NAME = "test"

PATH = "/datausers/ioit/thaontp/hynduf/test"

DATA_PATH = PATH + "/data/example"
LOG_PATH = PATH + "/log/" + TEST_NAME
RESULT_PATH = PATH + "/result/" + TEST_NAME
DETAILS_RESULT_PATH = RESULT_PATH + "/details"

SUFFIXES = [
    "SPR6",
    "TBR5",
    "ACO"
]

COMMANDS = [
    PATH + "/cmd/mpboot-avx -s " + DATA_PATH + "/? " + " -pre " +
    LOG_PATH + "/?_" + SUFFIXES[0],

    PATH + "/cmd/mpboot-avx -s " + DATA_PATH + "/? " +
    " -tbr_pars -pre " + LOG_PATH + "/?_" + SUFFIXES[1],

    PATH + "/cmd/mpboot-avx -s " + DATA_PATH + "/? " +
    " -aco -pre " + LOG_PATH + "/?_" + SUFFIXES[2]
]

# Number of runs on each testcase for each command
NUM_RUNS = 5
SEEDS = [random.randint(0, 10000) for _ in range(NUM_RUNS)]

NUM_DATASET_FILES = 4
# ========================================================================================= #