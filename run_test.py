import os
import shutil
import time
from settings import *
from helper_func import *

for SUF in SUFFIXES:
    if '_' in SUF:
        print("No underscore ('_') allowed in SUFFIXES. Please fix " + SUF)
        exit(0)
if len(SUFFIXES) != len(COMMANDS) or len(COMMANDS) != NUM_VERSIONS:
    print("Invalid number of versions running!")
    exit(0)
create_necessary_dirs()

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

while True:
    user_input = input("Do you want to continue? Type 'yes' to proceed ('no' to exit): ")
    if user_input.lower() == "yes":
        break  # Exit the loop if the user enters 'yes'
    elif user_input.lower() == "no":
        exit(0)

SETTINGS_LOG_PATH = PATH + "/log_settings/" + TEST_NAME
create_dirs(SETTINGS_LOG_PATH)
# Construct the source and destination paths
source_path = os.path.join(PATH, "settings.py")
destination_path = os.path.join(SETTINGS_LOG_PATH, "settings.py")

# Copy the file
shutil.copyfile(source_path, destination_path)

print(f"File 'settings.py' copied from {source_path} to {destination_path}")

def job_sub_commands_generator(filename):
    # if filename == "dna_M7024_767_5814" or filename == "dna_M7964_640_25260" or \
    #     filename == "dna_M7929_428_15016" or filename == "dna_M12051_699_6914":
    #     return
    for i in range(NUM_RUNS):
        for id in range(len(COMMANDS)):
            s = COMMANDS[id].replace("?", filename) + '_' + str(SEEDS[i]) + ' -seed ' + str(SEEDS[i])
            # script_path = SCRIPTS_PATH + "/" + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ".sh"
            # with open(script_path, "w") as f:
            #     f.write("#!/bin/bash\n")
            #     f.write(s)
            # c = 'qsub -q long_cpu -N ' + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ' -l select=1:ncpus=1 -j oe ' + script_path
            c = 'bsub -q normal -J ' + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ' "' + s + '"'
            os.system(c)
        time.sleep(0.09)

# Subscribe jobs to the system
for file_name in list_of_files_desc_size:
  job_sub_commands_generator(file_name)
