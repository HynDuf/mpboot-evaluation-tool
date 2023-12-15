import matplotlib.pyplot as plt
from settings import *
from helper_func import *
import os
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the coordinates of the equilateral triangle vertices
def equilateral_triangle(side_length):
    height = np.sqrt(3) * side_length / 2  # Calculate the height of the equilateral triangle

    # Vertices of the equilateral triangle
    vertex1 = [0, 0]
    vertex2 = [side_length, 0]
    vertex3 = [side_length / 2, height]

    return vertex1, vertex2, vertex3

def find_intersection(line1, line2):
    """
    Find the intersection point of two lines given their coefficients.
    
    Parameters:
    - line1: Tuple (m1, b1) representing the coefficients of the first line.
    - line2: Tuple (m2, b2) representing the coefficients of the second line.
    
    Returns:
    - Tuple (x, y) representing the intersection point.
    """
    m1, b1 = line1
    m2, b2 = line2

    # Check if the lines are parallel
    if m1 == m2:
        raise ValueError("Lines are parallel and do not intersect.")

    # Calculate the intersection point
    x = (b2 - b1) / (m1 - m2)
    y = m1 * x + b1

    return x, y

def distance_to_line(point, line_coefficients):
    """
    Calculate the distance between a point and a line.
    
    Parameters:
    - point: Tuple (x, y) representing the coordinates of the point.
    - line_coefficients: Tuple (A, B, C) representing the coefficients of the line equation Ax + By + C = 0.
    
    Returns:
    - The distance between the point and the line.
    """
    x, y = point
    A, B, C = line_coefficients

    # Calculate the distance
    distance = abs(A * x + B * y + C) / np.sqrt(A**2 + B**2)

    return distance

def transform_to_points(p_nni, p_spr, p_tbr):
    assert(abs(p_nni + p_spr + p_tbr - 1) < 1e-9)
    line1 = (0, p_nni)
    line2 = (-np.sqrt(3), 2 - 2 * p_tbr)
    (x, y) = find_intersection(line1, line2)
    assert(y == p_nni)
    assert(np.abs(distance_to_line((x, y), (-np.sqrt(3), -1, 2)) - p_tbr) < 1e-9)
    return (x, y)

def draw_perpendicular_line(ax, point, line_slope, line_intercept):
    # Calculate the perpendicular line
    if line_slope != 0:
        perpendicular_slope = -1 / line_slope
        perpendicular_intercept = point[1] - perpendicular_slope * point[0]

        # Find intersection point
        intersection_x = (line_intercept - perpendicular_intercept) / (perpendicular_slope - line_slope)
        intersection_y = perpendicular_slope * intersection_x + perpendicular_intercept

        # Plot the perpendicular line segment
        ax.plot([point[0], intersection_x], [point[1], intersection_y], linestyle='--', color='black', linewidth=4)

        # Calculate and display the length of the perpendicular segment
        length = np.sqrt((point[0] - intersection_x)**2 + (point[1] - intersection_y)**2)
        text = ""
        midx = (point[0] + + intersection_x) / 2
        midy = (point[1] + + intersection_y) / 2
        if line_intercept == 2:
            text = f'{length:.2f}'
            midx -= 0.02
            midy -= 0.03
        else:
            text = f'{length:.2f}'
            midx -= 0.09
            midy -= 0.04
        ax.text(midx, midy, text, rotation=0, color='black', fontsize=15)

    else:
        # For a line with slope 0, the perpendicular line is vertical
        ax.plot([point[0], point[0]], [point[1], 0], linestyle='--', color='black', linewidth=4)

        # Calculate and display the length of the perpendicular segment
        length = np.abs(point[1])
        ax.text(point[0] + 0.01, point[1] / 2, f'{length:.2f}', rotation=0, color='black', fontsize=15)

