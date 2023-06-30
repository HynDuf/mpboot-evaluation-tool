import os
from helper_func import *
from settings import *

# Check if enough of log files
expected_file_count = NUM_RUNS * len(COMMANDS) * NUM_DATASET_FILES
file_extensions = ['.log', '.mpboot', '.treefile']
file_counts = {ext: 0 for ext in file_extensions}
for filename in os.listdir(LOG_PATH):
    file_extension = os.path.splitext(filename)[1]
    if file_extension in file_extensions:
        file_counts[file_extension] += 1
all_file_counts_valid = all(count == expected_file_count for count in file_counts.values())

if not all_file_counts_valid:
    for count in file_counts.values():
        print(count)
    print("Number of log files is not valid.")
    exit(0)

create_dirs(DETAILS_RESULT_PATH)

analyse_phase_1()
analyse_phase_2()
analyse_phase_3()

output_result()
 


