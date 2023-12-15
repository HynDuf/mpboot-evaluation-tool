import csv
import matplotlib.pyplot as plt
import time
import numpy as np
import os
import math
import re
import shutil
from settings import *
import pandas as pd

global_best_score = {}
global_init_score = {}
global_ic_score = {}
avg_score_version_testfile = {}
avg_cputime_version_testfile = {}
aco_num_version_testfile = {}
stds_version_testfile = {}
sum_stds_version = {}
sum_cputime_version = {}
diff_tbr5_and_tnt = {}
summarize_anyway = False

def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Folder {path} already exists.")
        user_input = input("Do you want to delete and create a new one? Type 'yes' to proceed: ")
        if user_input.lower() == "yes":
            shutil.rmtree(path)
            os.makedirs(path)
        else:
            exit(0)

def create_necessary_dirs():
    create_dirs(LOG_PATH)
    create_dirs(SCRIPTS_PATH)
    if not os.path.exists(DATA_PATH):
        print(f"Error: DATA_PATH {DATA_PATH} doesn't exist.")
        exit(0)

def remove_files_in_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in the directory '{directory_path}' have been removed.")
    else:
        print(f"Directory '{directory_path}' does not exist.")

def update_dict_max(dictionary, key, value):
    if key in dictionary:
        dictionary[key] = max(dictionary[key], value)
    else:
        dictionary[key] = value

def update_dict_min(dictionary, key, value):
    if key in dictionary:
        dictionary[key] = min(dictionary[key], value)
    else:
        dictionary[key] = value