def draw_aco_triangle(prob_tuples, out_path):
    side_length = 2 / np.sqrt(3)

    vertex1, vertex2, vertex3 = equilateral_triangle(side_length)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.tick_params(axis='both', which='major', labelsize=18)

    ax.plot([vertex1[0], vertex2[0]], [vertex1[1], vertex2[1]], color='blue', linewidth=8)  # Side 1
    ax.plot([vertex2[0], vertex3[0]], [vertex2[1], vertex3[1]], color='purple', linewidth=8)   # Side 2
    ax.plot([vertex3[0], vertex1[0]], [vertex3[1], vertex1[1]], color='green', linewidth=8) # Side 3

    ax.set_xlim(0, vertex2[0])  # Adjusted to end at the right corner containing the triangle
    ax.set_ylim(0, vertex3[1])  # Adjusted to end at the top corner containing the triangle

    ax.set_aspect('equal', adjustable='box')

    ax.set_xlabel('NNI', fontsize=20)
    ax.set_ylabel('Probabilities', fontsize=20)
    ax.text(0.18, 0.5, "SPR", rotation=0, color='black', fontsize=20)
    ax.text(0.90, 0.5, "TBR", rotation=0, color='black', fontsize=20)
    ax.set_xticks([])

    np.random.seed(42)  # For reproducibility

    # prob_tuples = [(0.5, 0.3, 0.2), (0.55, 0.2, 0.25), (0.57, 0.13, 0.3), (0.6, 0.15, 0.25)]

    for prob_tuple in prob_tuples:
        point = transform_to_points(*prob_tuple)
        ax.scatter(point[0], point[1], marker='o', color='r', s=60, linewidths=9)

    average_point = np.mean(np.array([transform_to_points(*prob_tuple) for prob_tuple in prob_tuples]), axis=0)

    draw_perpendicular_line(ax, average_point, 0, 0)
    draw_perpendicular_line(ax, average_point, -np.sqrt(3), 2)
    draw_perpendicular_line(ax, average_point, np.sqrt(3), 0)

    ax.scatter(average_point[0], average_point[1], marker='x', color='black', s=210, linewidths=6, label='Average Point')

    ax.legend(fontsize=18)
    ax.grid(True, which='both', linestyle='--', linewidth=1)
    plt.savefig(out_path + '/aco_triangle.png')
    plt.close()

def draw_aco_triangle_path(prob_tuples, out_path):
    side_length = 2 / np.sqrt(3)

    vertex1, vertex2, vertex3 = equilateral_triangle(side_length)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.tick_params(axis='both', which='major', labelsize=18)

    ax.plot([vertex1[0], vertex2[0]], [vertex1[1], vertex2[1]], color='blue', linewidth=8)  # Side 1
    ax.plot([vertex2[0], vertex3[0]], [vertex2[1], vertex3[1]], color='purple', linewidth=8)   # Side 2
    ax.plot([vertex3[0], vertex1[0]], [vertex3[1], vertex1[1]], color='green', linewidth=8) # Side 3

    ax.set_xlim(0, vertex2[0])  # Adjusted to end at the right corner containing the triangle
    ax.set_ylim(0, vertex3[1])  # Adjusted to end at the top corner containing the triangle

    ax.set_aspect('equal', adjustable='box')

    ax.set_xlabel('NNI', fontsize=20)
    ax.set_ylabel('Percentages', fontsize=20)
    ax.text(0.18, 0.5, "SPR", rotation=0, color='black', fontsize=20)
    ax.text(0.90, 0.5, "TBR", rotation=0, color='black', fontsize=20)
    ax.set_xticks([])

    np.random.seed(42)  # For reproducibility

    # prob_tuples = [(0.5, 0.3, 0.2), (0.55, 0.2, 0.25), (0.57, 0.13, 0.3), (0.6, 0.15, 0.25)]
    points = []

    for prob_tuple in prob_tuples:
        point = transform_to_points(*prob_tuple)
        points.append(point)

    for point in points:
        ax.scatter(point[0], point[1], marker='o', color='r', s=60, linewidths=9.3)
    # Use the range of indices to determine the color gradient
    indices = np.arange(len(points))

    # Normalize indices to be in the range [0, 1] for the color map
    norm_indices = indices / (len(points) - 1)

    # Define the color map (yellow to red)
    cmap = plt.get_cmap('OrRd')
    ax.scatter([point[0] for point in points], 
                     [point[1] for point in points], 
                     marker='o', 
                     c=norm_indices, 
                     cmap=cmap, 
                     s=60, 
                     linewidths=9)

    draw_perpendicular_line(ax, points[-1], 0, 0)
    draw_perpendicular_line(ax, points[-1], -np.sqrt(3), 2)
    draw_perpendicular_line(ax, points[-1], np.sqrt(3), 0)

    ax.grid(True, which='both', linestyle='--', linewidth=3)
    plt.savefig(out_path)
    plt.close()

