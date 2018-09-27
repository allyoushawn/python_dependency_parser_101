import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
import pickle
import pdb

matplotlib.rcParams.update({'font.size': 15})
blue_patch = mpatches.Patch(color='blue', label='Shift-reduced Parser')
red_patch = mpatches.Patch(color='red', label='Stanford parser')

stanford_hit_file_name = 'stanford_hit.pkl'
stanford_total_file_name = 'stanford_total.pkl'
self_hit_file_name = 'self_parser_hit.pkl'
self_total_file_name = 'self_parser_total.pkl'

with open(stanford_hit_file_name, 'rb') as fp:
    st_hit = pickle.load(fp)
with open(stanford_total_file_name, 'rb') as fp:
    st_total = pickle.load(fp)

with open(self_hit_file_name, 'rb') as fp:
    self_hit = pickle.load(fp)
with open(self_total_file_name, 'rb') as fp:
    self_total = pickle.load(fp)

self_total = self_total[1:-1]
self_hit = self_hit[1:-1]
st_total = st_total[1:-1]
st_hit = st_hit[1:-1]

plt.plot(range(len(st_total)), [st_hit[i] / st_total[i] for i in range(len(st_total))], '-^', color='red')
plt.plot(range(len(self_total)), [self_hit[i] / self_total[i] for i in range(len(self_total))], '-^', color='blue')

plt.legend(handles=[red_patch, blue_patch])
plt.ylabel('Correctness')
plt.xlabel('Distance to Root')
plt.show()

