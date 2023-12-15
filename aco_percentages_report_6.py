import sys
import matplotlib.pyplot as plt
import random

if len(sys.argv) != 2:
    print("Usage: python read_file.py <file_path>")
    exit(0)
file_path = sys.argv[1]
ratchets = []
iqps = []
random_nnis = []
nnis = []
sprs = []
tbrs = []
with open(file_path, 'r') as file:
    content = file.read().split('\n')
    i = 0
    while i < len(content):
        if content[i] == "%Phero:":
            assert(i + 6 < len(content))
            for j in range(6):
                num = float(content[i + j + 1].split()[2])
                if j == 0:
                    ratchets.append(num)
                elif j == 1:
                    iqps.append(num)
                elif j == 2:
                    random_nnis.append(num)
                elif j == 3:
                    nnis.append(num)
                elif j == 4:
                    sprs.append(num)
                else:
                    tbrs.append(num)
            i += 6
        i += 1
noise = 0.008
for i in range(len(ratchets)):
    if abs(ratchets[i] - iqps[i]) < noise:
        if random.randint(0, 1):
            ratchets[i] += noise * random.uniform(0, 1)
            iqps[i] -= noise * random.uniform(0, 1)
        else:
            ratchets[i] -= noise * random.uniform(0, 1)
            iqps[i] += noise * random.uniform(0, 1)
    if abs(ratchets[i] - random_nnis[i]) < 0.01:
        if random.randint(0, 1):
            ratchets[i] += noise * random.uniform(0, 1)
            random_nnis[i] -= noise * random.uniform(0, 1)
        else:
            ratchets[i] -= noise * random.uniform(0, 1)
            random_nnis[i] += noise * random.uniform(0, 1)
x = [i + 1 for i in range(len(nnis))]
# Create a new figure and axes object
fig, ax = plt.subplots()
# Plotting the data
ax.plot(x, ratchets, color='red', label='RATCHET')
ax.plot(x, iqps, color='blue', label='IQP')
ax.plot(x, random_nnis, color='green', label='RANDOM_NNI')
ax.plot(x, nnis, color='orange', label='NNI')
ax.plot(x, sprs, color='purple', label='SPR')
ax.plot(x, tbrs, color='pink', label='TBR')

# Add labels and title
ax.set_xlabel('Iterations')
ax.set_ylabel('Pheromone Percentages')
ax.set_title('Pheromone Percentages throughtout 1 run')

# Add legend
ax.legend()

# Hide xticks
plt.xticks([])

# Display the plot
plt.savefig('tem.png')