def draw_aco_pheromone_changes_3(log_file, out_path):
    nnis = []
    sprs = []
    tbrs = []
    better = []
    with open(log_file, 'r') as file:
        content = file.read().split('\n')
        i = 0
        while i < len(content):
            if content[i] == "%Phero:":
                if i > 0 and content[i - 1] == "BETTER":
                    better.append(1)
                else:
                    better.append(0)
                assert(i + 3 < len(content))
                for j in range(3):
                    num = float(content[i + j + 1].split()[2])
                    if j == 0:
                        nnis.append(num)
                    elif j == 1:
                        sprs.append(num)
                    elif j == 2:
                        tbrs.append(num)
                i += 3
            i += 1

    x = [i + 1 for i in range(len(nnis))]
    # Create a new figure and axes object
    fig, ax = plt.subplots()
    # Plotting the data
    ax.plot(x, nnis, color='blue', label='NNI')
    ax.plot(x, sprs, color='green', label='SPR')
    ax.plot(x, tbrs, color='purple', label='TBR')

    # Add labels and title
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Pheromone Percentages')
    ax.set_title('Pheromone Percentages throughtout 1 run')

    # Add legend
    ax.legend()

    # Hide xticks
    plt.xticks([])

    # Display the plot
    plt.savefig(out_path)
    plt.close()

def summarize_aco_3():
    for version in SUFFIXES:
        cur_path = ACO_DETAILS_RESULT_PATH + "/" + version
        create_dirs(cur_path)
        for filename in os.listdir(DATA_PATH):
            if filename.endswith('.phy'):
                print(f"Summarizing {filename}...")
                nxt_path = cur_path + "/" + filename.split('.')[0]
                create_dirs(nxt_path)
                nxt_changes_path = nxt_path + "/aco_pheromone_changes" 
                nxt_path_path = nxt_path + "/aco_pheromone_path" 
                create_dirs(nxt_changes_path)
                create_dirs(nxt_path_path)
                probs = []
                probs_path = []
                for logfile in os.listdir(LOG_PATH):
                    if logfile.endswith('.log') and logfile.startswith(filename + "_" + version + "_"):
                        with open(LOG_PATH + "/" + logfile, 'r') as file:
                            content = file.read()
                            try:
                                num_nni = get_int_with_prefix(content, "NNI : ")
                                num_spr = get_int_with_prefix(content, "SPR : ")
                                num_tbr = get_int_with_prefix(content, "TBR : ")
                            except Exception as e:
                                continue
                            sum3 = num_nni + num_spr + num_tbr
                            p_nni = num_nni / sum3
                            p_spr = num_spr / sum3
                            p_tbr = num_tbr / sum3
                            probs.append((p_nni, p_spr, p_tbr))

                            i = 0
                            while i < len(content):
                                nni, spr, tbr = 0, 0, 0
                                if content[i].startswith("NNI : "):
                                    for j in range(3):
                                        num = int(content[i + j].split()[2])
                                        if j == 0:
                                            nni = num 
                                        elif j == 1:
                                            spr = num
                                        elif j == 2:
                                            tbr = num
                                    i += 3
                                    sum = nni + spr + tbr
                                    p_nni = nni / float(sum)
                                    p_spr = spr / float(sum)
                                    p_tbr = tbr / float(sum)
                                    probs_path.append([p_nni, p_spr, p_tbr])
                                else:
                                    i += 1
                        draw_aco_pheromone_changes_3(LOG_PATH + "/" + logfile, nxt_changes_path + "/" \
                                                     + logfile.split(".")[1].split("_")[-1] + ".png")
                        draw_aco_triangle_path(probs_path, nxt_path_path + "/" \
                                                     + logfile.split(".")[1].split("_")[-1] + ".png")
                draw_aco_triangle(probs, nxt_path)

def summarize_aco_3_path(log_file):
    probs_path = []
    with open(log_file, 'r') as file:
        content = file.read().split('\n')
        i = 0
        while i < len(content):
            nni, spr, tbr = 0, 0, 0
            if content[i].startswith("NNI : "):
                for j in range(3):
                    num = int(content[i + j].split()[2])
                    if j == 0:
                        nni = num 
                    elif j == 1:
                        spr = num
                    elif j == 2:
                        tbr = num
                i += 3
                sum = nni + spr + tbr
                p_nni = nni / float(sum)
                p_spr = spr / float(sum)
                p_tbr = tbr / float(sum)
                probs_path.append([p_nni, p_spr, p_tbr])
            else:
                i += 1
    draw_aco_triangle_path(probs_path, "/home/diepht/hynduf/mpboot-evaluation-tool/aco_triangle_path.png")
