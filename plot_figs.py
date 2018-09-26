import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib


matplotlib.rcParams.update({'font.size': 15})
blue_patch = mpatches.Patch(color='blue', label='dev')
red_patch = mpatches.Patch(color='red', label='train')

dev_corr = []
train_corr = []
with open('log') as f:
    for line in f.readlines():
        tokens = line.rstrip().split()
        if 'Dev' in line:
            dev_corr.append(float(tokens[2]))
        elif 'Iteration' in line:
            train_corr.append(float(tokens[2]))
plt.plot([x for x in range(len(dev_corr))], train_corr, color='red')
plt.plot([x for x in range(len(dev_corr))], dev_corr, color='blue')
plt.axhline(y=0.5808, color='black')
plt.legend(handles=[red_patch, blue_patch])
plt.annotate('NLTK Stanford Dependency Parser',
    color='black',
    xy=(10, 0.6),
    xytext=(10, 0.6))
plt.ylabel('Correctness')
plt.xlabel('Epoch')
plt.show()