def update_dict1_add(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = 0
    dictionary[key] += value

def update_dict2_add(dictionary, key1, key2, value):
    if key1 not in dictionary:
        dictionary[key1] = {}
    if key2 not in dictionary[key1]:
        dictionary[key1][key2] = 0
    dictionary[key1][key2] += value

def update_dict3_add(dictionary, key1, key2, key3, value):
    if key1 not in dictionary:
        dictionary[key1] = {}
    if key2 not in dictionary[key1]:
        dictionary[key1][key2] = {}
    if key3 not in dictionary[key1][key2]:
        dictionary[key1][key2][key3] = 0
    dictionary[key1][key2][key3] += value

def check_valid_num_log_files():
    # Get list of all files only in the given directory
    list_of_files_desc_size = filter(
        lambda x: os.path.isfile(os.path.join(LOG_PATH, x)),
        os.listdir(LOG_PATH))

    # Sort list of file names by size
    list_of_files_desc_size = sorted(
        list_of_files_desc_size,
        key=lambda x: os.stat(os.path.join(LOG_PATH, x)).st_size)
    list_of_files_desc_size.reverse()

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
        for key in file_counts:
            print(key, " : ", file_counts[key])
        print("Number of log files is not valid.")
        mp_seeds = {}
        for file in list_of_files_desc_size:
            if file.endswith(".log") or file.endswith(".treefile") or file.endswith(".mpboot"):
                parts = file.split('.')
                version_parts = parts[-2].split('_')
                s = version_parts[-1]

                update_dict1_add(mp_seeds, s, 1)

        # Get list of all .phy files in the given directory
        data_files = filter(
            lambda x: os.path.isfile(os.path.join(DATA_PATH, x)) and x.endswith(".phy"
                                                                                ),
            os.listdir(DATA_PATH))
        # Sort list of file names by size
        data_files = sorted(
            data_files,
            key=lambda x: os.stat(os.path.join(DATA_PATH, x)).st_size)
        data_files.reverse()

        if len(data_files) != NUM_DATASET_FILES:
            print(len(data_files))
            print("Missing entire test files")
            exit(0)
        
        while True:
            user_input = input("Do you want to resubmit the missing log files?\nType 'yes'/'no'/'anyway' to proceed/exit/summarize anyway: ")
            if user_input.lower() == "yes":
                break
            elif user_input.lower() == "no":
                exit(0)
            elif user_input.lower() == "anyway":
                summarize_anyway = True
                return
        num_missing = 0
        for filename in data_files:
            for seed in mp_seeds:
                if int(seed) > 32 or int(seed) < 31:
                    continue
                for id in range(len(COMMANDS)):
                    f = filename + "_" + SUFFIXES[id] + "_" + str(seed) + ".mpboot"
                    full_path = os.path.join(LOG_PATH, f)
                    if not os.path.exists(full_path):
                        print(full_path)
                        num_missing += 1
                        s = COMMANDS[id].replace("?", filename) + '_' + str(seed) + ' -seed ' + str(seed)
                        # script_path = SCRIPTS_PATH + "/" + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ".sh"
                        # with open(script_path, "w") as f:
                        #     f.write("#!/bin/bash\n")
                        #     f.write(s)
                        # c = 'qsub -q long_cpu -N ' + filename + "_" + SUFFIXES[id] + "_" + str(SEEDS[i]) + ' -l select=1:ncpus=1 -j oe ' + script_path
                        c = 'bsub -q normal -J ' + filename + "_" + SUFFIXES[id] + "_" + str(seed) + ' "' + s + '"'
                        os.system(c)
                # time.sleep(0.09)
        print("Resubmitted", num_missing, "commands")
        exit(0)

def find_next_whitespace(string, start_position):
    return next((i + start_position for i, char in enumerate(string[start_position:]) if char.isspace()), -1)

def get_float_with_prefix(content, pref):
    idx = content.rfind(pref)
    sp = find_next_whitespace(content, idx + len(pref))
    return float(content[idx + len(pref):sp])

def get_int_with_prefix(content, pref):
    idx = content.rfind(pref)
    sp = find_next_whitespace(content, idx + len(pref))
    return int(content[idx + len(pref):sp])

def get_second_last_int_with_prefix(content, pref):
    idx = content.rfind(pref)
    if content.count(pref) > 1:
        idx = content.rfind(pref, 0, idx - 1)
    sp = find_next_whitespace(content, idx + len(pref))
    return int(content[idx + len(pref):sp])

def extract_testfile_and_version(filename):
    # dna_M4399_205_8913.phy_SPR5_1234.log
    # testfile: dna_M4399_205_8913
    # version: SPR5

    parts = filename.split('.')
    testfile_parts = parts[0].split('_')
    version_parts = parts[-2].split('_')
    testfile = '_'.join(testfile_parts[:])
    version = version_parts[-2]

    return testfile, version

def extract_n_from_file(filename):
    # dna_M4399_205_8913
    # Returns: 205
    if filename == "example":
        return 17
    elif filename == "prot_M8569_164_383_edited":
        return 164
    pattern = r'_(\d+)_\d+$'
    match = re.search(pattern, filename)
    if match:
        return int(match.group(1))
    else:
        print("Invalid filename:", filename)
        exit(0)

def extract_n_and_m_from_file(filename):
    # dna_M4399_205_8913
    # Returns: 205, 8913
    if filename == "prot_M8569_164_383_edited":
        return 164, 383
    pattern = r'_(\d+)_(\d+)$'
    match = re.search(pattern, filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    else:
        print("Invalid filename:", filename)
        exit(0)

def get_ic_score_testfiles():
    for filename in os.listdir(DATA_PATH):
        if filename.endswith('.phy'):
            with open(DATA_PATH + "/" + filename, 'r') as file:
                print(filename)
                content = file.read().split("\n")
                n, m = map(int, content[0].split())
                rows = []
                for i in range(n):
                    rows.append(content[i + 1].split()[1])
                    assert(len(rows[i]) == m)
                char_cnt_all = {}
                for i in range(n):
                    for j in range(m):
                        update_dict1_add(char_cnt_all, rows[i][j], 1)
                for c in char_cnt_all:
                        char_cnt_all[c] /= n * m
                ic_score = 0
                for j in range(m):
                    char_cnt = {}
                    for i in range(n):
                        update_dict1_add(char_cnt, rows[i][j], 1)
                    
                    for c in char_cnt:
                        char_cnt[c] /= n
                        ic_score += char_cnt[c] * math.log(char_cnt[c] / char_cnt_all[c])
                global_ic_score[filename.split('.')[0]] = ic_score
                
def get_fallback_total_time(text):
    pattern = r'Time: (\d+)h:(\d+)m:(\d+)s \((\d+)h:(\d+)m:(\d+)s left\)'
    matches = list(re.finditer(pattern, text))
    if matches:
        hours, minutes, seconds, left_hours, left_minutes, left_seconds = map(int, matches[-1].groups())

        # Calculate total time in seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        total_seconds_left = left_hours * 3600 + left_minutes * 60 + left_seconds

        return total_seconds + total_seconds_left
    else:
        return None
def get_last_better_score(text):
    pattern = r'BETTER TREE FOUND at iteration \d+: (\d+)'
    matches = list(re.finditer(pattern, text))
    if matches:
        last_match = matches[-1]
        second_integer = last_match.group(1)
        return int(second_integer)
    else:
        return None
def analyse_phase_1():
    aco_num_valid_files = {}
    test_num_valid_files = {}
    for filename in os.listdir(LOG_PATH):
        if filename.endswith('.log'):
            testfile, version = extract_testfile_and_version(filename)
            with open(LOG_PATH + "/" + filename, 'r') as file:
                print(filename)
                content = file.read()
                fallback_time = get_fallback_total_time(content)
                if fallback_time == None:
                    print("Incomplete log file!")
                    continue
                update_dict2_add(test_num_valid_files, version, testfile, 1)
                cur_init_score = get_int_with_prefix(content, "Current best score: ")
                try:
                    cur_best_score = get_int_with_prefix(content, "BEST SCORE FOUND : ")
                except:
                    cur_best_score = get_last_better_score(content)
                    if cur_best_score == None:
                        cur_best_score = cur_init_score
                try:
                    cur_cpu_time = get_float_with_prefix(content, "Total CPU time used: ")
                except:
                    cur_cpu_time = fallback_time
                
                update_dict_min(global_best_score, testfile, cur_best_score)
                update_dict_max(global_init_score, testfile, cur_init_score)

                update_dict2_add(avg_score_version_testfile, version, testfile, cur_best_score)
                update_dict2_add(avg_cputime_version_testfile, version, testfile, cur_cpu_time)

                if version.startswith("ACO"):
                    try:
                        num_nni = get_int_with_prefix(content, "NNI : ")
                        num_spr = get_int_with_prefix(content, "SPR : ")
                        num_tbr = get_int_with_prefix(content, "TBR : ")

                        update_dict3_add(aco_num_version_testfile, version, testfile, "NNI", num_nni)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "SPR", num_spr)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "TBR", num_tbr)
                        update_dict2_add(aco_num_valid_files, version, testfile, 1)
                    except Exception as e:
                        print(filename, "can't read #NNI, SPR or TBR")
                elif version.startswith("ACO6"):
                    try:
                        num_ratchet = get_int_with_prefix(content, "RATCHET : ")
                        num_iqp = get_int_with_prefix(content, "IQP : ")
                        num_random_nni = get_int_with_prefix(content, "RANDOM_NNI : ")
                        num_nni = get_int_with_prefix(content, "NNI : ")
                        num_spr = get_int_with_prefix(content, "SPR : ")
                        num_tbr = get_int_with_prefix(content, "TBR : ")

                        update_dict3_add(aco_num_version_testfile, version, testfile, "RATCHET", num_ratchet)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "IQP", num_iqp)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "RANDOM_NNI", num_random_nni)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "NNI", num_nni)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "SPR", num_spr)
                        update_dict3_add(aco_num_version_testfile, version, testfile, "TBR", num_tbr)
                        update_dict2_add(aco_num_valid_files, version, testfile, 1)
                    except Exception as e:
                        print(filename, "can't read #NNI, SPR or TBR")

    for version in avg_score_version_testfile:
        for testfile in global_best_score:
            avg_score_version_testfile[version][testfile] /= test_num_valid_files[version][testfile]
            avg_cputime_version_testfile[version][testfile] /= test_num_valid_files[version][testfile]

            if version.startswith("ACO"):
                for type in aco_num_version_testfile[version][testfile]:
                    assert(aco_num_valid_files[version][testfile] <= NUM_RUNS)
                    aco_num_version_testfile[version][testfile][type] /= aco_num_valid_files[version][testfile]
            elif version.startswith("ACO6"):
                for type in aco_num_version_testfile[version][testfile]:
                    assert(aco_num_valid_files[version][testfile] <= NUM_RUNS)
                    aco_num_version_testfile[version][testfile][type] /= aco_num_valid_files[version][testfile]

