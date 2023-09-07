import json
import random
import numpy as np
from tqdm import tqdm
from itertools import cycle
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D


with open('/Users/bernoulli_hermes/projects/python_summer/refined_pages.json', 'r') as f:
    data = json.load(f)

filtered_data = []
for entry in data:
    segdict = entry['segdict']
    filtered_segdict = {k: v for k, v in segdict.items() if len(k) > 1}
    entry['segdict'] = filtered_segdict
    filtered_data.append(entry)

all_segnames = list(set(segname for entry in filtered_data for segname in entry['segdict'].keys()))
selected_segnames = random.sample(all_segnames, min(200000, len(all_segnames)))
segname_to_index = {segname: i for i, segname in enumerate(selected_segnames)}

selected_data = random.sample(filtered_data, min(20000, len(filtered_data)))
feature_matrix = np.zeros((len(selected_data), len(selected_segnames)))

for i, entry in tqdm(enumerate(selected_data), total=len(selected_data), desc="Creating feature matrix"):
    segdict = entry['segdict']
    for segname, count in segdict.items():
        j = segname_to_index.get(segname)
        if j is not None:
            feature_matrix[i, j] = count

tsne = TSNE(n_components=3, random_state=0)
transformed_data = tsne.fit_transform(feature_matrix)
selected_keywords = ['小米', '比亚迪','宁德时代']
keyword_to_color = {'小米': [1, 0, 0],  # 红色
                    '比亚迪': [0, 0, 1],
                    '宁德时代': [0, 1, 0]}

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

for i, entry in tqdm(enumerate(selected_data), total=len(selected_data), desc="Plotting"):
    x, y, z = transformed_data[i]
    keywords = entry['keywords']
    relevant_keywords = [keyword for keyword in keywords if keyword in selected_keywords]

    if relevant_keywords:
        color = np.mean([keyword_to_color[keyword] for keyword in relevant_keywords], axis=0)


        ax.scatter(x, y, z, c=[color])

plt.show()
