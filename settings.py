import random
# ======================================= EDIT THIS ======================================= #

# Name of the result folder
TEST_NAME = "all_aco3_1020_1312"

PATH = "/home/diepht/hynduf/mpboot-evaluation-tool"

DATA_PATH = PATH + "/data/treebase"
LOG_PATH = PATH + "/log/" + TEST_NAME
RESULT_PATH = PATH + "/result/" + TEST_NAME
DETAILS_RESULT_PATH = RESULT_PATH + "/details"
ACO_DETAILS_RESULT_PATH = RESULT_PATH + "/aco_details"

DEBUG_PATH = PATH + "/debug"
SCRIPTS_PATH = DEBUG_PATH + "/scripts/" + TEST_NAME

SUFFIXES = [
    # "SPR6",
    # "TBR5",
    # "TBR5-SC100",
    # "ACO-OPT-3-W",
    # "ACO-EQ-W",
    # "ACO-OPT-3-W-1",
    "ACO-EQ-W-0-1",
    "ACO-EQ-W-MUL-0-1",
    "SPR6",
    "TBR5"
    # "ACO-OPT-W",
]

COMMANDS = [
    # PATH + "/cmd/mpboot-avx-covid -s " + DATA_PATH + "/? " +
    # " -pre " + LOG_PATH + "/?_" + SUFFIXES[0],

    # PATH + "/cmd/mpboot-avx-covid -s " + DATA_PATH + "/? " +
    # " -tbr_pars -pre " + LOG_PATH + "/?_" + SUFFIXES[1],

    # PATH + "/cmd/mpboot-avx-covid -s " + DATA_PATH + "/? " +
    # " -tbr_pars -stop_cond 100 -pre " + LOG_PATH + "/?_" + SUFFIXES[2],

    # PATH + "/cmd/mpboot-avx-covid -s " + DATA_PATH + "/? " +
    # " -aco -aco_stop_cond -aco_ratchet_prior 0.3 -aco_iqp_prior 0.3 -aco_random_nni_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[3],

    # PATH + "/cmd/mpboot-avx-covid -s " + DATA_PATH + "/? " +
    # " -aco -aco_stop_cond -aco_ratchet_prior 0.3 -aco_iqp_prior 0.3 -aco_random_nni_prior 0.3 -aco_nni_prior 0.3 -aco_spr_prior 0.3 -aco_tbr_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[4],
    
    # PATH + "/cmd/mpboot-avx-covid-log -s " + DATA_PATH + "/? " + 
    # " -aco -aco_stop_cond -aco_ratchet_prior 0.25 -aco_iqp_prior 0.35 -aco_random_nni_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[0],

    # PATH + "/cmd/mpboot-avx-covid-log -s " + DATA_PATH + "/? " +
    # " -aco -aco_stop_cond -aco_evaporation_rate 0.4 -aco_ratchet_prior 0.3 -aco_iqp_prior 0.3 -aco_random_nni_prior 0.3 -aco_nni_prior 0.3 -aco_spr_prior 0.3 -aco_tbr_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[0],
    
    PATH + "/cmd/mpboot-avx-aco-3-once -s " + DATA_PATH + "/? " +
    " -aco -aco_stop_cond -aco_evaporation_rate 0.1 -aco_nni_prior 0.3 -aco_spr_prior 0.4 -aco_tbr_prior 0.4 -pre " + LOG_PATH + "/?_" + SUFFIXES[0],

    PATH + "/cmd/mpboot-avx-aco-3-multiple -s " + DATA_PATH + "/? " +
    " -aco -aco_stop_cond -aco_evaporation_rate 0.1 -aco_nni_prior 0.3 -aco_spr_prior 0.4 -aco_tbr_prior 0.4 -pre " + LOG_PATH + "/?_" + SUFFIXES[1],

    PATH + "/cmd/mpboot-avx-aco-3-multiple -s " + DATA_PATH + "/? " +
    " -pre " + LOG_PATH + "/?_" + SUFFIXES[2],

    PATH + "/cmd/mpboot-avx-aco-3-multiple -s " + DATA_PATH + "/? " +
    " -tbr_pars -pre " + LOG_PATH + "/?_" + SUFFIXES[3],
    # PATH + "/cmd/mpboot-avx-covid-log -s " + DATA_PATH + "/? " +
    # " -aco -aco_stop_cond -aco_evaporation_rate 0.4 -aco_ratchet_prior 0.3 -aco_iqp_prior 0.3 -aco_random_nni_prior 0.4 -aco_nni_prior 0.45 -aco_spr_prior 0.4 -aco_tbr_prior 0.3 -pre " + LOG_PATH + "/?_" + SUFFIXES[2],
]

NUM_VERSIONS = 4

# Number of runs on each testcase for each command
NUM_RUNS = 50
# SEEDS = [random.randint(0, 100000) for _ in range(NUM_RUNS)]
SEEDS = list(range(1, NUM_RUNS + 1))
# SEEDS = [16321, 57307, 51137, 34235, 86622, 25298, 57844, 66232, 81441, 84374]

NUM_DATASET_FILES = 115
# ========================================================================================= #