def analyse_phase_2():
    include_intensive_TNT = False
    user_input = input("Do you want to include intensive TNT result? Type 'yes' to proceed: ")
    if user_input.lower() == "yes":
        include_intensive_TNT = True
    if include_intensive_TNT:
        try:
            tnt_best_score, tnt_sum_time = read_tnt_csv_bb1000()
        except Exception as e:
            print("Error reading TNT csv file. Fallback to not include TNT result.\n", e)
            include_intensive_TNT = False
    if include_intensive_TNT:
        tnt_sum_stds = 0
        for testfile in global_best_score:
            mp_score = tnt_best_score.get(testfile, 0)
            if mp_score == 0:
                print(testfile, "not found in TNT result")
                exit(0)
            update_dict_min(global_best_score, testfile, mp_score)
            tnt_sum_stds += mp_score - global_best_score[testfile]
        sum_stds_version['intensive_TNT'] = tnt_sum_stds
        sum_cputime_version['intensive_TNT'] = tnt_sum_time
        for version in avg_score_version_testfile:
            if version == "TBR5":
                for testfile in global_best_score:
                    diff_tbr5_and_tnt[testfile] = avg_score_version_testfile['TBR5'][testfile] - tnt_best_score[testfile]

    test_num_valid_files = {}
    for filename in os.listdir(LOG_PATH):
        if filename.endswith('.log'):
            testfile, version = extract_testfile_and_version(filename)
            with open(LOG_PATH + "/" + filename, 'r') as file:
                content = file.read()
                fallback_time = get_fallback_total_time(content)
                if fallback_time == None:
                    print("Incomplete log file!")
                    continue
                update_dict2_add(test_num_valid_files, version, testfile, 1)
                cur_init_score = get_int_with_prefix(content, "Current best score: ")
                try:
                    cur_best_score = get_int_with_prefix(content, "BEST SCORE FOUND : ")
                except:
                    cur_best_score = get_last_better_score(content)
                    if cur_best_score == None:
                        cur_best_score = cur_init_score

                update_dict2_add(stds_version_testfile, version, testfile, (cur_best_score - global_best_score[testfile])**2)
    for version in avg_score_version_testfile:
        for testfile in global_best_score:
            stds_version_testfile[version][testfile] /= test_num_valid_files[version][testfile]
            stds_version_testfile[version][testfile] = math.sqrt(stds_version_testfile[version][testfile])

