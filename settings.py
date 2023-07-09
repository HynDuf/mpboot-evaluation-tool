import random
# ======================================= EDIT THIS ======================================= #

# Name of the result folder
TEST_NAME = "test_serious_00_43_09_07"

PATH = "/home/diepht/hynduf/mpboot-evaluation-tool"

DATA_PATH = PATH + "/data/treebase"
LOG_PATH = PATH + "/log/" + TEST_NAME
RESULT_PATH = PATH + "/result/" + TEST_NAME
DETAILS_RESULT_PATH = RESULT_PATH + "/details"

DEBUG_PATH = PATH + "/debug"
SCRIPTS_PATH = DEBUG_PATH + "/scripts/" + TEST_NAME

SUFFIXES = [
    "SPR6",
    "TBR5",
    "ACO-OPT",
    "ACO-OPT-C",
    "ACO-OPT-1",
    "ACO-OPT-2",
    "ACO-OPT-3",
]

COMMANDS = [
    PATH + "/cmd/mpboot-avx-normal -s " + DATA_PATH + "/? " + " -pre " +
    LOG_PATH + "/?_" + SUFFIXES[0],

    PATH + "/cmd/mpboot-avx-normal -s " + DATA_PATH + "/? " +
    " -tbr_pars -pre " + LOG_PATH + "/?_" + SUFFIXES[1],

    PATH + "/cmd/mpboot-avx-opt -s " + DATA_PATH + "/? " +
    " -aco -pre " + LOG_PATH + "/?_" + SUFFIXES[2],

    PATH + "/cmd/mpboot-avx-opt-c -s " + DATA_PATH + "/? " +
    " -aco -pre " + LOG_PATH + "/?_" + SUFFIXES[3],

    PATH + "/cmd/mpboot-avx-opt -s " + DATA_PATH + "/? " +
    " -aco -aco_evaporation_rate 0.7 -pre " + LOG_PATH + "/?_" + SUFFIXES[4],

    PATH + "/cmd/mpboot-avx-opt -s " + DATA_PATH + "/? " +
    " -aco -aco_nni_prior 0.3 -aco_spr_prior 0.3 -aco_tbr_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[5],

    PATH + "/cmd/mpboot-avx-opt -s " + DATA_PATH + "/? " +
    " -aco -aco_ratchet_prior 0.25 -aco_iqp_prior 0.35 -aco_random_nni_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[6],
]

# Number of runs on each testcase for each command
NUM_RUNS = 10
# SEEDS = [random.randint(0, 100000) for _ in range(NUM_RUNS)]
SEEDS = [16321, 57307, 51137, 34235, 86622, 25298, 57844, 66232, 81441, 84374]

NUM_DATASET_FILES = 115
# ========================================================================================= #
