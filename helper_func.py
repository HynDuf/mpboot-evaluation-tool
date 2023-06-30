import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import math
import re
from settings import *

global_best_score = {}
global_init_score = {}
avg_score_version_testfile = {}
avg_cputime_version_testfile = {}
aco_num_version_testfile = {}
stds_version_testfile = {}
sum_stds_version = {}
sum_cputime_version = {}

def create_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print(f"Error: Folder {path} already exists.")
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

def analyse_phase_1():
    for filename in os.listdir(LOG_PATH):
        if filename.endswith('.log'):
            testfile, version = extract_testfile_and_version(filename)
            with open(LOG_PATH + "/" + filename, 'r') as file:
                content = file.read()
                cur_best_score = get_int_with_prefix(content, "BEST SCORE FOUND : ")
                cur_init_score = get_int_with_prefix(content, "Current best score: ")
                cur_cpu_time = get_float_with_prefix(content, "Total CPU time used: ")
                if version.startswith("ACO"):
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
                
                update_dict_min(global_best_score, testfile, cur_best_score)
                update_dict_max(global_init_score, testfile, cur_init_score)

                update_dict2_add(avg_score_version_testfile, version, testfile, cur_best_score)
                update_dict2_add(avg_cputime_version_testfile, version, testfile, cur_cpu_time)

    for version in avg_score_version_testfile:
        for testfile in global_best_score:
            avg_score_version_testfile[version][testfile] /= NUM_RUNS
            avg_cputime_version_testfile[version][testfile] /= NUM_RUNS
            if version.startswith("ACO"):
                for type in aco_num_version_testfile[version][testfile]:
                    aco_num_version_testfile[version][testfile][type] /= NUM_RUNS

def analyse_phase_2():
    for filename in os.listdir(LOG_PATH):
        if filename.endswith('.log'):
            testfile, version = extract_testfile_and_version(filename)
            with open(LOG_PATH + "/" + filename, 'r') as file:
                content = file.read()
                cur_best_score = get_int_with_prefix(content, "BEST SCORE FOUND : ")

                update_dict2_add(stds_version_testfile, version, testfile, (cur_best_score - global_best_score[testfile])**2)
    for version in avg_score_version_testfile:
        for testfile in global_best_score:
            stds_version_testfile[version][testfile] /= NUM_RUNS
            stds_version_testfile[version][testfile] = math.sqrt(stds_version_testfile[version][testfile])

def analyse_phase_3():
    for version in avg_score_version_testfile:
        for testfile in global_best_score:
            update_dict1_add(sum_cputime_version, version, avg_cputime_version_testfile[version][testfile])
            update_dict1_add(sum_stds_version, version, stds_version_testfile[version][testfile])

def plot_aco_usages(aco_csv_file, folder_path):
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

    # Create a new figure and axes object
    fig, ax = plt.subplots()
    # Plotting the data
    ax.plot(x, ratchet, color='red', label='RATCHET')
    ax.plot(x, iqp, color='blue', label='IQP')
    ax.plot(x, random_nni, color='green', label='RANDOM_NNI')
    ax.plot(x, nni, color='orange', label='NNI')
    ax.plot(x, spr, color='purple', label='SPR')
    ax.plot(x, tbr, color='pink', label='TBR')

    # Add labels and title
    ax.set_xlabel('Dataset Complexity')
    ax.set_ylabel('Percentage')
    ax.set_title('Usage of ACO types')

    # Add legend
    ax.legend()

    # Display the plot
    plt.savefig(folder_path + '/aco_usages.png')

def plot_summarise_all_versions(summarise_csv_file):
    # Read the data from the CSV file
    versions = []
    sum_stds = []
    sum_cputime = []

    with open(summarise_csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            versions.append(row['Version'])
            sum_stds.append(float(row['Average STDs']))
            sum_cputime.append(float(row['Sum of Time (secs)']))

    # Sort the versions by Average STDs
    sorted_indices_stds = np.argsort(sum_stds)
    sorted_versions_stds = [versions[i] for i in sorted_indices_stds]
    sorted_avg_stds = [sum_stds[i] for i in sorted_indices_stds]
    sorted_sum_cputime_stds = [sum_cputime[i] for i in sorted_indices_stds]

    # Create a plot sorted by Average STDs
    fig, ax1 = plt.subplots()
    color_stds = 'tab:red'
    ax1.set_xlabel('Version')
    ax1.set_ylabel('Average STDs', color=color_stds)

    bar_width = 0.35  # Width of the bars
    x_pos = np.arange(len(sorted_versions_stds))  # X positions for the bars

    ax1.bar(x_pos, sorted_avg_stds, color=color_stds, width=bar_width, label='Average STDs')
    ax1.tick_params(axis='y', labelcolor=color_stds)

    # Create a twin axes for the Sum of Time
    ax2 = ax1.twinx()

    # Plot the Sum of Time in the same plot
    color_time = 'tab:blue'
    ax2.set_ylabel('Sum of Time (secs)', color=color_time)

    ax2.bar(x_pos + bar_width, sorted_sum_cputime_stds, color=color_time, width=bar_width, label='Sum of Time (secs)')
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
    plt.savefig(RESULT_PATH + '/summarise_sorted_by_sum_stds.png')

    # Sort the versions by Sum of Time
    sorted_indices_time = np.argsort(sum_cputime)
    sorted_versions_time = [versions[i] for i in sorted_indices_time]
    sorted_avg_stds_time = [sum_stds[i] for i in sorted_indices_time]
    sorted_sum_cputime_time = [sum_cputime[i] for i in sorted_indices_time]

    # Create a plot sorted by Sum of Time
    fig, ax3 = plt.subplots()
    ax3.set_xlabel('Version')
    ax3.set_ylabel('Average STDs', color=color_stds)

    ax3.bar(x_pos, sorted_avg_stds_time, color=color_stds, width=bar_width, label='Average STDs')
    ax3.tick_params(axis='y', labelcolor=color_stds)

    ax4 = ax3.twinx()
    ax4.set_ylabel('Sum of Time (secs)', color=color_time)

    ax4.bar(x_pos + bar_width, sorted_sum_cputime_time, color=color_time, width=bar_width, label='Sum of Time (secs)')
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
    plt.savefig(RESULT_PATH + '/summarise_sorted_by_sum_time.png')


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
                "Init Score": global_init_score[testfile]
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
                row = {
                    "Filename": testfile,
                    "Complexity.first": global_init_score[testfile] - global_best_score[testfile],
                    "Complexity.second": global_init_score[testfile] / extract_n_from_file(testfile),
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
            plot_aco_usages(cur_path + "/aco.csv", cur_path)