def analyse_phase_3():
    for version in avg_score_version_testfile:
        for testfile in global_best_score:
            update_dict1_add(sum_cputime_version, version, avg_cputime_version_testfile[version][testfile])
            update_dict1_add(sum_stds_version, version, stds_version_testfile[version][testfile])

def plot_aco_usages(aco_csv_file, folder_path):
    # Read the data from the CSV file
    x = []
    nni = []
    spr = []
    tbr = []

    with open(aco_csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            x.append(i)
            sum_layer_2 = float(row['NNI']) + float(row['SPR']) + float(row['TBR'])
            nni.append(float(row['NNI']) / sum_layer_2)
            spr.append(float(row['SPR']) / sum_layer_2)
            tbr.append(float(row['TBR']) / sum_layer_2)

    # Apply moving average smoothing
    window_size = 1
    nni_smoothed = pd.Series(nni).rolling(window=window_size, center=True).mean()
    spr_smoothed = pd.Series(spr).rolling(window=window_size, center=True).mean()
    tbr_smoothed = pd.Series(tbr).rolling(window=window_size, center=True).mean()
    # Create a new figure and axes object
    fig, ax = plt.subplots()
    # Plotting the data
    ax.plot(x, nni_smoothed, color='blue', label='NNI')
    ax.plot(x, spr_smoothed, color='green', label='SPR')
    ax.plot(x, tbr_smoothed, color='purple', label='TBR')

    # Add labels and title
    ax.set_xlabel('Dataset Difficulty')
    ax.set_ylabel('Percentage')
    ax.set_title('Usage of ACO types')

    # Add legend
    ax.legend()

    # Display the plot
    plt.savefig(folder_path + '/aco_usages.png')

def plot_aco6_usages(aco_csv_file, folder_path):
    # Read the data from the CSV file
    x = []
    ratchet = []
    iqp = []
    random_nni = []
    nni = []
    spr = []
    tbr = []

    with open(aco_csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            x.append(i)
            sum_layer_1 = float(row['RATCHET']) + float(row['IQP']) + float(row['RANDOM_NNI'])
            ratchet.append(float(row['RATCHET']) / sum_layer_1)
            iqp.append(float(row['IQP']) / sum_layer_1)
            random_nni.append(float(row['RANDOM_NNI']) / sum_layer_1)
            sum_layer_2 = float(row['NNI']) + float(row['SPR']) + float(row['TBR'])
            nni.append(float(row['NNI']) / sum_layer_2)
            spr.append(float(row['SPR']) / sum_layer_2)
            tbr.append(float(row['TBR']) / sum_layer_2)

    # Apply moving average smoothing
    window_size = 1
    ratchet_smoothed = pd.Series(ratchet).rolling(window=window_size, center=True).mean()
    iqp_smoothed = pd.Series(iqp).rolling(window=window_size, center=True).mean()
    random_nni_smoothed = pd.Series(random_nni).rolling(window=window_size, center=True).mean()
    nni_smoothed = pd.Series(nni).rolling(window=window_size, center=True).mean()
    spr_smoothed = pd.Series(spr).rolling(window=window_size, center=True).mean()
    tbr_smoothed = pd.Series(tbr).rolling(window=window_size, center=True).mean()
    # Create a new figure and axes object
    fig, ax = plt.subplots()
    # Plotting the data
    ax.plot(x, ratchet_smoothed, color='red', label='RATCHET')
    ax.plot(x, iqp_smoothed, color='blue', label='IQP')
    ax.plot(x, random_nni_smoothed, color='green', label='RANDOM_NNI')
    ax.plot(x, nni_smoothed, color='orange', label='NNI')
    ax.plot(x, spr_smoothed, color='purple', label='SPR')
    ax.plot(x, tbr_smoothed, color='pink', label='TBR')

    # Add labels and title
    ax.set_xlabel('Dataset Difficulty')
    ax.set_ylabel('Percentage')
    ax.set_title('Usage of ACO types')

    # Add legend
    ax.legend()

    # Display the plot
    plt.savefig(folder_path + '/aco_usages.png')

def plot_sorted_sum_stds(versions, sum_stds):
    # Sort the versions by Sum STDs
    sorted_indices_stds = np.argsort(sum_stds)
    sorted_versions_stds = [versions[i] for i in sorted_indices_stds]
    sorted_avg_stds = [sum_stds[i] for i in sorted_indices_stds]

    # Create a plot sorted by Sum STDs
    fig, ax1 = plt.subplots()
    color_stds = 'tab:red'
    ax1.set_xlabel('Version')
    ax1.set_ylabel('Sum of STDs')

    bar_width = 0.6
    x_pos = np.arange(len(sorted_versions_stds))  # X positions for the bars

    ax1.bar(x_pos, sorted_avg_stds, color=color_stds, width=bar_width, label='Sum of STDs')
    ax1.tick_params(axis='y')

    # Display a legend
    ax1.legend(loc='upper left')

    # Set the x-axis tick positions and labels
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(sorted_versions_stds, ha='center')

    # # Add Bar Labels
    # for c in ax1.containers:
    #     ax1.bar_label(c)

    # Adjust spacing
    fig.tight_layout()

    # Save the plot to a file
    plt.savefig(RESULT_PATH + '/summarise_sum_stds.png')

def plot_sorted_sum_time(versions, sum_cputime):
    # Convert time from seconds to hours
    sum_cputime_hours = np.array(sum_cputime) / 3600.0

    # Sort the versions by Sum Time
    sorted_indices_time = np.argsort(sum_cputime_hours)
    sorted_versions_time = [versions[i] for i in sorted_indices_time]
    sorted_avg_time = [sum_cputime_hours[i] for i in sorted_indices_time]

    # Create a plot sorted by Sum Time
    fig, ax1 = plt.subplots()
    color_time = 'tab:blue'
    ax1.set_xlabel('Version')
    ax1.set_ylabel('Sum of Time (hours)')

    bar_width = 0.6
    x_pos = np.arange(len(sorted_versions_time))  # X positions for the bars

    ax1.bar(x_pos, sorted_avg_time, color=color_time, width=bar_width, label='Sum of Time (hours)')
    ax1.tick_params(axis='y')

    # Display a legend
    ax1.legend(loc='upper left')

    # Set the x-axis tick positions and labels
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(sorted_versions_time, ha='center')

    # # Add Bar Labels
    # for c in ax1.containers:
    #     ax1.bar_label(c)

    # Adjust spacing
    fig.tight_layout()

    # Save the plot to a file
    plt.savefig(RESULT_PATH + '/summarise_sum_time.png')
def plot_summarise_all_versions(summarise_csv_file):
    # Read the data from the CSV file
    versions = []
    sum_stds = []
    sum_cputime = []

    with open(summarise_csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            versions.append(row['Version'])
            sum_stds.append(float(row['Sum of STDs']))
            sum_cputime.append(float(row['Sum of Time (secs)']))

    plot_sorted_sum_stds(versions, sum_stds)
    plot_sorted_sum_time(versions, sum_cputime)
    # Sort the versions by Sum STDs
    sorted_indices_stds = np.argsort(sum_stds)
    sorted_versions_stds = [versions[i] for i in sorted_indices_stds]
    sorted_avg_stds = [sum_stds[i] for i in sorted_indices_stds]
    sorted_sum_cputime_stds = [sum_cputime[i] / 3600 for i in sorted_indices_stds]

    # Create a plot sorted by Sum STDs
    fig, ax1 = plt.subplots()
    color_stds = 'tab:red'
    ax1.set_xlabel('Version')
    ax1.set_ylabel('Sum of STDs', color=color_stds)

    bar_width = 0.35  # Width of the bars
    x_pos = np.arange(len(sorted_versions_stds))  # X positions for the bars

    ax1.bar(x_pos, sorted_avg_stds, color=color_stds, width=bar_width, label='Sum of STDs')
    ax1.tick_params(axis='y', labelcolor=color_stds)

    # Create a twin axes for the Sum of Time
    ax2 = ax1.twinx()

    # Plot the Sum of Time in the same plot
    color_time = 'tab:blue'
    ax2.set_ylabel('Sum of Time (hours)', color=color_time)

    ax2.bar(x_pos + bar_width, sorted_sum_cputime_stds, color=color_time, width=bar_width, label='Sum of Time (hours)')
    ax2.tick_params(axis='y', labelcolor=color_time)

    # Display a legend
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Set the x-axis tick positions and labels
    ax1.set_xticks(x_pos + bar_width / 2)
    ax1.set_xticklabels(sorted_versions_stds, rotation=45, ha='right')

    # Adjust spacing between subplots
    fig.tight_layout()

    # Save the plot to a file
    plt.savefig(RESULT_PATH + '/summarise_both_sorted_by_sum_stds.png')

    # Sort the versions by Sum of Time
    sorted_indices_time = np.argsort(sum_cputime)
    sorted_versions_time = [versions[i] for i in sorted_indices_time]
    sorted_avg_stds_time = [sum_stds[i] for i in sorted_indices_time]
    sorted_sum_cputime_time = [sum_cputime[i] / 3600 for i in sorted_indices_time]

    # Create a plot sorted by Sum of Time
    fig, ax3 = plt.subplots()
    ax3.set_xlabel('Version')
    ax3.set_ylabel('Sum STDs', color=color_stds)

    ax3.bar(x_pos, sorted_avg_stds_time, color=color_stds, width=bar_width, label='Sum of STDs')
    ax3.tick_params(axis='y', labelcolor=color_stds)

    ax4 = ax3.twinx()
    ax4.set_ylabel('Sum of Time (hours)', color=color_time)

    ax4.bar(x_pos + bar_width, sorted_sum_cputime_time, color=color_time, width=bar_width, label='Sum of Time (hours)')
    ax4.tick_params(axis='y', labelcolor=color_time)

    # Display a legend
    ax3.legend(loc='upper left')
    ax4.legend(loc='upper right')

    # Set the x-axis tick positions and labels
    ax3.set_xticks(x_pos + bar_width / 2)
    ax3.set_xticklabels(sorted_versions_time, rotation=45, ha='right')

    # Adjust spacing between subplots
    fig.tight_layout()

    # Save the plot to a file
    plt.savefig(RESULT_PATH + '/summarise_both_sorted_by_sum_time.png')

def read_tnt_csv_bb1000():
    TNT_CSV = "intensive_TNT_bb.csv"
    tnt_best_score = {}
    tnt_sum_time = 0

    with open(TNT_CSV, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row

        for row in csv_reader:
            test_file, mp_score, time_seconds = row
            mp_score = float(mp_score)  # Convert to float if needed
            time_seconds = float(time_seconds)  # Convert to float if needed

            tnt_best_score[test_file] = mp_score 
            tnt_sum_time += time_seconds
    return tnt_best_score, tnt_sum_time

def output_result():
    # global.csv saved global values like Global best score, Worst init score
    with open(RESULT_PATH + "/global.csv", "w") as csvfile:
        fieldnames = ["Filename", "Best Score", "Init Score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for testfile in global_best_score:
            writer.writerow({
                "Filename": testfile,
                "Best Score": global_best_score[testfile],
                "Init Score": global_init_score[testfile],
            })
    # summarise.csv saved summarise values or each version like Average STDS, Sum of Time (secs)
    with open(RESULT_PATH + "/summarise.csv", "w") as csvfile:
        fieldnames = ["Version", "Sum of STDs", "Sum of Time (secs)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for version in sum_cputime_version:
            writer.writerow({
                "Version": version,
                "Sum of STDs": sum_stds_version[version],
                "Sum of Time (secs)": sum_cputime_version[version],
            })

    # Plot the summarise graph
    plot_summarise_all_versions(RESULT_PATH + "/summarise.csv")
    
    # Detailed results for each version saved in its own folder
    for version in sum_cputime_version:
        if version == "intensive_TNT":
            continue
        cur_path = DETAILS_RESULT_PATH + "/" + version
        create_dirs(cur_path)
        with open(cur_path + "/result.csv", "w") as csvfile:
            fieldnames = ["Filename", "Average MP", "STDs", "Time (secs)"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for testfile in avg_score_version_testfile[version]:
                writer.writerow({
                    "Filename": testfile,
                    "Average MP": avg_score_version_testfile[version][testfile],
                    "STDs": stds_version_testfile[version][testfile],
                    "Time (secs)": avg_cputime_version_testfile[version][testfile]
                })
        if version.startswith("ACO"):
            rows = []
            for testfile in avg_score_version_testfile[version]:
                n, m = extract_n_and_m_from_file(testfile)
                row = {
                    "Filename": testfile,
                    "Complexity.first": (diff_tbr5_and_tnt[testfile]) / (n * m),
                    "Complexity.second": global_init_score[testfile] / (n * m),
                    "NNI": aco_num_version_testfile[version][testfile]["NNI"],
                    "SPR": aco_num_version_testfile[version][testfile]["SPR"],
                    "TBR": aco_num_version_testfile[version][testfile]["TBR"],
                }
                rows.append(row)
            # Sorting the rows by Complexity.first and Complexity.second
            sorted_rows = sorted(rows, key=lambda row: (row["Complexity.first"], row["Complexity.second"]))
            
            # Writing the sorted rows to the CSV file
            with open(cur_path + "/aco.csv", "w", newline="") as csvfile:
                fieldnames = ["Filename", "Complexity.first", "Complexity.second", "RATCHET", "IQP", "RANDOM_NNI", "NNI", "SPR", "TBR"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sorted_rows)

            # Plot the ACO Usage plot
            plot_aco_usages(cur_path + "/aco.csv", cur_path)
        elif version.startswith("ACO6"):
            rows = []
            for testfile in avg_score_version_testfile[version]:
                n, m = extract_n_and_m_from_file(testfile)
                row = {
                    "Filename": testfile,
                    "Complexity.first": (global_init_score[testfile] - global_best_score[testfile]) / (n * m),
                    "Complexity.second": global_init_score[testfile] / (n * m),
                    "RATCHET": aco_num_version_testfile[version][testfile]["RATCHET"],
                    "IQP": aco_num_version_testfile[version][testfile]["IQP"],
                    "RANDOM_NNI": aco_num_version_testfile[version][testfile]["RANDOM_NNI"],
                    "NNI": aco_num_version_testfile[version][testfile]["NNI"],
                    "SPR": aco_num_version_testfile[version][testfile]["SPR"],
                    "TBR": aco_num_version_testfile[version][testfile]["TBR"],
                }
                rows.append(row)
            # Sorting the rows by Complexity.first and Complexity.second
            sorted_rows = sorted(rows, key=lambda row: (row["Complexity.first"], row["Complexity.second"]))
            
            # Writing the sorted rows to the CSV file
            with open(cur_path + "/aco.csv", "w", newline="") as csvfile:
                fieldnames = ["Filename", "Complexity.first", "Complexity.second", "RATCHET", "IQP", "RANDOM_NNI", "NNI", "SPR", "TBR"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(sorted_rows)

            # Plot the ACO Usage plot
            plot_aco6_usages(cur_path + "/aco.csv", cur_path)
