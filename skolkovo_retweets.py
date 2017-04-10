import matplotlib.pyplot as plt
from collections import Counter

with open('skolkovo.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
names = Counter([line.split()[6][:-1]
                 for line in lines if 'RT ' in line])
names = dict(names.most_common(10))

labels = sorted(names.keys())
nums = range(len(names))
twit_nums = [names[key] for key in labels]

plt.bar(nums, twit_nums, align='center')
plt.xticks(nums, labels, rotation='vertical')
plt.subplots_adjust(bottom=0.3)
plt.show()
